from datetime import datetime
from typing import Optional

from app.env import SETTINGS
from bson import ObjectId
from models.customs import CustomJsonEncoder, IvField
from pydantic import BaseModel, Field


class PublicKeyModel(BaseModel):
    public_key: str = Field(
        ..., max_length=44, description="ed25519 public key, base64 encoded"
    )


class CanaryEd25519Model(IvField, PublicKeyModel):
    cipher_text: str = Field(
        ...,
        max_length=240,
        description="ed25519 private key, encrypted with keychain, base64 encoded",
    )


class __CanarySharedModel(CustomJsonEncoder):
    domain: str = Field(
        ...,
        regex=r"(?i)^((?!(?:www|www\d+)\.)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:[a-zA-Z]{2,})$",
    )
    about: str = Field(..., max_length=500)
    signature: str = Field(..., max_length=128)
    algorithms: str = Field(
        "XCHACHA20_POLY1305+ED25519+BLAKE2b",
        max_length=120,
        description="Algorithms used for canary",
    )


class CreateCanaryModel(__CanarySharedModel):
    keypair: CanaryEd25519Model


class PublicCanaryModel(__CanarySharedModel):
    id: ObjectId = Field(..., alias="_id")
    logo: Optional[str] = None
    user_id: ObjectId
    created: datetime
    keypair: PublicKeyModel

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if self.logo:
            self.logo = f"{SETTINGS.s3.download_url}/canary/logos/{self.logo}"


class DomainVerification(BaseModel):
    completed: bool = False
    code: str
    code_prefixed: str = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.code_prefixed = f"{SETTINGS.canary.domain_verify.prefix}{self.code}"


class CanaryModel(PublicCanaryModel):
    domain_verification: DomainVerification
    keypair: CanaryEd25519Model
