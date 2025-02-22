from pydantic import BaseModel

ROLE_USER = 'user'
ROLE_ADMIN = 'admin'
ROLE_NONE = 'none'

class UserCreate(BaseModel):
    """
        Modèle représentant les informations d'un utilisateur
    """
    username: str
    email: str
    password: str
    name: str

class UserCurrent(BaseModel):
    """
        Modèle représenant les informations d'un utilisateur connecté
    """

    username : str
    email: str
    name: str
    role: str

class Credential(BaseModel):
    """
        Modèle représentant les informations de connexion
    """
    email: str
    password: str

class QueryResetPassword(BaseModel):
    """
        Modèle représentant la demande de réinitialisation de mot de passe
    """
    email: str

class ResetPassword(BaseModel):
    """
        Modèle représentant la réinitialisation de mot de passe
    """
    email: str
    password: str
    token: str
