# Policies

uv's versioning, support, and compatibility policies.

## Version numbering

uv follows semantic versioning: `MAJOR.MINOR.PATCH`

### MAJOR version
- Breaking changes to CLI or API
- Incompatible default behaviors
- Requires user migration

### MINOR version
- New features
- Backward compatible
- Non-disruptive changes

### PATCH version
- Bug fixes
- Performance improvements
- Security patches

## Backward compatibility

### Stability commitments

uv commits to:
- Stable command-line interface
- Consistent behavior across versions
- Reproducible builds
- Compatible lock file format

### Breaking changes

Breaking changes only in MAJOR versions:
- Prior deprecation period
- Clear migration guide
- Reasonable notice (6+ months)

## Python version support

### Supported versions

uv supports:
- Python 3.8+
- CPython
- PyPy (3.8+)
- Conda environments

### End of support

When Python versions reach end-of-life:
- Deprecation notice
- Continued support for 1 year
- Eventually removed

## Platform support

### Supported platforms

- **Linux** - x86_64, aarch64, ppc64le
- **macOS** - x86_64, aarch64 (Apple Silicon)
- **Windows** - x86_64, i686

### Community support

Community-supported platforms:
- Alpine Linux
- Custom architectures
- Embedded systems

### Tier 1 (fully supported)
- Linux x86_64
- macOS (Intel and Apple Silicon)
- Windows x86_64

### Tier 2 (best effort)
- Linux aarch64
- Other architectures
- Non-standard setups

## License

uv is dual licensed:

### MIT License
- Commercial use
- Modification
- Distribution
- Private use

### Apache License 2.0
- Alternative to MIT
- Explicit patent grant
- Liability limitations

Choose either license.

## Security policy

### Security releases

Security vulnerabilities:
- Addressed promptly
- Patch releases issued
- CVE assigned if applicable
- Advisories published

### Reporting vulnerabilities

Report to: security@astral.sh

### Disclosure timeline

- Vulnerability reported
- Initial response: 48 hours
- Fix development
- Patch release
- Public disclosure

## Release cycle

### Frequency

- New MINOR release: every 2-4 weeks
- PATCH releases: as needed
- MAJOR releases: planned, infrequent

### Release support

Each MAJOR version:
- Full support for 12 months
- Security support for 24 months
- Long-term stability guarantee

## Deprecation policy

### Deprecation timeline

1. **Announce** - Release notes mention deprecation
2. **Grace period** - 6+ months of support
3. **Removal** - Only in next MAJOR version

### Deprecation notices

- Clear error messages
- Migration guidance
- Documentation updates

## Compatibility promises

### Lock file format

- Forward compatible
- Backward compatible (last 2 versions)
- Clear migration path

### Configuration files

- Stable `pyproject.toml` support
- Backward compatible
- Deprecation warnings

### Command interface

- Stable flags and options
- Consistent behavior
- Documented changes

## Community and contributions

### Code of conduct

uv community follows:
- Respectful interaction
- Inclusive environment
- Collaborative spirit

### Contribution guidelines

- GitHub issues for feedback
- Pull requests welcome
- Documentation valued
- Testing required

## API stability

### Public API

Stable and documented:
- CLI interface
- Configuration schema
- Output formats

### Internal API

Not guaranteed stable:
- Subject to change
- Not for production use
- Documented requirements

## Long-term support

### Support commitment

- 12 months full support
- 24 months security support
- Regular updates
- Community assistance

### Upgrade path

- Clear upgrade guides
- Backward compatibility
- Gradual transitions
- Zero-downtime possible

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/policies/
