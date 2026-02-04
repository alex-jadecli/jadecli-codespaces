# Installer Options

Reference for uv installer customization.

## Installation methods

### Standalone installer

Download and run the installer script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Specific version

```bash
curl -LsSf https://astral.sh/uv/0.9.28/install.sh | sh
```

### Inspect before installing

```bash
curl -LsSf https://astral.sh/uv/install.sh | less
```

## Installer environment variables

### UV_INSTALL_DIR
Custom installation directory:

```bash
UV_INSTALL_DIR=$HOME/.bin bash -c '$(curl -LsSf https://astral.sh/uv/install.sh | sh)'
```

Default: `$HOME/.local/bin`

### UV_UPDATE_AVAILABLE_MSG
Show update availability message:

```bash
export UV_UPDATE_AVAILABLE_MSG=1
```

### UV_NO_MODIFY_PATH
Don't modify shell profiles:

```bash
export UV_NO_MODIFY_PATH=1
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Shell configuration

After installation, add uv to your shell:

### Bash
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Zsh
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

### Fish
```bash
set -Ua fish_user_paths $HOME/.local/bin
```

## Self-update

Update uv to latest version:

```bash
uv self update
```

Disable self-updates:

```bash
export UV_NO_MODIFY_PATH=1
```

## Package manager installation

### Homebrew
```bash
brew install uv
```

### MacPorts
```bash
sudo port install uv
```

### WinGet
```bash
winget install --id=astral-sh.uv -e
```

### Scoop
```bash
scoop install main/uv
```

### Cargo
```bash
cargo install --locked uv
```

### PyPI/pipx
```bash
pipx install uv
```

## Verification

Verify installation:

```bash
uv --version
```

Check installation location:

```bash
which uv
```

## Uninstallation

### Standalone installer

Remove binaries:

```bash
rm ~/.local/bin/uv ~/.local/bin/uvx
```

Clean up data:

```bash
uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"
```

### Package manager

Use package manager to uninstall:

```bash
brew uninstall uv          # Homebrew
winget uninstall astral-sh.uv  # WinGet
pipx uninstall uv          # pipx
```

## Troubleshooting

### Command not found

Add to PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Permission denied

Fix permissions:

```bash
chmod +x ~/.local/bin/uv
chmod +x ~/.local/bin/uvx
```

### Shell integration

Restart shell or source profile:

```bash
source ~/.bashrc      # Bash
source ~/.zshrc       # Zsh
exec fish            # Fish
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/installer-options/
