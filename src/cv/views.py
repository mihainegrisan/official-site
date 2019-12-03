from django.shortcuts import render

def home_1(request):
    return render(request, 'cv/cv1.html', {})

def home_2(request):
    return render(request, 'cv/cv2.html', {})
