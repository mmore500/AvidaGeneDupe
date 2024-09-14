{ pkgs }: {
    deps = [
      pkgs.nano
      pkgs.unzip
      pkgs.vim
      pkgs.pandoc
      pkgs.texlive.combined.scheme-full
      pkgs.python39Packages.pip
      pkgs.nodejs
      pkgs.editorconfig-checker
      pkgs.python39Packages.editorconfig
      pkgs.bibtex-tidy
      pkgs.cowsay
    ];
}
