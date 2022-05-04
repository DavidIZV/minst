from django.shortcuts import render

from django.http import HttpResponse

from django.template import loader

from django.http import JsonResponse

from django.http import HttpResponseRedirect

from .forms import UploadFileForm

import os

import time

from .predictor import get_neural_network_predictions

"""DRG"""
def form(request):
    template = loader.get_template('form.html')
    context = {}
    return HttpResponse(template.render(context, request))

def prediction(request):
    img_name, full_path, complete=read_image(request)
    prediction_models,prediction_models_acc=get_neural_network_predictions(full_path)
    json_response={'prediction_models': prediction_models, 'prediction_models_acc': prediction_models_acc, 'img_name': img_name, 'full_path': full_path, 'complete': complete}
    return JsonResponse(json_response, safe=False)

def read_image(request):
    complete=0
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        complete=1
        if form.is_valid():
            image=request.FILES['img']
            complete=1
            img_name, full_path=handle_uploaded_file(image)
            return img_name, full_path, complete
        else:
            complete=form.errors
    else:
        form = UploadFileForm()
        print("No es post")
    return None, None, complete

def handle_uploaded_file(f):
    img_name=str(time.time())
    full_path_tmp=os.path.dirname(__file__) + "/static/tmp"
    if os.path.exists(full_path_tmp) == False:
        os.makedirs(full_path_tmp)
    full_path=full_path_tmp + "/" + img_name
    print(img_name)
    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return img_name, full_path
