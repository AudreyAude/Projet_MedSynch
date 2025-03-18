from fastapi import FastAPI
import os # import lien
from fastapi.middleware.cors import CORSMiddleware # permet la communication avec d'autre langage
import snowflake.connector as sc 
import uvicorn  #Pour lancer le serveur
from dotenv import load_dotenv # pour upload les acces caches
from .Models import Medecins,medec,Patient,Patien,Modif_Pati,MedecinModif,PatientImage,MedecinImage
from .Function import password_hash,password_verify,extractFeatures_bd,decode,face_detetion
from flask import Flask, request, jsonify

app = Flask(__name__)

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
    authenticator = "externalbrowser",
    role = "ACCOUNTADMIN",
    warehouse = "COMPUTE_WH"

    )  

cursor=Connect.cursor() # pour manager toutes les functions lies a la base de donnes

@app.post("/Inscription_Medecin")

async def Inscript_medecin(A:Medecins):
    print(A)
    sql = "SELECT * FROM MEDSYNCH.MEDSYNCH.MEDECINS where Email=%s"
    params=[A.Email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    

    if resultat : 
        return { "message":"Email exixte deja"}
    
    else :
       
       y= password_hash(A.Mot_de_passe)
       sql =""" 
       
       INSERT INTO  MEDSYNCH.MEDSYNCH.MEDECINS(Nom,Prenom,Mot_de_passe,Nom_hopital,Tel,Matricule,Email,Image)
       values (%s,%s,%s,%s,%s,%s,%s,%s)
       
       """

       params=[A.Nom,A.Prenom,y,A.Nom_Hopital,A.Tel,A.Matricule,A.Email,A.Image]
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
       
       INSERT INTO  MEDSYNCH.MEDSYNCH.PATIENTS (Nom,Prenom,Date_Naissance,Genre,Parents_Ident,Adresse,Email,NAS,Mot_de_Passe,Image)
       values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
       
       """
       params=[A.Nom,A.Prenom,A.Date_Naissance,A.Genre,A.Identifiant_Parent,A.Adresse,A.Email,A.NAS,M,decode(A.Image)]
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

@app.post("/ModifInfo_Patient")

async def  modifInfo_patient(P:Modif_Pati):
      
      Sql_Update= "UPDATE  MEDSYNCH.MEDSYNCH.PATIENTS SET Adresse=%s,Email=%s where  Id_Patient=%s "
      params=[P.Adresse,P.Email,P. Id_Patient]
      cursor.execute(Sql_Update,params)

      return  {"message":"Les Informations du patient ont bien été Modifié "}

@app.post("/Medecin_InfoPatient")

async def medecin_InfoPatient(Med:MedecinModif):
    Update="UPDATE  MEDSYNCH.MEDSYNCH.PATIENTS SET Nom=%s,Prenom=%s,Date_Naissance=%s,Genre=%s,Parents_Ident=%s,Adresse=%s,Email=%s,NAS=%s where  Id_Patient=%s "
    Params=[Med.Nom,Med.Prenom,Med.Date_Naissance,Med.Genre,Med.Identifiant_Parent,Med.Adresse,Med.Email,Med.NAS]
    cursor.execute(Update,Params)

    return {"message":"Toutes les informations du Patients ont été Modifiés avec succes"}

@app.post("/connect_CapturePatient")

async def facial_Connection(Aude:PatientImage):
    sql="SELECT  MEDSYNCH.MEDSYNCH.PATIENTS where Email=%s"
    params=[Aude.Email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()

    if resultat:
        extract_bd=extractFeatures_bd(Aude.Image)
        image=decode(Aude.Image)

        face_verify=face_detetion(image,extract_bd)
        print(face_verify)

        if face_verify:
             
             s={
              "patient_id":resultat[0],
              "nom":resultat[1],
              "NAS":resultat[8]}
          
             return {"message":s}
        else:
            { "message":"lesvisage sont incompatibles "}


@app.post("/connect_captureMedecin")

async def facial_connectMed(Aud:MedecinImage):
    sql= "SELECT * from  MEDSYNCH.MEDSYNCH.MEDECINS  where Email=%s"
    params=[Aud.Email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()

    if resultat:
        extract_bd=extractFeatures_bd(Aud.Image)
        image=decode(Aud.Image)

        face_verify=face_detetion(image,extract_bd)
        print(face_verify)

        if face_verify:
            x={
               "medecin_id":resultat[0],
              "nom":resultat[1],
              "matricule":resultat[5] 
            }
        return{"message":x}
    else:
        {"message":"Aucune compatibilité"}


data = {
    'users': [
        {
            'id': 1,
            'name': 'Jean Dupont',
            'medicalRecord': 'Allergies aux pollens, asthme.',
        },
        {
            'id': 2,
            'name': 'Marie Martin',
            'medicalRecord': 'Diabète de type 2, hypertension.',
        }
    ]
}

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').lower()
    user_name = request.json.get('userName', '').lower()

    if not user_input or not user_name:
        return jsonify({'response': 'Désolé, je n\'ai pas compris votre demande.'})

    bot_response = "Désolé, je n'ai pas compris votre question. Pouvez-vous reformuler ?"

    # Réponses basées sur le contenu du message de l'utilisateur
    if 'malade' in user_input:
        bot_response = "Je suis désolé d'apprendre cela. Si vous avez des symptômes spécifiques, je peux vous aider à trouver des informations."
    elif 'médecin' in user_input:
        bot_response = "Vous pouvez prendre rendez-vous avec un médecin en utilisant notre plateforme."
    elif 'dossier médical' in user_input:
        # Rechercher l'utilisateur dans la "base de données"
        user = next((u for u in data['users'] if u['name'].lower() == user_name), None)
        if user:
            bot_response = f"Votre dossier médical: {user['medicalRecord']}"
        else:
            bot_response = "Désolé, nous n'avons pas trouvé votre dossier médical. Assurez-vous que votre nom est correct."

    return jsonify({'response': bot_response})


        


if __name__== "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000,workers=1)