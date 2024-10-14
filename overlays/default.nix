[
  (self: super: {
    poetry = super.poetry.overrideAttrs (oldAttrs: rec {
      version = "1.8.2"; # Define version directly here

      src = super.fetchFromGitHub {
        owner = "python-poetry";
        repo = "poetry";
        rev = "1.8.2"; # Use the same version here
        sha256 = "d41d8cd98f00b204e9800998ecf8427e"; # Replace with actual sha256
      };
    });
  })
]
