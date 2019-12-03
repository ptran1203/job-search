
from keras.models import load_model, model_from_json
from PIL import Image
import numpy as np
import time
import urllib.request
import cv2
import os
import numpy as np


dir_path = os.path.dirname(os.path.realpath(__file__))
save_path = os.path.join(dir_path ,  "face_droped.jpg")


def get_model():
    json_file = open(dir_path + '/model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(dir_path + '/model/model_weight.h5')
    return model

MODEL = get_model()
MODEL._make_predict_function()
def isvalid(img):
    return img.shape[0] > 0 and img.shape[1] > 0

def val(img):
    return img.shape[0] * img.shape[1]

def drop_face(img):
    allfaces = []
    face_cascade = cv2.CascadeClassifier(dir_path + '/model/haarcascade_frontalface_default.xml')
    try:
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.1, 4)
      height, width = img.shape[:2]
      for (x, y, w, h) in faces:
          face = img[y :min(y + h, height),
                    x -50 :min(x + w, width)]
          # only get the first one
          if (isvalid(face)):
            allfaces.append(face)
    except:
      return img
    
    if (len(allfaces)):
      return sorted(allfaces, key=lambda x: -val(x))[0]
    return img

def predict(img_path, name):
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
    img = drop_face(img)
    try:
        img = cv2.resize(img, (227, 227))
        # save
        cv2.imwrite(save_path.replace('.jpg', name + '.jpg'), img)
    except Exception as e:
        pass
    nor_img = np.expand_dims(img / 255.0, axis=0)

    return {
        'score': MODEL.predict(nor_img)[0][0],
    }


def dropped(name):
    path = save_path.replace('.jpg', name + '.jpg')
    img = open(path, "rb").read()
    # remove file
    if os.path.isfile(path)
        os.remove(path)
    return img
