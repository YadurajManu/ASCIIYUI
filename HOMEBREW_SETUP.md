# 🍺 Homebrew Setup Guide

This guide explains how to set up Homebrew distribution for AsciiCam.

## Prerequisites

1. A GitHub account (YaduEnc)
2. Homebrew installed on your Mac
3. Git configured

## Step 1: Create the Homebrew Tap Repository

1. Go to GitHub and create a new repository named `homebrew-tap`
   - Repository name: `homebrew-tap`
   - Description: "Homebrew tap for YaduEnc projects"
   - Make it **Public** (required for Homebrew taps)
   - **Do NOT** initialize with README, .gitignore, or license

2. Clone the repository locally:
```bash
git clone https://github.com/YaduEnc/homebrew-tap.git
cd homebrew-tap
```

## Step 2: Add the Formula

1. Create a `Formula` directory:
```bash
mkdir -p Formula
```

2. Copy the formula file from this repository:
```bash
cp /path/to/AsciiCam/Formula/asciicam.rb Formula/asciicam.rb
```

Or create it manually with the content from `Formula/asciicam.rb`

3. Update the SHA256 hash:
   - First, create a release tag in the ASCIICam repository:
   ```bash
   cd /path/to/AsciiCam
   git tag v1.0.0
   git push origin v1.0.0
   ```
   
   - Then download the source archive and calculate SHA256:
   ```bash
   curl -L https://github.com/YaduEnc/ASCIICam/archive/refs/tags/v1.0.0.tar.gz | shasum -a 256
   ```
   
   - Update the `sha256` line in `Formula/asciicam.rb` with the result

4. Commit and push:
```bash
git add Formula/asciicam.rb
git commit -m "Add asciicam formula"
git push origin main
```

## Step 3: Test the Installation

Users can now install AsciiCam via Homebrew:

```bash
brew tap YaduEnc/homebrew-tap
brew install asciicam
```

## Updating the Formula

When you release a new version:

1. Update the version in `Formula/asciicam.rb`
2. Create a new git tag in the ASCIICam repository
3. Calculate the new SHA256 hash:
   ```bash
   curl -L https://github.com/YaduEnc/ASCIICam/archive/refs/tags/v1.0.1.tar.gz | shasum -a 256
   ```
4. Update the formula with the new version and SHA256
5. Commit and push to homebrew-tap

## Alternative: Using GitHub Releases

For better versioning, you can use GitHub releases instead of tags:

1. Create a release on GitHub (releases page → "Create a new release")
2. Upload a source tarball or use the auto-generated one
3. Update the formula URL to point to the release:
   ```ruby
   url "https://github.com/YaduEnc/ASCIICam/archive/v1.0.0.tar.gz"
   ```

## Troubleshooting

- **Formula not found**: Make sure the tap repository is public
- **SHA256 mismatch**: Recalculate the hash for the correct archive URL
- **Installation fails**: Check that all dependencies are available via Homebrew

## Resources

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Homebrew Python Guide](https://docs.brew.sh/Python-for-Formula-Authors)
