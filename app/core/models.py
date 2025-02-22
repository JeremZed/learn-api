from pydantic import BaseModel

class User(BaseModel):
    """
        Modèle représentant les informations d'un utilisateur
    """
    username: str
    email: str
    password: str
    name: str

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
