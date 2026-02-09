from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class AWSConfig(BaseModel):
    region: str
    access_key_id: str
    secret_access_key: str
    gpu_asg_name: str


def get_aws_config() -> AWSConfig:

    return AWSConfig(
        region=os.getenv("AWS_REGION"),
        access_key_id=os.getenv(
            "DEVELOPMENT_INFRASTRUCTURE_CONTROL_ACCESS_KEY_ID"),
        secret_access_key=os.getenv(
            "DEVELOPMENT_INFRASTRUCTURE_CONTROL_SECRET_ACCESS_KEY"),
        gpu_asg_name=os.getenv("DEVELOPMENT_GPU_ASG_NAME"),
    )
