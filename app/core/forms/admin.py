from pydantic import BaseModel
from typing import Optional
from app.core.models import ROLE_NONE


class FormRegister(BaseModel):
    """
        Formulaire de création de compte - Admin
    """
    username: str
    email: str
    password: str
    name: str
    role: Optional[str] = ROLE_NONE