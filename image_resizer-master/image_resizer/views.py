from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import os
import cloudinary
import requests
import io
import zipfile
from django.http import FileResponse


def home(request):
    return render(request,'home.html')

def resize_image(request):
    return render(request,'resize_image.html')    

def resize_bulk(request):
    if request.method == 'POST':
        if not "resized" in os.listdir():
            os.mkdir("resized")
        list_images = request.FILES.getlist('image')
        resizeval = int(request.POST['resizeval'])
        response_images = []
        
        for ctr, i in enumerate(list_images, 1):
            img_name = i.name
            img_name = img_name.split('.')[0]
            img = Image.open(i)
            imgObj = img.resize((resizeval, resizeval), Image.ANTIALIAS)
            imagePath = f"resized/{img_name}{ctr}+.png"
            imgObj.save(imagePath)
            uploaded_image = cloudinary.uploader.upload(imagePath,
                                                        folder="resized_images")
            response_images.append(uploaded_image['url'])
            os.remove(imagePath)
        print(response_images)
        request.session['image_urls'] = response_images
        return render(request,'download_images.html',{'image_list':response_images})

    else:
        return render(request,'resize_bulk.html')    
        

def download_images(request):
    image_urls = request.session.get('image_urls', [])
    public_ids = [url.split("/")[-1].split(".")[0] for url in image_urls]
    version_numbers = []
    for url in image_urls:
        parts = url.split("/")
        version_string = parts[-3]
        version_number = version_string.split("v")[-1]
        version_numbers.append(version_number)
    if not public_ids:
        return HttpResponse('No images found')
    # create in-memory file-like buffer to receive PDF data.
    images = []
    for public_id,version_number in zip(public_ids,version_numbers):
        image_url = f"http://res.cloudinary.com/dbgciyvr2/image/upload/v{version_number}/resized_images/{public_id}.png"
        response = requests.get(image_url)
        if response.status_code == 200:
            images.append(io.BytesIO(response.content))

    in_memory = io.BytesIO()
    with zipfile.ZipFile(in_memory, "a") as zf:
        for i, img in enumerate(images):
            zf.writestr(f"resizedimage_{i}.jpg", img.getvalue())

    in_memory.seek(0)
    response = FileResponse(in_memory, as_attachment=True, filename="images_resized_download.zip")
    return response


