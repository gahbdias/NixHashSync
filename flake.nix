{
  description = "My NixHashSync application with Poetry integration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-linux"; # Modifique conforme sua arquitetura
      # pkgs = import nixpkgs { system = "x86_64-linux"; };
    in
    {
      devShell.x86_64-linux = poetry2nix.mkPoetryApplication
        {
          src = ./.;
        };
      # devShell.x86_64-linux = pkgs.mkShell {
      #   buildInputs = [
      #     poetry2nix.packages.${pkgs.system}.poetry
      #     poetry2nix.mkPoetryEnv
      #     {
      #       projectDir = ./.;
      #     }
      #   ];
      # };
      # defaultPackage.${system} = poetry2nix.mkPoetryApplication {
      #   src = ./.;
      # };
    };
}

