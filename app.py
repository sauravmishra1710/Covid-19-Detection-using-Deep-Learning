import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='Covid-19_With_EfficientNet_B0.h5'

# Load your trained model
model = load_model(MODEL_PATH)




def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Image Preprocessing
    img = image.img_to_array(img)
    
    img = img/255
    img = np.expand_dims(img, axis=0)

    pred_class = model.predict_classes(x)
    
    if pred_class==0:
        pred_class="Covid Negative"
    elif pred_class==1:
        pred_class="Covid Positive"

    return pred_class


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        f = request.files['file']

        
        basepath = os.path.dirname(__file__)
        if not os.path.exists('uploads'):
            os.mkdir('uploads')
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        #Prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)