[
  (self: super: let 
    version = "1.8.3";
  in {
    poetry = super.poetry.overrideAttrs (oldAttrs: rec {
      inherit version;

      src = super.fetchFromGitHub {
        inherit version;
        owner = "python-poetry";
        repo = "poetry";
        rev = "1.8.3";
        sha256 = "0s0d55x9rjvndm22fd6ibl9bgxnhzv14p03vhvmrqp5rc7sfvw9w";
      };
    });
  })
]
