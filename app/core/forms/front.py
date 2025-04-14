from pydantic import BaseModel


class FormRegister(BaseModel):
    """
        Formulaire de création de compte - Front
    """
    username: str
    email: str
    password: str

class FormLogin(BaseModel):
    """
        Formulaire de connexion - Front
    """
    email: str
    password: str

class FormQueryResetPassword(BaseModel):
    """
        Formulaire de demande de réinitialisation de mot de passe - Front
    """
    email: str

class FormResetPassword(BaseModel):
    """
        Formulaire de réinitialisation de mot de passe - Front
    """
    email: str
    password: str
    token: str

class FormChangePassword(BaseModel):
    """
        Formulaire de modification du mot de passe - Front > Account > Security
    """
    current_password: str
    new_password: str