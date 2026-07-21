from django.shortcuts import render
from django.http import HttpResponse

def document_list(request):
    return HttpResponse("Список документов")