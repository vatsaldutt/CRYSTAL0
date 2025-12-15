import os
import cv2
import face_recognition
import pickle
import numpy as np
from PIL import Image

path = './img/known/'
images = []
classNames = []
myList = os.listdir(path)
images = myList

def find_encodings(images_):
    encode_list = []
    for imgs in images_:
        imgs = np.array(Image.open('./img/known/'+imgs))
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(imgs)[0]
        encode_list.append(encode)
    return encode_list


encodeListKnown = find_encodings(images)
print(len(encodeListKnown))
print('Encoding Complete')

with open('face_rec', 'wb') as file:
    pickle.dump(encodeListKnown, file)
    file.close()
