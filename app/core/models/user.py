from pydantic import BaseModel, field_validator
from typing import Optional, List
import re
from core.tools import hash_password
from enum import Enum

class UserRole(str, Enum):
    """
        Classe représentant les rôles disponible pour un User
    """
    user = "user"
    admin = "admin"
    mentor = "mentor"
    webmaster = "webmaster"

class UserBase(BaseModel):
    """
        Classe de base d'une USER
    """
    username: str
    email: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v) <= 3:
            raise ValueError("Le pseudo doit avoir au minimum 3 caractères.")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, v):
            raise ValueError("L'adresse email saisie n'est pas valide.")
        return v

class UserCreate(UserBase):
    """
        Modèle uniquement à utiliser pour la création d'un nouvel utilisateur
    """
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) <= 3:
            raise ValueError("Le mot de passe doit faire au moins 3 caractères.")
        return hash_password(v)

    roles: List[UserRole] = [UserRole.user]

class UserOut(UserBase):
    """
        Le modèle qui permet de retourner les informations USER au front
    """
    id: str
    roles: list

    class Config:
        from_attributes = True

class User(UserBase):
    """
        Modèle pour les traitement côté serveur uniquement
    """
    id: Optional[str] = None
    password: str
    roles: List[UserRole] = [UserRole.user]
    token_session: Optional[str] = ""
    token_password_dt: Optional[float] = 0.0
    auth_two_factor: Optional[bool] = False
    failed_login_attempts: int = 0

    def is_admin(self) -> bool:
        return UserRole.admin in self.roles
