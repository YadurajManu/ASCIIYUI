#!/bin/bash
# Helper script to calculate SHA256 for Homebrew formula

VERSION=${1:-"1.0.0"}
REPO="YadurajManu/ASCIIYUI"

if [ "$VERSION" = "main" ]; then
  URL="https://github.com/${REPO}/archive/refs/heads/main.zip"
  echo "⚠️  Warning: Using main branch. Consider creating a release tag instead."
else
  URL="https://github.com/${REPO}/archive/refs/tags/v${VERSION}.tar.gz"
fi

echo "Calculating SHA256 for version: $VERSION"
echo "URL: $URL"
echo ""
SHA256=$(curl -sL "$URL" | shasum -a 256 | awk '{print $1}')
echo "SHA256: $SHA256"
echo ""
echo "Update Formula/asciicam.rb with:"
echo "  sha256 \"$SHA256\""
