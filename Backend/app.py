from fastapi import FastAPI
import os # import lien
from fastapi.middleware.cors import CORSMiddleware # permet la communication avec d<autre langage
import snowflake.connector as sc 
import uvicorn  #Pour lancer le serveur
from dotenv import load_dotenv # pour upload les acces caches
from .Models import Medecins,medec
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
          
          




    

if __name__== "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000,workers=1)