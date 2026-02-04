# Authentication

Managing authentication with uv.

## What is authentication?

Authentication is needed to access private package indexes and securely download packages from protected sources.

## Using credentials

Configure credentials in multiple ways:

### Environment variables

```bash
export UV_INDEX_AUTH=token
export UV_INDEX_USERNAME=myuser
export UV_INDEX_PASSWORD=mypass
```

### URL-embedded credentials

Include credentials directly in index URL:

```toml
[tool.uv.index]
indexes = [
    { url = "https://token@private.example.com/simple/" },
]
```

### Keyring authentication

uv can use system keyring for storing credentials:

```bash
uv add mypackage --index-url https://private.example.com/simple/
# Will prompt for credentials and store securely
```

## GitHub token authentication

For GitHub Packages:

```bash
export UV_INDEX_AUTH=mytoken
uv add mypackage --index-url https://npm.pkg.github.com/
```

## Azure artifact feeds

For Azure DevOps:

```bash
uv add mypackage --index-url https://username:password@dev.azure.com/...
```

## Security best practices

- Use tokens instead of passwords
- Store credentials in environment variables
- Don't commit credentials to version control
- Use `.gitignore` for sensitive files
- Rotate tokens regularly

## More Information

For complete details, visit: https://docs.astral.sh/uv/concepts/authentication/
