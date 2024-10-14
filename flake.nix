{
  description = "My NixHashSync application with Poetry integration";

  inputs = {
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, poetry2nix }:
    let
      system = "x86_64-linux";
    in
    { };
}

