#! /usr/bin/python

# import the necessary packages
from imutils import paths
import cv2
import os
import face_recognition
import pickle

#path of data folder
print("Starting...")
imagePaths = list(paths.list_images("my_dataset"))

# list of face datas and names
face_datas = []
name_datas = []

for (i, imagePath) in enumerate(imagePaths): # extract images names
	
	print(f"Processing image {i + 1}/{len(imagePaths)}")
	name = imagePath.split(os.path.sep)[-2] # extract names

	image = cv2.imread(imagePath) #read image
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert bgr to rgb

	boxes = face_recognition.face_locations(rgb,model="hog") #detect face (x,y) and boxing

	face_data_embed = face_recognition.face_encodings(rgb, boxes) #creating embed data for face

	for face in face_data_embed:
		#update lists
		face_datas.append(face)
		name_datas.append(name)

#write trained  file

data = {"face_data_encode": face_datas, "names": name_datas}

with open("trained_model.pickle", "wb") as file:
	file.write(pickle.dumps(data))

print("Finished...")
