from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm
from .model_loader import model, class_indices
from .utils import preprocess_image, classify_image
import os
from uuid import uuid4


def classify_image_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            unique_filename = f"{uuid4().hex}_{img.name}"
            img_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
            with open(img_path, 'wb+') as f:
                for chunk in img.chunks():
                    f.write(chunk)

            if not os.path.exists(img_path):
                return render(request, 'image_classification/upload.html', {
                    'form': form,
                    'error': 'File not found after upload. Please try again.'
                })

            img_array = preprocess_image(img_path)
            predicted_class_name, predicted_probability, predictions = classify_image(model, img_array, class_indices)

            probabilities = {class_name: prob * 100 for class_name, prob in zip(class_indices, predictions)}
            top_class, top_probability = max(probabilities.items(), key=lambda item: item[1])
            unique_id = uuid4().hex

            return render(request, 'image_classification/result.html', {
                'class_name': top_class,
                'probability': top_probability,
                'img_url': unique_filename,
                'unique_id': unique_id,
            })
    else:
        form = ImageUploadForm()
    return render(request, 'image_classification/upload.html', {'form': form})
