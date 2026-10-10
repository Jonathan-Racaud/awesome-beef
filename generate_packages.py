import os
import json
import logging
import time
import urllib.error
import urllib.parse
import urllib.request

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
log = logging.getLogger(__name__)

base_url = "https://api.github.com"
search_repositories_url = f"{base_url}/search/repositories"
repos_url = f"{base_url}/repos"

PER_PAGE = 100  # max allowed by GitHub

headers = {
    'Accept': 'application/vnd.github.text-match+json',
    'X-GitHub-Api-Version': '2026-03-10',
}

token = os.environ.get('GITHUB_TOKEN')
if token:
    headers['Authorization'] = f"Bearer {token}"
    log.info("Using GITHUB_TOKEN for authentication")
else:
    log.warning("No GITHUB_TOKEN set - unauthenticated rate limits apply (60 req/hour)")

topics = ['beef', 'beef-language', 'beef-programming-language', 'beeflang', 'beef-lang']

repos = []

def http_get(url, params=None):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read().decode('utf-8')), dict(response.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')[:500]
        log.error(f"GET {url} -> HTTP {e.code}: {body}")
        return e.code, None, {}
    except urllib.error.URLError as e:
        log.error(f"GET {url} -> network error: {e.reason}")
        return None, None, {}

def http_get_all_pages(url, base_params=None):
    """Fetch all pages of a paginated endpoint. Returns (status, items)."""
    all_items = []
    page = 1
    while True:
        params = dict(base_params or {})
        params['per_page'] = PER_PAGE
        params['page'] = page
        status, data, _ = http_get(url, params=params)

        if status != 200 or data is None:
            return status, all_items if all_items else None

        items = data if isinstance(data, list) else data.get('items', [])
        all_items.extend(items)

        if len(items) < PER_PAGE:
            return 200, all_items

        page += 1
        # Search API is limited to 30 requests/minute - pace ourselves when paging search results
        if '/search/' in url:
            time.sleep(2)

for topic in topics:
    status, items = http_get_all_pages(
        search_repositories_url,
        base_params={'q': f'topic:{topic}'}
    )

    if status != 200 or items is None:
        log.warning(f"Search for topic '{topic}' failed with status {status}, skipping")
        continue

    log.info(f"Topic '{topic}': {len(items)} matches fetched")

    for item in items:
        owner = item['owner']['login']
        name = item['name']
        languages_url = f"{repos_url}/{owner}/{name}/languages"

        lang_status, languages_json, _ = http_get(languages_url)

        if lang_status != 200 or not languages_json:
            log.info(f"  {owner}/{name}: languages request failed ({lang_status}), skipping")
            continue

        # Before github recognized Beef as a proper programming language it often categorized the code as being HyPhy and Brainfuck. Sometimes both at the same time.
        if not languages_json.keys() & {'Beef', 'HyPhy', 'Brainfuck'}:
            log.debug(f"  {owner}/{name}: languages = {list(languages_json.keys())}, excluded")
            continue

        log.info(f"  {owner}/{name}: kept")
        repos.append({
            'id': item['id'],
            'name': name,
            'owner': owner,
            'description': item['description'],
            'url': item['html_url'],
            'created_at': item['created_at'],
            'updated_at': item['updated_at'],
        })

log.info(f"After search phase: {len(repos)} repos collected")

# Remove duplicated repos (by id)
repos = list({repo['id']: repo for repo in repos}.values())
log.info(f"After dedup: {len(repos)} repos")

for repo in repos:
    repo_url = f"{repos_url}/{repo['owner']}/{repo['name']}"
    content_url = f"{repo_url}/contents/BeefProj.toml"
    tags_url = f"{repo_url}/tags"

    status, _, _ = http_get(content_url)

    if status == 200:
        log.info(f"  {repo['owner']}/{repo['name']}: BeefProj.toml found")
        repo['beef_package_manager_compatible'] = True

    status, data = http_get_all_pages(tags_url)

    repo['tags'] = data if (status == 200 and data is not None) else []
    log.info(f"  {repo['owner']}/{repo['name']}: {len(repo['tags'])} tags")

with open('packages.json', 'w') as f:
    json.dump(repos, f, indent=2)

log.info(f"Wrote {len(repos)} repos to packages.json")
