from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from myapp.models import CustomUser, DailyInput


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

def get_my_id(request):
    try:
        username = request.GET.get('username')
        user = CustomUser.objects.get(username=username)
        my_id = user.id
        response_data = {'my_id': my_id}
        return JsonResponse(response_data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def create_daily_input(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            # Create a DailyInput instance
            daily_input = DailyInput(
                date=data['date'],
                user=request.user,  # Assuming you have authentication in place
                wellbeing=data['wellbeing'],
                vigor=data['vigor'],
                foods=data['foods'],
                hours_slept=data['hours_slept'],
                wakeup_time=data['wakeup_time']
            )
            
            # Save the instance
            daily_input.save()
            
            return JsonResponse({'message': 'DailyInput created successfully'}, status=201)
        
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_all_daily_input_by_user(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            daily_inputs = DailyInput.objects.filter(user_id=user_id)
            response_data = {'my_daily_inputs': list(daily_inputs.values())}
            return JsonResponse(response_data)
        except DailyInput.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)