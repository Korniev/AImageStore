import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf


def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array


def classify_image(model, img_array, class_indices):
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    predicted_class_name = class_indices[predicted_class]
    predicted_probability = np.max(predictions[0]) * 100  # Convert to percentage
    return predicted_class_name, predicted_probability, predictions[0]
