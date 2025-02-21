import bcrypt
import json

def clean_item(document: dict) -> dict:
    """
        Permet de retourner un item mongodb sans ObjectId qui occasionne une erreur dans la sérialisation
    """

    if document is None:
        return document

    document["id"] = str(document["_id"])
    del document["_id"]

    return document

def clean_items(documents: list) -> list:
    """
        Permet de retourner une liste d'items mongodb sans ObjectId qui occasionne une erreur dans la sérialisation
    """
    for doc in documents:
        if "_id" in doc:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
    return documents

def hash_password(password: str) -> str:
    """
        Permet de hasher les mots de passe
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')  # Retourne le hachage (qui inclut le sel)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
        Permet de verifier le hash du mot de passe
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
