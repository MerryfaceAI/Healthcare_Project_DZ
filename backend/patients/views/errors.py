# patients/views/errors.py
from django.shortcuts import render

def custom_page_not_found(request, exception):
    return render(request, "errors/404.html", status=404)

def custom_permission_denied(request, exception):
    return render(request, "errors/403.html", status=403)
