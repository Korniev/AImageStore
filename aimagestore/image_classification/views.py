from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken, SocialAccount

from django.shortcuts import render, redirect
from django.conf import settings
from googleapiclient.http import MediaFileUpload

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


def save_to_drive(request, img_url):
    if request.user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=request.user, provider='Google').first()
        if social_account:
            token = SocialToken.objects.filter(account=social_account).first()
            if token:
                creds = Credentials(
                    token=token.token,
                    refresh_token=token.token_secret,
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                    client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                )

                service = build('drive', 'v3', credentials=creds)

                file_path = os.path.join(settings.MEDIA_ROOT, img_url)

                file_metadata = {
                    'name': img_url,
                    'mimeType': 'image/jpeg'
                }

                media = MediaFileUpload(file_path, mimetype='image/jpeg')

                file = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                print(f"File saved to Google Drive with ID: {file.get('id')}")

                return redirect('classify:classify_image')

    return redirect('classify:classify_image')
