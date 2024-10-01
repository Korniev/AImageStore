import os

from tensorflow.keras.models import load_model
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'utils', 'animal_classification_model.keras')
model = load_model(MODEL_PATH)

with open(os.path.join(settings.BASE_DIR, 'utils', 'name of the animals.txt'), 'r') as f:
    class_indices = f.read().splitlines()
