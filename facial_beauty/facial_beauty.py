
from keras.models import load_model, model_from_json
from PIL import Image
import numpy as np
import time
import urllib.request
import cv2
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

def get_model():
    json_file = open(dir_path + '/model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(dir_path + '/model/model_weight.h5')
    return model

MODEL = get_model()
MODEL._make_predict_function()

def faces(img):
    face_cascade = cv2.CascadeClassifier(dir_path + '/model/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    height, width = img.shape[:2]
    for (x, y, w, h) in faces:
        if (w < 250 or h < 250):
            continue
        face = img[y :min(y + h + 75, height),
                   x :min(x + w + 75, h)]
        # only get the first one
        return face

    return img

def predict(img_path):
    img = None
    if type(img_path != str):
        npimg = np.fromstring(img_path.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    elif img_path.startswith('http') or \
       img_path.startswith('data:image/jpeg'):
        req = urllib.request.urlopen(img_path)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
    else:
        img = cv2.imread(img_path)
    
    # Crop the face
    # img = faces(img)
    try:
        img = cv2.resize(img, (227, 227)) / 255.0
    except Exception as e:
        img = img / 255.0 
    img = np.expand_dims(img, axis=0)

    return MODEL.predict(img)[0][0]



# img_path = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMxRw96-QdObv0SflMIXVmLhFT-QgX4SPURqU4qY_h4FK6w2nL8w&s'
# now = time.time()
# pre = predict(img_path)
# print('predict take: ', time.time() - now)
# print(pre)
