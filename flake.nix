{
  description = "My NixHashSync application with Poetry integration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    poetry2nix.url = "github:nix-community/poetry2nix";
    flake-utils.url = github:numtide/flake-utils?branch=master;
  };

  outputs = { self, nixpkgs, poetry2nix, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = import ./overlays;
        pkgs = import nixpkgs {
          inherit system overlays;
        };
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
        myPythonApp = mkPoetryApplication { projectDir = ./.; };
      in
      {
        apps.default = {
          type = "app";
          program = "${myPythonApp}/bin/nixhashsync";
        };
        packages.default = myPythonApp;
        devShells.default = pkgs.mkShell {
          buildInputs = [
            myPythonApp
            pkgs.direnv
            pkgs.poetry
          ];
        };
      });
}

