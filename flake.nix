{
  description = "My NixHashSync application with Poetry integration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-linux"; # Modifique conforme sua arquitetura
    in
    {
      devShell.${system} = poetry2nix.mkPoetryEnv {
        projectDir = ./.;
      };
    };
}

