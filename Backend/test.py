import face_recognition
import cv2

# on load les images

image1 = cv2.imread("Backend/aude.jpg")
image2= cv2.imread("Backend\img2.jpg")
image3= cv2.imread("Backend\img3.jpg")


#on transforme en RGB 
image1_rgb=cv2.cvtColor(image1,cv2.COLOR_BGR2RGB)
image2_rgb=cv2.cvtColor(image2,cv2.COLOR_BGR2RGB)

#on localise la face 
face1=face_recognition.face_locations(image1_rgb)
face2=face_recognition.face_locations(image2_rgb)



#on cripte
face_enc1=face_recognition.face_encodings(image2_rgb)[0]
face_enc2=face_recognition.face_encodings(image1_rgb,face1)

print(face_enc1)

#on compare
for face in face_enc2:

    match=face_recognition.compare_faces([face_enc1],face)

print(f"la compatibilite est : {match}")

