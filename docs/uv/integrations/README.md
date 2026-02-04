# uv Integrations

Complete guides for integrating uv with other tools and platforms.

## Integration Guides

### Development Tools
- [Docker](./01-docker.md) - Using uv in Docker images
- [Jupyter](./02-jupyter.md) - Using uv with Jupyter notebooks
- [marimo](./03-marimo.md) - Using uv with marimo notebooks
- [Pre-commit](./06-pre-commit.md) - Git pre-commit hooks with uv

### CI/CD Platforms
- [GitHub Actions](./04-github-actions.md) - GitHub Actions workflows
- [GitLab CI/CD](./05-gitlab-cicd.md) - GitLab CI/CD pipelines

### Package Management
- [Alternative Indexes](./09-alternative-indexes.md) - Using custom package indexes
- [Dependency Bots](./10-dependency-bots.md) - Dependabot and Renovate integration

### Web Frameworks
- [FastAPI](./08-fastapi.md) - Building FastAPI applications

### Machine Learning
- [PyTorch](./07-pytorch.md) - Installing and using PyTorch
- [Coiled](./12-coiled.md) - Distributed computing with Dask and Coiled

### Cloud Platforms
- [AWS Lambda](./11-aws-lambda.md) - Deploying to AWS Lambda

## Quick Integration Checklist

- [ ] Docker: Use official uv image for builds
- [ ] GitHub Actions: Use `astral-sh/setup-uv@v1`
- [ ] Pre-commit: Configure uv tools as local hooks
- [ ] CI/CD: Cache dependencies with `uv.lock`
- [ ] Private indexes: Configure authentication
- [ ] Cloud: Use Docker for consistent deployments

## Official Documentation

For more information, visit: https://docs.astral.sh/uv/guides/
