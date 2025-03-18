from passlib.context import CryptContext
import cv2, numpy as np
import face_recognition
import base64
from datetime import datetime

context=CryptContext(schemes=["pbkdf2_sha256","des_crypt"],deprecated="auto")

def password_hash(password):
    return context.hash(password)

def password_verify(password,hash_password):
    return context.verify(password,hash_password)


# function pour la reconnaissance facial
#extraction des caracteristiques de l'img dans la bd

def extractFeatures_bd(path):


    extractImg=cv2.imread(path)
    img=cv2.cvtColor(extractImg,cv2.COLOR_BGR2RGB)

    try:
        feat=face_recognition.face_encodings(img)[0]
    except:
        print('erreur')

    return feat

#Apres extraction on compare l'img de la connex a celle de la bd
def face_detetion(path,encode_bd):

    extractImg=cv2.imread(path)

    #convertion de l'img en bgr
    img=cv2.cvtColor(extractImg,cv2.COLOR_BGR2RGB)

    #Face detection

    face_curent=face_recognition.face_locations(img)
    print(face_curent)

    if face_curent is None:
        raise ValueError("Aucune face detecter dans l'image")
    
    else:
        #encoding
        face_encode=face_recognition.face_encodings(img,face_curent)[0]
        #compare
        match=face_recognition.compare_faces([encode_bd],face_encode)
        print(match)
        return match

def decode(A):
    aude=base64.b64decode(A.split(",")[1])

    current_time=datetime.now()

    name=current_time.strftime("%H-%M-%S")

    img_name =f"{name}.jpg"

    path=f"Backend\images\{img_name}"

    with open(path,'wb') as f:
        f.write(aude)

    return path
    


