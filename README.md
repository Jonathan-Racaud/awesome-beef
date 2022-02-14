<div style="text-align:center"><img src="github_banner_transparent.png"/></div>

# Awesome Beef [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)
A curated list of awesome Beef framework, libraries and resources.

Inspired by [awesome-python](https://github.com/vinta/awesome-python).

# Summary
- [Official Resources](#official-resources)
- [Frameworks and Libraries](#frameworks-and-libraries)
    - [Algorithms](#algorithms)
        - [Cryptography and Hashing](#cryptography-and-hashing)
        - [Noise](#noise)
    - [Caching](#caching)
    - [Command Line Interface Development](#command-line-interface-development)
    - [Coroutines](#coroutines)
    - [Game Development](#game-development)
        - [Engines](#engines)
        - [Frameworks](#frameworks)
        - [Libraries](#libraries)
    - [GUI](#gui)
    - [IoC](#ioc)
    - [Logging](#logging)
    - [Networking](#networking)
    - [Scripting Engines](#scripting-engines)
    - [Serialization](#serialization)
    - [Themes](#themes)
    - [Text Processing](#text-processing)
- [Projects and Articles](#projects-and-articles)
    - [Dynamic Linking](#dynamic-linking)
    - [Networking](#networking)
- [Contributing](#contributing)

# Official resources
*The official documentation and resource for the Beef programming language.*

- [Official website](https://beeflang.org) - Official website of the Beef programming language.
- [Official documentation](https://beeflang.org/docs) - Official documentation explaining how the language wworks and its philosophy.
- [Corelib documentation](https://www.beeflang.org/docs/doxygen/corlib/html/index.html) - Auto generated documentation for the core library.
- [Official repository](https://github.com/beefytech/Beef) - Repository hosting the language and its associated IDE.

# Frameworks and Libraries
## Algorithms
*Libraries providing implementations of algorithms*

### Cryptography and Hashing
- [Beef-Hash](https://github.com/thibmo/Beef-Hash) - Collection of hashing algorithms.
- [Beef-OpenSSL](https://github.com/thibmo/Beef-OpenSSL) - Beef port of OpenSSL.

### Noise
- [FastNoise_Beef](https://github.com/EinBurgbauer/FastNoise_Beef) - Beef port of the FastNoise Lite library.

### Caching
- [System.Caching](https://github.com/thibmo/System.Caching) - A BeefLang implementation of .net System.Runtime.Caching, useful to prevent double-triggering, response caching, data caching, etc.

## Command Line Interface Development
*Libraries for building CLI applications*

- [CowieCLI](https://github.com/RogueMacro/CowieCLI) - Awesome command line arguments parsing library.

## Coroutines
*Libraries related to coroutines and multithread programming*

- [Minicoro-beef](https://github.com/jazzbre/minicoro-beef) - Wrapper for the C asymetric coroutines library.

## Game Development
*Awesome game development libraries and frameworks.*

### Engines
- [Strawberry](https://github.com/MattThorson/Strawberry) - A 2D game engine using SDL, focused on usability and simplicity.
- [Tilengine-beef](https://github.com/rootbeerking/Tilengine-Beef) - Beef Language wrapper for Tilengine 2D Graphics Engine.

### Frameworks
- [Pile](https://github.com/EinBurgbauer/Pile) - A simple extendable game framework.
- [Raylib-beef](https://github.com/M0n7y5/raylib-beef) - A raylib binding for Beef programming language.

### Libraries
- [BGFX-beef](https://github.com/jazzbre/bgfx-beef) - A Cross-platform, graphics API agnostic, "Bring Your Own Engine/Framework" style rendering library.
    - Also linked in the official [BGFX repository](https://github.com/bkaradzic/bgfx/tree/master/bindings/bf). 
- [Box2D-beef](https://github.com/jazzbre/box2d-beef) - 2D physics engine for games.
- [Bulkan](https://github.com/jayrulez/Bulkan) - Low level Vulkan bindings.
- [Chipmunk2D-beef](https://github.com/jazzbre/Chipmunk2D-beef) - A simple, lightweight, fast and portable 2D rigid body physics library.
- [directx-beef](https://github.com/aharabada/directx-beef) - Beef wrapper library for Direct3D 11.
- [Glfw-beef](https://github.com/MineGame159/glfw-beef) - Beef wrapper library for GLFW.
- [Opengl-beef](https://github.com/MineGame159/opengl-beef) - OpenGL loader for Beef.
- [SDL2-beef](https://github.com/jazzbre/sdl2-beef) - SDL2 Wrapper, synced with SDL2 shipped with Beef.
- [sokol-beef](https://github.com/kochol/sokol-beef) - Auto generated library for [sokol](https://github.com/floooh/sokol) headers.
- [SoLoud-beef](https://github.com/jarikomppa/soloud) - easy to use, free, portable c/c++ audio engine for games.

## GUI
*Libraries and frameworks for general GUI programming*
- ImGui
    - [ImGui-beef](https://github.com/RogueMacro/imgui-beef) - Beef wrapper library for ImGui.
    - [ImGuibgfx-beef](https://github.com/jazzbre/imguibgfx-beef) - ImGui wrapper using SDL2 and BGFX.
    - [ImGui-Vulkan-beef](https://github.com/MineGame159/imgui-vulkan-beef) - Vulkan backend for Dear ImGui in Beef.
- [NativeFileDialog-beef](https://github.com/jazzbre/nativefiledialog-beef) - Portable library to invoke native file dialogs.
- [Ultralight-beef](https://github.com/kumikumi/Ultralight-beef) - Write UI code for your game/application with web technologies (HTML/CSS/JS) using a lightweight web renderer.

## IoC
*Inversion of Control libraries and frameworks*

- [Steak.DependencyInjection](https://github.com/RogueMacro/Steak.DependencyInjection) - Simple dependency injection library.

## Logging
*Logging libraries and frameworks.*

- [Steak.Logging](https://github.com/RogueMacro/Steak.Logging) - An awesome logging library for Beef.

## Networking
*Networking related libraries*

- [Beef-Net](https://github.com/thibmo/Beef-Net) - BeefLang networking library, based on lNet

## Scripting Engines
*Awesome scripting libraries.*

- [Lua-beef](https://github.com/thibmo/lua-beef) - BeefLang wrapper library for Lua.

## Serialization
*Libraries for serializing and parsing text*
- [Atma.Json](https://github.com/xposure/Atma.Json) - Json serialization framework.
- [Beef-toml](https://github.com/killamaaki/beef-toml) - Toml parser/serializer library.
- [Xml-Beef](https://github.com/thibmo/Xml-Beef) - Single-file XML parser in Beef with doctype support.

## Themes
*IDE themes.*

- [Dracula](https://github.com/fhornung/beef-dracula) - Dracula theme.
- [OneDarkPro](https://github.com/thibmo/BeefIDE-OneDarkPro) - Atom's iconic One Dark theme.
- [SimplyDark](https://github.com/M0n7y5/BeefIDE-SimplyDark) - Simple dark theme.

## Text Processing
*Libraries for parsing and manipulating plain texts.*

- [TinyRegex](https://github.com/disarray2077/TinyRegex) - Tiny implementation of a subset of Regex.

# Projects and Articles
*To show or explain what beef is capable of.*

## Dynamic Linking

- [Beef DLL Creation & Research](https://m0n7y5.github.io/beef-dll-creation-and-research-2/) - Showcase of a fully functional Beef DLL.

##  Networking

- [SampleListener](https://github.com/jairopaiva/SampleListener) - Example of an echo server showing the use of System.Net.Socket to listen for clients connections.


---

# Contributing

Your contributions are always welcome! Please take a look at the [contribution guidelines](https://github.com/Jonathan-Racaud/awesome-beef/blob/master/CONTRIBUTING.md) first.

I will keep some pull requests open if I'm not sure whether those libraries are awesome, you could [vote for them](https://github.com/Jonathan-Racaud/awesome-beef/pulls) by adding :+1: to them. Pull requests will be merged when their votes reach **20**.
