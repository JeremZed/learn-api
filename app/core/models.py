from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

ROLE_USER = 'user'
ROLE_ADMIN = 'admin'
ROLE_NONE = 'none'

class User(BaseModel):
    """
        Classe représentant l'entité User
    """
    id : Optional[str] = None
    username : str
    email: str
    name: str
    role: Optional[str] = ROLE_NONE
    password: Optional[str] = ""
    token_password_dt: Optional[float] = 0.0



class UserCurrent(BaseModel):
    """
        Modèle représenant les informations d'un utilisateur connecté
    """

    username : str
    email: str
    name: str
    role: Optional[str] = ROLE_NONE

    def is_admin(self):
        return self.role == ROLE_ADMIN


