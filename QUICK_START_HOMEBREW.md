# 🚀 Quick Start: Setting Up Homebrew Distribution

## TL;DR - Quick Setup

1. **Create the tap repository on GitHub:**
   - Go to https://github.com/new
   - Repository name: `homebrew-tap`
   - Make it **Public**
   - Create repository (no README/gitignore)

2. **Clone and setup:**
```bash
git clone https://github.com/YaduEnc/homebrew-tap.git
cd homebrew-tap
mkdir -p Formula
```

3. **Copy the formula:**
```bash
# Copy Formula/asciicam.rb from this repo to homebrew-tap/Formula/
cp /path/to/AsciiCam/Formula/asciicam.rb Formula/asciicam.rb
```

4. **Create a release tag (if not already done):**
```bash
# From the AsciiCam directory:
git tag v1.0.0
git push origin v1.0.0
```

5. **Calculate SHA256 and update formula:**
```bash
# From the AsciiCam directory:
./scripts/calculate_sha256.sh 1.0.0
```

6. **Update the sha256 line in Formula/asciicam.rb, then:**
```bash
cd homebrew-tap
git add Formula/asciicam.rb
git commit -m "Add asciicam formula"
git push origin main
```

7. **Test installation:**
```bash
brew tap YaduEnc/homebrew-tap
brew install asciicam
asciicam
```

## For Future Updates

When releasing a new version:

1. Tag the release in ASCIICam repo:
```bash
git tag v1.0.1
git push origin v1.0.1
```

2. Calculate new SHA256:
```bash
./scripts/calculate_sha256.sh 1.0.1
```

3. Update `Formula/asciicam.rb`:
   - Update `url` to point to the new tag: `v1.0.1.tar.gz`
   - Update `sha256` with the new hash

4. Commit and push to homebrew-tap

## Formula File Location

The formula file is at: `Formula/asciicam.rb`

For detailed instructions, see `HOMEBREW_SETUP.md`
