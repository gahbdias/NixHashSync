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
        sha256 = "1f2sq6xlivxk6j1ih8j5vw8xqkzs8hpl9c6s749q1q63lkrlx3mn";
      };
    });
  })
]
