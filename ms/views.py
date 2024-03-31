from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Data, Text,ms_user
from django.db.models import Q
from django.shortcuts import render ,get_object_or_404 ,redirect
from django.http import HttpResponse ,HttpRequest, HttpResponseForbidden
from django.core.exceptions import FieldError
from django.contrib.auth.decorators import login_required


def ms_index(request, user):
    # Retrieve the User object based on its primary key (pk=user)
    user_obj = get_object_or_404(User, username=user)
    

    try:
        # Attempt to get the Data object related to the current user
        current_data = Data.objects.get(name=request.user, from_name=user_obj)
        text = current_data.text.values_list('text', flat=True)
    except Data.DoesNotExist:
        # If the Data object doesn't exist, set a default value for text
        text = "Default text"

    print(text)
    # Get the ms_user object related to the current user
    try:
        current_user_ms = ms_user.objects.get(name=request.user)
        img = current_user_ms.photo
    except ms_user.DoesNotExist:
        # If there is no related ms_user object for the current user, set img to None or provide a default value
        img = None


    contact = current_user_ms.contact.all()

    return render(request, 'ms_index.html', {"user": user, "img": img, "text": text,"contact":contact,})
