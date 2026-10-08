from django.shortcuts import render


def login(request):
    return render(request, 'FrontEnd/login.html')

def blog(request):
    return render(request, 'FrontEnd/blog.html')

def detalle_viaje(request, pk):
    return render(request, 'FrontEnd/detalle_viaje.html', {'pk': pk})

def personas(request):
    return render(request, 'FrontEnd/personas.html')

def lugares(request):
    return render(request, 'FrontEnd/lugares.html')

def form_persona(request, pk=None):
    return render(request, 'FrontEnd/form_persona.html', {'pk': pk})

def form_lugar(request, pk=None):
    return render(request, 'FrontEnd/form_lugar.html', {'pk': pk})

def form_viaje(request, pk=None):
    return render(request, 'FrontEnd/form_viaje.html', {'pk': pk})