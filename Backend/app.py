from fastapi import FastAPI
import os # import lien
from fastapi.middleware.cors import CORSMiddleware # permet la communication avec d<autre langage
import snowflake.connector as sc 
import uvicorn  #Pour lancer le serveur
from dotenv import load_dotenv # pour upload les acces caches
from .Models import Medecins,medec,Patient,Patien,Patie
from .Function import password_hash,password_verify

load_dotenv()
app= FastAPI()


app.add_middleware ( CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

Connect= sc.Connect(
    user= os.getenv("snowflake_user"),
    password=os.getenv("snowflake_password"),
    account=os.getenv("snowflake_account"),
    database=os.getenv("snowflake_database"),

)

cursor=Connect.cursor() # pour manager toutes les function lies a la base de donnes

@app.post("/Inscription_Medecin")


async def Inscript_medecin(A:Medecins):
    sql = "SELECT * FROM MEDSYNCH.MEDSYNCH.MEDECINS where Email=%s"
    params=[A.Email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    

    if resultat : 
        return { "message":"Email exixte deja"}
    
    else :
       
       y= password_hash(A.Mot_de_passe)
       sql =""" 
       
       INSERT INTO  MEDSYNCH.MEDSYNCH.MEDECINS(Nom,Prenom,Mot_de_passe,Nom_hopital,Tel,Matricule,Email)
       values (%s,%s,%s,%s,%s,%s,%s)
       
       """

       params=[A.Nom,A.Prenom,y,A.Nom_Hopital,A.Tel,A.Matricule,A.Email]
       x=cursor.execute(sql,params)


       return {"message":"Medecin Ajoute avec succes"}
    

@app.post("/Connect_Medecin")

async def connect_medecin(E:medec):
    sql= "SELECT * from  MEDSYNCH.MEDSYNCH.MEDECINS  where Email=%s"
    params=[E.Email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
  

    if resultat :
      x= password_verify(E.Mot_de_passe,resultat[3])

      if x :
          r={
              "medecin_id":resultat[0],
              "nom":resultat[1],
              "matricule":resultat[5]
          }
          
          return{'message':r}
      else:
          return{'message':'mot de passe incorrect'}
      
    else:
        return{'message':'email introuvable'}
    

@app.post("/Inscription_Patient")
          
async def Inscript_patient(A:Patient):

    sql = "SELECT * FROM MEDSYNCH.MEDSYNCH.PATIENTS where Email=%s"
    params=[A.Email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    

    if resultat : 
        return { "message":f"{A.Email} exixte deja"}
    
    else :
       
       M = password_hash(A.Mdp)
       print(M)

       sql =""" 
       
       INSERT INTO  MEDSYNCH.MEDSYNCH.PATIENTS (Nom,Prenom,Date_Naissance,Genre,Parents_Ident,Adresse,Email,NAS,Mot_de_Passe)
       values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
       
       """

       params=[A.Nom,A.Prenom,A.Date_Naissance,A.Genre,A.Identifiant_Parent,A.Adresse,A.Email,A.NAS,M]
       x=cursor.execute(sql,params)

       return {"message":f"{A.Nom} Ajoute avec succes"}




@app.post("/Connection_Patient")

async def connect_patient(E:Patien):
    sql= "SELECT * from  MEDSYNCH.MEDSYNCH.PATIENTS  where Email=%s"
    params=[E.Email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    
  

    if resultat :
      x= password_verify(E.Mdp,resultat[9])
   

      if x :
          s={
              "patient_id":resultat[0],
              "nom":resultat[1],
              "NAS":resultat[8]
          }
          
          return{'message':s}
      else:
          return{'message':'mot de passe incorrect'}
      
    else:
        return{'message':'email introuvable'}

# @app.put("/ModifInfo_Patient")

# async def  modifInfo_patient(P:Patie):
#     update="SELECT * FROM  MEDSYNCH.MEDSYNCH.PATIENTS WHERE patient_id=%s"

#     params=[P.Email]
#     cursor.execute(update,params)
#     resultat=cursor.fetchone()

#     if resultat:
#         update=""" 
#         UPDATE  MEDSYNCH.MEDSYNCH.PATIENTS SET (Adresse,Email,Mdp)where patient_id=%s 
#         values (%s,%s,%s)
#         """ 
#         T= password_hash(P.Mdp)
#         params=[P.Adresse,P.Email,P.Mdp,T]
#         x=cursor.execute(update,params)
#         return {"message":"Les information du patient ont été Modifié avec succes"}
#     else:
#          return  {"message":"Patient introuvable"}

    

if __name__== "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000,workers=1)