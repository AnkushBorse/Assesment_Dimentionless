import csv
from datetime import datetime

import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Image


def upload(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)
        for index, row in df.iterrows():
            image_name = row['image_name']
            objects_detected = row['objects_detected']
            timestamp = row['timestamp']
            Image.objects.create(image_name=image_name, objects_detected=objects_detected, timestamp=timestamp)
        return HttpResponseRedirect('/results/')
    return render(request, 'upload.html', context={"data":Image.objects.all()})

def results(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        images = Image.objects.filter(timestamp__range=[start_date, end_date])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        writer = csv.writer(response)
        writer.writerow(['image_name', 'detections', 'timestamp'])
        total_objects_detected = 0
        for image in images:
            writer.writerow([image.image_name, image.objects_detected, image.timestamp])
            total_objects_detected += len(image.objects_detected.split(','))
        writer.writerow(['', '', ''])
        writer.writerow(['Total Objects Detected:', total_objects_detected])
        return response
    return render(request, 'upload.html')
