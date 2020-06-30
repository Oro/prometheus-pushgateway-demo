{ pkgs ? import <nixpkgs> { } }:

with pkgs;
let
  nixpkgs-tars = "https://github.com/NixOS/nixpkgs/archive/";
  pr91387 = import (fetchTarball
    "${nixpkgs-tars}3c6bd1664833dc460afa1593f6b5350c41861492.tar.gz") {};
in mkShell {
  buildInputs = [
    (python3.withPackages (ps: [ ps.requests ps.prometheus_client ]))
    kube3d
    kubectl
    pr91387.kubernetes-helm
  ];
}
