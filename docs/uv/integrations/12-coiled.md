# Coiled Integration

Using uv with Coiled for distributed computing.

## What is Coiled?

Coiled is a platform for running Dask distributed computing in the cloud. It integrates with Python environments for easy scaling.

## Project setup

Create a Dask + Coiled project:

```bash
uv init my-dask-app --python 3.11
cd my-dask-app
uv add dask dask-distributed coiled
```

## Basic Dask example

Create `src/analysis.py`:

```python
import dask.dataframe as dd
import coiled

@coiled.function
def process_data():
    # Load data with Dask
    df = dd.read_csv("s3://my-bucket/data/*.csv")
    
    # Perform computation
    result = df.groupby("category").value.mean().compute()
    
    return result

if __name__ == "__main__":
    result = process_data()
    print(result)
```

## Running on Coiled

Deploy and run on Coiled cloud:

```bash
uv run python src/analysis.py
```

## Coiled configuration

Configure in `pyproject.toml`:

```toml
[tool.coiled]
name = "my-dask-app"
python = "3.11"
worker-cpu = 2
worker-memory = "8GB"
```

## Environment setup

Ensure Coiled credentials are configured:

```bash
coiled login
```

## Scaling computations

Scale your Dask computations:

```python
import dask.dataframe as dd
from dask.distributed import Client
import coiled

# Create a Coiled cluster
cluster = coiled.Cluster(n_workers=10)
client = Client(cluster)

# Your computation automatically uses the cluster
df = dd.read_csv("s3://bucket/data/*.csv")
result = df.groupby("id").value.sum().compute()
```

## Dependencies management

All dependencies in `pyproject.toml` are automatically installed in workers.

## Monitoring

Monitor jobs on the Coiled dashboard:

```bash
coiled jobs list
coiled jobs logs <job-id>
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/coiled/
