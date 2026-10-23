#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
deps="$root/external/toolchain"
build="$root/external/.build/toolchain"
mkdir -p "$build" "$deps/bin"
if [ ! -f "$deps/newt0/src/newt_core/NewtObj.c" ]; then
    echo 'Missing external/toolchain/newt0; restore the pinned source in external/DEPENDENCIES.json.' >&2
    exit 1
fi
if [ ! -d "$build/tntk-src" ]; then
    cp -R "$deps/tntk" "$build/tntk-src"
    patch -s -p1 -d "$build/tntk-src" < "$deps/patches/tntk-auto-package.patch"
fi
cmake -S "$build/tntk-src" -B "$build/build" -DUSE_DCL=OFF -DFETCHCONTENT_SOURCE_DIR_NEWT0="$deps/newt0"
cmake --build "$build/build" -j4
cp "$build/build/tntk" "$deps/bin/tntk"
