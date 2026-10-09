{ pkgs, lib, config, inputs, ... }:

{
  packages = with pkgs; [];

  languages.python = {
    enable = true;
    uv.enable = true;
  };
}
