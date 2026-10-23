#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
deps="$root/external/toolchain"
build="$root/external/.build/toolchain"
mkdir -p "$build" "$deps/bin"
if [ ! -f "$deps/newt0/src/newt_core/NewtObj.c" ]; then
    echo 'Missing external/toolchain/newt0; follow external/README.md.' >&2
    exit 1
fi
if [ ! -d "$build/tntk-src" ]; then
    cp -R "$deps/tntk" "$build/tntk-src"
    patch -s -p1 -d "$build/tntk-src" < "$root/source/main/tools/patches/tntk-auto-package.patch"
fi
if [ ! -d "$build/newt0-src" ]; then
    cp -R "$deps/newt0" "$build/newt0-src"
    if ! grep -q 'uint32_t cp;' "$build/newt0-src/src/newt_core/NewtIconv.c"; then
        patch -s -p1 -d "$build/newt0-src" < "$root/source/main/tools/patches/newt0-utf8.patch"
    fi
fi
cmake -S "$build/tntk-src" -B "$build/build" -DUSE_DCL=OFF -DFETCHCONTENT_SOURCE_DIR_NEWT0="$build/newt0-src"
cmake --build "$build/build" -j4
cp "$build/build/tntk" "$deps/bin/tntk"
mkdir -p "$deps/platform"
cp "$deps/tntk/examples/native/Newton 2.1" "$deps/platform/Newton 2.1"
