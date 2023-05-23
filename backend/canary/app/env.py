import secrets
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, BaseSettings, Field


class MongoDB(BaseModel):
    host: str = "localhost"
    port: int = 27017
    collection: str = "canary"


class ProxiedUrls(BaseModel):
    frontend: AnyHttpUrl = AnyHttpUrl(url="localhost", scheme="http")
    backend: AnyHttpUrl = AnyHttpUrl(url="localhost/api", scheme="http")


class S3(BaseModel):
    region_name: str
    secret_access_key: str
    access_key_id: str
    bucket: str
    folder: str = "canary"
    download_url: str
    endpoint_url: Optional[str] = None


class OpenAPI(BaseModel):
    title: str = "canary"
    version: str = "0.0.1"


class Redis(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0


class mCaptcha(BaseModel):
    verify_url: str
    site_key: str
    account_secret: str


class Documents(BaseModel):
    max_amount: int = 3
    max_size: int = 5243000
    allowed_extensions: List[str] = [
        "pdf",
        "html",
        "png",
        "jpeg",
        "jpg",
        "mp4",
        "mp3",
        "gif",
        "7z",
    ]


class Jwt(BaseModel):
    secret: str = Field(default=secrets.token_urlsafe(32), min_length=32)
    expire_days: int = 30


class DomainVerify(BaseModel):
    prefix: str = "canarystat.us__verify="
    timeout: int = 20


class Proxycheck(BaseModel):
    api_key: Optional[str] = None
    url: str = "https://proxycheck.io/v2/"


class Settings(BaseSettings):
    mongo: MongoDB = MongoDB()
    redis: Redis = Redis()
    proxy_urls: ProxiedUrls = ProxiedUrls()
    open_api: OpenAPI = OpenAPI()
    mcaptcha: Optional[mCaptcha] = None
    documents: Documents = Documents()
    site_name = "canarystat.us"
    domain_verify: DomainVerify = DomainVerify()
    proxy_check: Optional[Proxycheck] = None

    jwt: Jwt = Jwt()
    csrf_secret: str = Field(default=secrets.token_urlsafe(32), min_length=32)

    class Config:
        env_prefix = "canary_"


SETTINGS = Settings()  # type: ignore
