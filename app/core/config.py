import os

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, field_validator, model_validator

load_dotenv()


class AWSConfig(BaseModel):
    region: str | None = None
    profile_name: str | None = None
    access_key_id: str | None = None
    secret_access_key: str | None = None
    gpu_asg_name: str

    @field_validator("*", mode="before")
    @classmethod
    def blank_strings_to_none(cls, value):
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @model_validator(mode="after")
    def validate_static_credentials(self):
        has_access_key = bool(self.access_key_id)
        has_secret_key = bool(self.secret_access_key)

        if has_access_key != has_secret_key:
            raise ValueError(
                "set both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, "
                "or leave both empty to use the default AWS credential chain"
            )

        return self


def get_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value and value.strip():
            return value

    return None


def get_aws_config() -> AWSConfig:
    try:
        return AWSConfig(
            region=get_env("AWS_REGION", "AWS_DEFAULT_REGION"),
            profile_name=get_env("AWS_PROFILE", "AWS_DEFAULT_PROFILE"),
            access_key_id=get_env(
                "AWS_ACCESS_KEY_ID",
                "DEVELOPMENT_INFRASTRUCTURE_CONTROL_ACCESS_KEY_ID",
            ),
            secret_access_key=get_env(
                "AWS_SECRET_ACCESS_KEY",
                "DEVELOPMENT_INFRASTRUCTURE_CONTROL_SECRET_ACCESS_KEY",
            ),
            gpu_asg_name=get_env("GPU_ASG_NAME", "DEVELOPMENT_GPU_ASG_NAME"),
        )
    except ValidationError as exc:
        raise RuntimeError(
            "Missing or invalid AWS configuration. Set GPU_ASG_NAME and "
            "configure AWS credentials with AWS_PROFILE, the AWS CLI, an IAM "
            "role, or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY."
        ) from exc
