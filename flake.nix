{
  description = "My NixHashSync application with Poetry integration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-darwin";
      overlays = import ./overlays;
      pkgs = import nixpkgs {
        inherit system overlays;
      };
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      myPythonApp = mkPoetryApplication { projectDir = ./.; };
    in
    {
      apps.${system}.default = {
        type = "app";
        program = "${myPythonApp}/bin/nixhashsync";
      };

      packages.${system}.default = myPythonApp;
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          myPythonApp # Adds the poetry-built application to the devShell
          pkgs.direnv # Include direnv for use flake in .envrc
          pkgs.super-poetry
        ];
      };
    };
}

