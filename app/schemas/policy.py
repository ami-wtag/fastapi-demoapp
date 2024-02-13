from pydantic import BaseModel, UUID4
from typing import Optional

from app.schemas.base import AppBaseModel


class CasbinRolePolicy(BaseModel):
    id: int
    ptype: str = 'p'
    v0: str
    v1: str
    v2: str
    v3: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "330000",
                    "ptype": "p",
                    "v0": "admin",
                    "v1": "Organization Name",
                    "v2": "^/api/...",
                    "v3": "(GET|POST|PUT|DELETE)"
                }
            ]
        }
    }