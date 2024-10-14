[
  (self: super: let 
    version = "1.8.2";
  in {
    super-poetry = super.poetry.overrideAttrs (oldAttrs: rec {
      inherit version;

      src = super.fetchFromGitHub {
        inherit version;
        owner = "python-poetry";
        repo = "poetry";
        rev = "1.8.2";
        sha256 = "058vyrby3q4632rgwfyix7fw0wjy51rqh7nmg3g9q7nl5xwra59h";
      };
    });
  })
]
