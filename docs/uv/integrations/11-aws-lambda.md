# AWS Lambda Integration

Deploying Python applications to AWS Lambda with uv.

## Project setup

Create a Lambda project:

```bash
uv init my-lambda --python 3.12
cd my-lambda
uv add boto3 requests
```

## Basic Lambda handler

Create `src/handler.py`:

```python
import json

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from Lambda!'
        })
    }
```

## Creating deployment package

Build the Lambda package:

```bash
mkdir lambda_package
uv sync --frozen --no-dev
cp -r .venv/lib/python3.12/site-packages/* lambda_package/
cp src/handler.py lambda_package/
cd lambda_package
zip -r ../lambda_function.zip .
```

## Docker-based deployment

Use Docker for consistent builds:

```dockerfile
FROM ghcr.io/astral-sh/uv:latest as builder

COPY pyproject.toml uv.lock /app/
WORKDIR /app

RUN uv sync --frozen --no-dev

# Create deployment package
RUN mkdir /lambda && \
    cp -r .venv/lib/python*/site-packages/* /lambda/ && \
    cp src/handler.py /lambda/

FROM public.ecr.aws/lambda/python:3.12

COPY --from=builder /lambda ${LAMBDA_TASK_ROOT}

CMD ["handler.lambda_handler"]
```

## Deployment with AWS CLI

Deploy using AWS CLI:

```bash
aws lambda create-function \
  --function-name my-function \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT:role/lambda-role \
  --handler handler.lambda_handler \
  --zip-file fileb://lambda_function.zip
```

## Environment configuration

Set dependencies in `pyproject.toml`:

```toml
[project]
dependencies = [
    "boto3>=1.26.0",
    "requests>=2.28.0",
]
```

## Testing locally

Test with SAM (Serverless Application Model):

```bash
sam local invoke MyFunction
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/aws-lambda/
