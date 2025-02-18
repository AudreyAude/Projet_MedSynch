from pydantic import BaseModel


class Medecins(BaseModel) :
    Nom:str
    Prenom:str
    Mot_de_passe:str
    Nom_Hopital:str
    Tel:str
    Matricule:str
    Email:str




class medec(BaseModel):
    Email:str
    Mot_de_passe:str



class Patient(BaseModel):
    Nom:str
    Prenom:str
    Date_Naissance:str
    Genre:str
    Identifiant_Parent:str
    Adresse:str
    Email:str
    NAS:str
    Mdp:str



class Patien(BaseModel):
    Email:str
    Mdp:str


class Patie(BaseModel):
    Adresse:str
    Email:str
    Mdp:str