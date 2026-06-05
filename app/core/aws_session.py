import boto3

from app.core.config import get_aws_config


def get_boto3_session() -> boto3.Session:
    """
    Return a boto3 session using either explicit env credentials or AWS defaults.
    """
    config = get_aws_config()
    session_options = {
        "region_name": config.region,
    }

    if config.access_key_id and config.secret_access_key:
        session_options["aws_access_key_id"] = config.access_key_id
        session_options["aws_secret_access_key"] = config.secret_access_key
    elif config.profile_name:
        session_options["profile_name"] = config.profile_name

    return boto3.Session(
        **{key: value for key, value in session_options.items() if value}
    )
