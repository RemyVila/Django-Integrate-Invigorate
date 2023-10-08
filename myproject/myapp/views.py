from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm

from myapp.models import CustomUser
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponse
import json


# Create your views here.

def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')

            # Validate the JSON data
            errors = {}

            if not email:
                errors['email'] = ['This field is required.']
            if not username:
                errors['username'] = ['This field is required.']
            if not password1:
                errors['password1'] = ['This field is required.']
            if not password2:
                errors['password2'] = ['This field is required.']
            if password1 != password2:
                errors['password2'] = ['Passwords do not match.']

            if errors:
                return JsonResponse({"message": "Validation failed", "errors": errors}, status=400)

            # Your registration logic here...
            user = CustomUser.objects.create_user(username=username, email=email, password=password1)

            # Create the user, handle validation, and login if successful.
            if user:
                login(request, user)
                return JsonResponse({"message": "Registration successful"})
            else:
                return JsonResponse({"message": "Registration failed. Please check your input."}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)

def all_users(request):
    # Query all user objects from the database
    users = CustomUser.objects.all()

    # Extract usernames from the user objects
    user_data_list = [
        {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "date_joined": user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            # Add more user attributes as needed
        }
        for user in users
    ]

    # Return the list of usernames in a JSON response
    response_data = {"usernames": user_data_list}
    return JsonResponse(response_data)


