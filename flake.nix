{
  description = "Decorator for marking AI functions";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        poetry2nix = inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
      in
      {
        packages = {
          dio = poetry2nix.mkPoetryApplication {
            packageName = "dio";
            projectDir = ./.;
            buildInputs = (
              with pkgs;
              [
                pkgs.ruff
              ]
            );
          };
          default = self.packages.${system}.dio;
        };

        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.python312
            pkgs.poetry
            pkgs.python312Packages.python-lsp-ruff
          ];
        };
      }
    );
}