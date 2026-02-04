# PyTorch Integration

Installing and using PyTorch with uv.

## Installing PyTorch

Install PyTorch with CPU support:

```bash
uv add torch torchvision torchaudio
```

## GPU support (CUDA)

For NVIDIA GPU support, install CUDA-enabled PyTorch:

```bash
uv add --index-url https://download.pytorch.org/whl/cu118 torch torchvision torchaudio
```

Replace `cu118` with your CUDA version:
- `cu118` - CUDA 11.8
- `cu121` - CUDA 12.1
- `cpu` - CPU only

## Project setup

Create a PyTorch project:

```bash
uv init --python 3.11
uv add torch torchvision torchaudio numpy matplotlib
```

## Basic usage

```python
import torch

# Check GPU availability
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Device: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")

# Create a tensor
x = torch.randn(3, 4)
print(x)
```

## In pyproject.toml

Specify PyTorch dependency:

```toml
[project]
dependencies = [
    "torch>=2.0.0",
    "torchvision>=0.15.0",
    "torchaudio>=2.0.0",
]
```

## Development dependencies

Add tools for development:

```bash
uv add --dev jupyter notebook tensorboard
```

## Running scripts

Execute PyTorch scripts:

```bash
uv run train.py
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/pytorch/
