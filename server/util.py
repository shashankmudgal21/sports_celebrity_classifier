import cv2
import numpy as np
import base64
import json
import joblib
from Wavelet import wavelett_trans

__class_codes = {}
__class_decodes = {}

__model = None



def get_image_b64(img_b64):
    encoded_data = img_b64.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def load_model():
    print("LOADING MODEL.......")
    global __class_codes
    global __class_decodes
    
    with open("J:\\Study Material\\Machine Learning Project\\Celebrity Image Classifier\\server\\artifacts\class_dict.json", "r") as f:
        __class_codes = json.load(f)
        __class_decodes = {v : k for k,v in __class_codes.items()}
        
    global __model
    
    if __model is None:
        with open("J:\Study Material\Machine Learning Project\Celebrity Image Classifier\Deep_Model.sav", 'rb') as f:
            __model = joblib.load(f)
    print("MODEL LOADED.......READY")
    

def crop_face(img_path, img_b64):
    face_classifier = cv2.CascadeClassifier("C:/Users/jonua/opencv-4.x/data/haarcascades/haarcascade_frontalface_default.xml")
    eye_classifier = cv2.CascadeClassifier("C:/Users/jonua/opencv-4.x/data/haarcascades/haarcascade_eye.xml")
    if img_path:
        img = cv2.imread(img_path)
    else:
        img = get_image_b64(img_b64)
    crpped_faces = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 4)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_classifier.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            crpped_faces.append(roi_color)
    return crpped_faces


def decode_celeb(code):
    return __class_decodes[code]


def classify_img(b64_img, path=None):
    imgs = crop_face(path, b64_img)
    result = []
    for img in imgs:
        scaled_raw_img = cv2.resize(img, (32,32))
        img_har = wavelett_trans(img)
        scaled_har_img = cv2.resize(img_har, (32,32))
        stack_img = np.vstack((scaled_raw_img.reshape(32*32*3, 1), scaled_har_img.reshape(32*32, 1)))
        # len_img = 32*32*3 + 32*32
        fin_img = stack_img.reshape(1,64, 64)
        fin_img = np.array(fin_img, dtype=np.uint8)
        # print(fin_img.shape)
        list_prob = __model.predict(fin_img)
        list_prob = np.array(list_prob*100, int)[0].tolist()
        result.append({
            'class': decode_celeb(np.argmax(__model.predict(fin_img)[0])),
            'class_probability': list_prob,
            'class_dictionary': __class_decodes
        })
    return result


def b64_image():
    with open("b64.txt", "r") as f:
        return f.read()        


if __name__ == '__main__':
    load_model()
    #code = classify_img(None, 'J:\Study Material\Machine Learning Project\Celebrity Image Classifier\Image DataSet\\ben_afflek\httpsuploadwikimediaorgwikipediacommonsthumbddBenAffleckbyGageSkidmorejpgpxBenAffleckbyGageSkidmorejpg.jpg')
    #code = classify_img(None, 'J:\Study Material\Machine Learning Project\Celebrity Image Classifier\Image DataSet\\roger_federer\Federer_640.jpg')
    #code = classify_img(None, 'J:\Study Material\Machine Learning Project\Celebrity Image Classifier\Image DataSet\lionel_messi\lionel-messi-net-worth-1.jpg')
    #print(code)
    