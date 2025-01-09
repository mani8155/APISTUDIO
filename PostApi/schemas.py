from pydantic import BaseModel
from typing import Dict


class CRUDSchema(BaseModel):
    data: Dict
