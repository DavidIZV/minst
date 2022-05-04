"""DRG"""

from os import walk
import pickle
import os
import numpy as np
from PIL import Image
from numpy import asarray
from tensorflow import keras

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

def get_neural_network_predictions(img_name):
    models_names=get_models_paths('/models/')
    models=get_list_loads_models(models_names)
    img=read_image_as_numpy_and_normalize(img_name)
    return predict_with_models(models, img)

def read_image_as_numpy_and_normalize(img_name):
    img=Image.open(img_name)
    img=img.resize((28, 28))
    img=img.resize((img.height, img.height))
    img=asarray(img)
    img=img.reshape(-1, 28 * 28)
    img=img/255.0
    return img

def predict_with_models(models, img):
    models_predictions,models_predictions_acc,cont={},{},0
    for model in models:
        predict=model.predict([img])
        index_name=np.argmax(predict[0])
        print(index_name)
        clothes=class_names[index_name]
        model_id=str(cont)+"_"+str(model.__class__.__name__)
        models_predictions[model_id]=clothes
        acc=round(100*np.max(predict[0]), 2)
        models_predictions_acc[model_id + '_acc']=acc
        cont=cont+1
    return models_predictions, models_predictions_acc

def get_list_loads_models(models_names):
    models=[]
    for model_name in models_names:
        model=keras.models.load_model(model_name)
        model=keras.Sequential([model, keras.layers.Softmax()])
        models.append(model)
    return models

def get_models_paths(sub_path):
    path = os.path.dirname(__file__) + sub_path
    models_paths = []
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            relative_path = path + filename
            models_paths.append(relative_path)
        break
    return models_paths
