import boto3
from app.core.config import get_aws_config


def get_boto3_session() -> boto3.Session:
    """
    Returns a boto3 session with the credentials from the environment variables.
    """
    config = get_aws_config()
    return boto3.Session(
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        region_name=config.region,
    )
