import face_recognition

known_image = face_recognition.load_image_file("Backend/img1.jpg")
unknown_image= face_recognition.load_image_file("Backend/img2.jpg")

img1_encoding = face_recognition.face_encodings(known_image)[0]
img2_encoding= face_recognition.face_encodings(unknown_image)[0]


results= face_recognition.compare_faces([img1_encoding],[img2_encoding])
print (f" les images comparees sont {results}")