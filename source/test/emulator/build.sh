#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
deps="$root/external/emulator"
build="$root/external/.build/emulator"
mkdir -p "$build"
if [ ! -d "$build/source" ]; then
    cp -R "$deps/source/Einstein" "$build/source"
    if ! grep -q 'UBX_PEN_COMMAND_FILE' "$build/source/Emulator/Screen/TFLScreenManager.cpp"; then
        patch -s -p1 -d "$build/source" < "$root/source/test/emulator/patches/pen-and-print-runtime.patch"
    fi
    patch -s -p1 -d "$build/source" < "$root/source/test/emulator/patches/isolated-runtime.patch"
fi
cmake -S "$build/source" -B "$build/build" \
    -DFETCHCONTENT_SOURCE_DIR_FLTK="$deps/deps/fltk" \
    -DFETCHCONTENT_SOURCE_DIR_GOOGLETEST="$deps/deps/googletest" \
    -DFETCHCONTENT_SOURCE_DIR_NEWT64="$root/external/toolchain/newt64"
cmake --build "$build/build" --target Einstein -j4
printf 'Built emulator: %s\n' "$build/build/Einstein.app"
