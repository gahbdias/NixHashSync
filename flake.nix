{
  description = "My NixHashSync application with Poetry integration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-linux";
      overlays = import ./overlays;
      pkgs = import nixpkgs {
        inherit system overlays;
      };
    in
    {
      # devShell.${system} = poetry2nix.mkPoetryEnv
      #   {
      #     python = "python3";
      #     projectDir = ./.;
      #     nativeBuildInputs = with pkgs;[
      #       poetry
      #       git
      #     ];
      #   };
    };
}

