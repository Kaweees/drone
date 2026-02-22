{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python313
    uv
    gcc
    ffmpeg_4
    pkg-config
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${
      pkgs.lib.makeLibraryPath (
        with pkgs;
        [
          ffmpeg_4
          stdenv.cc.cc.lib
        ]
      )
    }:$LD_LIBRARY_PATH"
    export UV_PYTHON="${pkgs.python313}/bin/python3"
  '';
}
