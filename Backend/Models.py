from pydantic import BaseModel


class Medecins(BaseModel) :
    Nom:str
    Prenom:str
    Mot_de_passe:str
    Nom_Hopital:str
    Tel:str
    Matricule:str
    Email:str
    Image:str




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
    Image:str



class Patien(BaseModel):
    Email:str
    Mdp:str



class Modif_Pati(BaseModel):
    Adresse:str
    Email:str
    Id_Patient:str

class MedecinModif(BaseModel):
    Nom:str
    Prenom:str
    Date_Naissance:str
    Genre:str
    Identifiant_Parent:str
    Adresse:str
    Email:str
    NAS:str

class PatientImage(BaseModel):
    Email:str
    Image:str

class MedecinImage(BaseModel):
    Email:str
    Image:str

