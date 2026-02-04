# Editor Integration

Using Ty in your editor.

## VS Code

### Installation

1. Install "Ty" extension from marketplace
2. Open VS Code Settings (Cmd/Ctrl + ,)
3. Search for "Ty"

### Configuration

```json
{
    "ty.enable": true,
    "ty.checkOnSave": true,
    "ty.showDiagnostics": true,
    "ty.pythonVersion": "3.10"
}
```

### Features

- Real-time type checking
- Hover information
- Go to definition
- Find references
- Quick fixes
- Problem diagnostics

### Keybindings

```json
{
    "key": "cmd+shift+p",
    "command": "ty.checkFile"
}
```

## PyCharm

### Installation

1. Go to Settings → Plugins
2. Search for "Ty"
3. Install the plugin
4. Restart PyCharm

### Configuration

Settings → Tools → Python → Type Checker:

- Enable type checking
- Set Python version
- Configure inspection level

### Features

- On-the-fly type checking
- Code inspections
- Quick fixes
- Gutter icons for errors

## Vim/Neovim

### CoC integration

Install CoC and Ty language server:

```bash
:CocInstall coc-ty
```

Configure `coc-settings.json`:

```json
{
    "languageserver": {
        "ty": {
            "command": "ty-language-server",
            "args": ["--stdio"],
            "filetypes": ["python"]
        }
    }
}
```

### Vim-LSP

Add to your vim config:

```vim
" Register Ty as language server
```

## Emacs

### LSP Mode

Add to your Emacs config:

```elisp
(with-eval-after-load 'lsp-mode
  (lsp-register-client
   (make-lsp-client :new-connection (lsp-stdio-connection "ty-language-server")
                    :major-modes '(python-mode)
                    :priority 10)))
```

## Sublime Text

### LSP integration

1. Install LSP package: `Package Control: Install Package`
2. Install LSP-Ty
3. LSP will handle type checking

## Other editors

Ty provides a language server that works with:
- Visual Studio
- Atom
- Nova
- And other LSP-compatible editors

## Language Server Protocol

Run the language server directly:

```bash
ty --language-server --stdio
```

## Configuration in editor

### Enable/disable checking

Most editors allow toggling Ty:
- Command palette: "Toggle Ty"
- Settings: `ty.enable`

### Python version

Configure in editor settings:

```json
{
    "ty.pythonVersion": "3.10"
}
```

### Strict mode

Enable strict type checking:

```json
{
    "ty.strict": true
}
```

### Exclude paths

Exclude paths from checking:

```json
{
    "ty.exclude": ["tests/", "venv/"]
}
```

## Troubleshooting

### Server not starting

1. Check Ty is installed: `ty --version`
2. Restart editor
3. Check extension logs

### Wrong Python version

Ensure pyproject.toml has correct version:

```toml
[tool.ty]
python-version = "3.10"
```

### Slow checking

- Increase timeout in editor settings
- Exclude large directories
- Use lower diagnostic level

## More Information

For complete details, visit: https://docs.astral.sh/ty/editor-integration/
