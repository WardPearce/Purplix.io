from os import path

from aiobotocore.session import get_session
from app.env import SETTINGS


def format_path(*paths: str) -> str:
    return path.join(SETTINGS.s3.folder, *paths)


def s3_create_client():
    session = get_session()
    return session.create_client(
        service_name="s3",
        region_name=SETTINGS.s3.region_name,
        aws_secret_access_key=SETTINGS.s3.secret_access_key,
        aws_access_key_id=SETTINGS.s3.access_key_id,
        endpoint_url=SETTINGS.s3.endpoint_url,
    )
