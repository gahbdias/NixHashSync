[
  (self: super: let 
    version = "1.8.2";
  in {
    poetry = super.poetry.overrideAttrs (oldAttrs: rec {
      inherit version;

      src = super.fetchFromGitHub {
        inherit version;
        owner = "python-poetry";
        repo = "poetry";
        rev = "1.8.2";
        sha256 = "1af9af53de544df0a8c8546dc0eb9f9a3330840c";
      };
    });
  })
]
