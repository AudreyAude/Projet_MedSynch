from pydantic import BaseModel


class Medecins(BaseModel) :
    Nom:str
    Prenom:str
    Mot_de_passe:str
    Nom_Hopital:str
    Tel:str
    Matricule:str
    Email:str