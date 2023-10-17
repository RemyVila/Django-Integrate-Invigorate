from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django.utils import timezone
from django.db.models import Q

from myapp.models import CustomUser, DailyInput

from .calculations import input_correlations
mean_wb_vigor = input_correlations.average_wellbeing_and_vigor_by_hours_slept
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

            # Check if a DailyInput already exists for today and the current user
            today = timezone.now().date()
            existing_input = DailyInput.objects.filter(user=request.user, date=today).first()

            if existing_input:
                # If an entry for today already exists, invoke the update_daily_input function
                return update_daily_input(request, existing_input, data)

            # Create a new DailyInput instance with today's date
            daily_input = DailyInput(
                date=today,
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

def update_daily_input(request, existing_input, new_data):
    new_foods = new_data.get('foods', {}).get('foods', [])
    existing_foods = existing_input.foods.get('foods', [])
    
    # Merge the new foods with the existing foods, removing duplicates
    merged_foods = list(set(existing_foods + new_foods))
    
    # Update other fields if provided in the new data
    existing_input.wellbeing = new_data.get('wellbeing', existing_input.wellbeing)
    existing_input.vigor = new_data.get('vigor', existing_input.vigor)
    existing_input.hours_slept = new_data.get('hours_slept', existing_input.hours_slept)
    existing_input.wakeup_time = new_data.get('wakeup_time', existing_input.wakeup_time)
    
    # Update the foods list in the existing input with the merged list
    existing_input.foods['foods'] = merged_foods

    # Save the updated instance
    existing_input.save()

    return JsonResponse({'message': 'DailyInput updated successfully'}, status=200)


def get_all_daily_input_by_user(request):
    if request.method == 'GET':
        try:
            username = request.GET.get('username')
            user = CustomUser.objects.get(username=username)
            daily_inputs = DailyInput.objects.filter(user=user)
            response_data = {'my_daily_inputs': list(daily_inputs.values())}
            return JsonResponse(response_data)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


def get_average_wellbeing_vigor_by_hours_slept(request):
    if request.method == 'GET':
        try:
            # Get the username from the request
            username = request.GET.get('username')

            # Get the DailyInput objects for the user
            daily_inputs = DailyInput.objects.filter(user__username=username)

            # Convert the queryset into a list of dictionaries
            daily_inputs_data = [{'hours_slept': entry.hours_slept, 'wellbeing': entry.wellbeing, 'vigor': entry.vigor}
                                 for entry in daily_inputs]

            # Calculate the response using the modified mean_wb_vigor function
            response = mean_wb_vigor(daily_inputs_data)

            # Return the response as JSON
            return JsonResponse({"response": response})

        except DailyInput.DoesNotExist:
            return JsonResponse({'error': 'Data not found'}, status=404)