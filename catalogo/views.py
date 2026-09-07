from django.http import HttpResponse

def home(request):
    return HttpResponse("Catálogo de Ferretería - en construcción")