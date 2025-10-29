#!/bin/bash
set -e

echo "🛠 Installing build dependencies..."
sudo apt update
sudo apt install -y build-essential cmake qtbase5-dev libraw-dev libtiff-dev git

echo "📦 Cloning hdrmerge..."
git clone https://github.com/jcelaya/hdrmerge.git
cd hdrmerge

echo "🏗 Building hdrmerge..."
mkdir -p build && cd build
#cmake .. -DCMAKE_BUILD_TYPE=Release
cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_ALGLIB=OFF
make -j$(nproc)

echo "🚀 Installing to /usr/local/bin (requires sudo)..."
sudo cp hdrmerge /usr/local/bin/hdrmerge-cli

echo "✅ Done. Try it with:"
echo "   hdrmerge-cli --align --output=test.exr your-brackets-1.dng ..."
