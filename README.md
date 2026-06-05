# aws-boto3-template

A small, open-source boto3 template for controlling an AWS Auto Scaling Group
that backs GPU capacity. It gives you a clean starting point for checking ASG
status, starting GPU capacity, and stopping GPU capacity from a Python CLI.

## What It Does

- Reads AWS configuration from `.env`, standard AWS environment variables, an
  AWS profile, or the normal boto3 credential chain.
- Shows the configured GPU Auto Scaling Group status.
- Starts GPU capacity by setting `MinSize` and `DesiredCapacity`.
- Stops GPU capacity by setting `MinSize` and `DesiredCapacity` to `0`.
- Provides a `typer` CLI that can be installed as `aws-gpu-control`.

## Requirements

- Python 3.11+
- An AWS account with permission to read and update the target Auto Scaling
  Group
- `uv` for the simplest local workflow

Minimum IAM actions for the target ASG:

```json
{
  "Action": [
    "autoscaling:DescribeAutoScalingGroups",
    "autoscaling:UpdateAutoScalingGroup"
  ],
  "Effect": "Allow",
  "Resource": "*"
}
```

Scope the `Resource` as tightly as your AWS account and ASG naming strategy
allow before using this in production.

## Quick Start

Clone the repository and install dependencies:

```bash
git clone https://github.com/mirza-mohibul-hasan/aws-boto3-template.git
cd aws-boto3-template
uv sync
```

Create your local environment file:

```bash
cp .env.example .env
```

Then set the values for your account:

```dotenv
AWS_REGION=ap-southeast-1
GPU_ASG_NAME=my-gpu-auto-scaling-group
AWS_PROFILE=my-aws-profile
```

You can also leave `AWS_PROFILE` empty and use `aws configure`, instance roles,
or `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`.

## Usage

Run the CLI with `uv`:

```bash
uv run aws-gpu-control status
uv run aws-gpu-control start
uv run aws-gpu-control start --desired-capacity 2
uv run aws-gpu-control stop
```

You can also run the compatibility script:

```bash
uv run python scripts/gpu_control.py status
```

## Configuration

The app reads these variables:

| Variable | Required | Description |
| --- | --- | --- |
| `GPU_ASG_NAME` | Yes | Name of the Auto Scaling Group to control. |
| `AWS_REGION` or `AWS_DEFAULT_REGION` | Usually | AWS region for the ASG. Can also come from your AWS profile. |
| `AWS_PROFILE` or `AWS_DEFAULT_PROFILE` | No | AWS profile name to use. |
| `AWS_ACCESS_KEY_ID` | No | Optional static access key. Prefer profiles or IAM roles. |
| `AWS_SECRET_ACCESS_KEY` | No | Optional static secret key. Must be set with `AWS_ACCESS_KEY_ID`. |

Legacy environment variables are still supported for existing users:

- `DEVELOPMENT_GPU_ASG_NAME`
- `DEVELOPMENT_INFRASTRUCTURE_CONTROL_ACCESS_KEY_ID`
- `DEVELOPMENT_INFRASTRUCTURE_CONTROL_SECRET_ACCESS_KEY`

## Project Structure

```text
.
|-- app/
|   |-- cli.py
|   |-- core/
|   |   |-- aws_session.py
|   |   `-- config.py
|   `-- services/
|       `-- asg_service.py
|-- scripts/
|   `-- gpu_control.py
|-- main.py
|-- pyproject.toml
`-- README.md
```

## Development

Install and run locally:

```bash
uv sync
uv run python -m compileall app main.py scripts
```

Before opening a pull request, make sure:

- `.env` is not committed.
- The README usage still matches the CLI.
- AWS permissions are scoped to the smallest practical target.
- Commands that change ASG capacity were tested against a non-production ASG
  first.

## Commit Style

Use concise conventional commit messages:

```text
feat: add gpu asg control cli
fix: support standard aws credential chain
docs: document setup and usage
chore: prepare repository metadata
```

A good commit message for this cleanup would be:

```text
feat: prepare gpu asg boto3 template for open source use
```

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
