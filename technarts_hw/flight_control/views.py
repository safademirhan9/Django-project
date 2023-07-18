from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
import jwt
import json
from .models import Airline, Aircraft, User
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def jwt_authentication_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            JWTTokenUserAuthentication().authenticate(request)
            return view_func(request, *args, **kwargs)
        except InvalidToken:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except TokenError:
            return JsonResponse({'error': 'Token error'}, status=401)

    return wrapper


@csrf_exempt
def home(request):
    return render(request, "flight_control/home.html")


@csrf_exempt
def not_authorized(request):
    return render(request, "flight_control/auth.html")


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)
            token = AccessToken.for_user(user)

            return JsonResponse({'token': str(token)})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        return render(request, 'flight_control/login.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User(username=username, password=password)
        user.save()

        token = AccessToken.for_user(user)

        return JsonResponse({'token': str(token)})
    else:
        return render(request, 'flight_control/signup.html')


@jwt_authentication_required
@csrf_exempt
def create_airline(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        callsign = request.POST.get('callsign')
        founded_year = request.POST.get('founded_year')
        base_airport = request.POST.get('base_airport')

        airline = Airline.objects.create(
            name=name,
            callsign=callsign,
            founded_year=founded_year,
            base_airport=base_airport
        )
        
        response_data = {'message': 'Airline created'}
        return JsonResponse(response_data, status=201)
    else:
        return render(request, 'flight_control/create_airline.html')


@jwt_authentication_required
@csrf_exempt
def update_airline(request, airline_id):
    airline = get_object_or_404(Airline, id=airline_id)

    if request.method == 'PATCH':
        name = request.POST.get('name')
        founded_year = request.POST.get('founded_year')
        base_airport = request.POST.get('base_airport')

        if name:
            airline.name = name
        if founded_year:
            airline.founded_year = founded_year
        if base_airport:
            airline.base_airport = base_airport

        airline.save()

        response_data = {'message': 'Airline updated'}
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@jwt_authentication_required
@csrf_exempt
def retrieve_airline(request, airline_id):
    if request.method == 'GET':
        airline = get_object_or_404(Airline, id=airline_id)
        response_data = {
            'id': airline.id,
            'name': airline.name,
            'callsign': airline.callsign,
            'founded_year': airline.founded_year,
            'base_airport': airline.base_airport
        }
        return JsonResponse(response_data, status=200)
    else:
        return render(request, 'flight_control/retrieve_airline.html')


@jwt_authentication_required
@csrf_exempt
def list_airlines(request):
    if request.method == 'GET':
        airlines = Airline.objects.all()
        response_data = {'airlines': []}
        for airline in airlines:
            response_data['airlines'].append({
                'id': airline.id,
                'name': airline.name,
                'callsign': airline.callsign,
                'founded_year': airline.founded_year,
                'base_airport': airline.base_airport
            })
        return JsonResponse(response_data, status=200)
    else:
        return render(request, 'flight_control/list_airlines.html', {'airlines': airlines})


@jwt_authentication_required
@csrf_exempt
def create_aircraft(request):
    if request.method == 'POST':
        manufacturer_serial_number = request.POST.get('manufacturer_serial_number')
        aircraft_type = request.POST.get('type')
        model = request.POST.get('model')
        operator_airline_id = request.POST.get('operator_airline')
        number_of_engines = request.POST.get('number_of_engines')

        operator_airline = get_object_or_404(Airline, id=operator_airline_id)

        aircraft = Aircraft.objects.create(
            manufacturer_serial_number=manufacturer_serial_number,
            type=aircraft_type,
            model=model,
            operator_airline=operator_airline,
            number_of_engines=number_of_engines
        )

        response_data = {'message': 'Aircraft created'}
        return JsonResponse(response_data, status=201)
    else:
        return render(request, 'flight_control/create_aircraft.html')


@jwt_authentication_required
@csrf_exempt
def update_aircraft(request, aircraft_id):
    aircraft = get_object_or_404(Aircraft, id=aircraft_id)

    if request.method == 'PATCH':
        manufacturer_serial_number = request.POST.get('manufacturer_serial_number')
        aircraft_type = request.POST.get('type')
        model = request.POST.get('model')
        operator_airline_id = request.POST.get('operator_airline')
        number_of_engines = request.POST.get('number_of_engines')

        if manufacturer_serial_number:
            aircraft.manufacturer_serial_number = manufacturer_serial_number
        if aircraft_type:
            aircraft.type = aircraft_type
        if model:
            aircraft.model = model
        if operator_airline_id:
            operator_airline = get_object_or_404(Airline, id=operator_airline_id)
            aircraft.operator_airline = operator_airline
        if number_of_engines:
            aircraft.number_of_engines = number_of_engines

        aircraft.save()

        response_data = {'message': 'Aircraft updated'}
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@jwt_authentication_required
@csrf_exempt
def retrieve_aircraft(request, aircraft_id):
    if request.method == 'GET':
        aircraft = get_object_or_404(Aircraft, id=aircraft_id)
        response_data = {
            'id': aircraft.id,
            'manufacturer_serial_number': aircraft.manufacturer_serial_number,
            'type': aircraft.type,
            'model': aircraft.model,
            'operator_airline': aircraft.operator_airline.id,
            'number_of_engines': aircraft.number_of_engines
        }
        return JsonResponse(response_data, status=200)
    else:
        return render(request, 'flight_control/retrieve_aircraft.html')


@jwt_authentication_required
@csrf_exempt
def delete_aircraft(request, aircraft_id):
    if request.method == 'POST':
        try:
            aircraft = Aircraft.objects.get(id=aircraft_id)
            aircraft.delete()
            response_data = {'message': 'Aircraft deleted'}
            return JsonResponse(response_data, status=200)
        except Aircraft.DoesNotExist:
            return JsonResponse({'error': 'Aircraft does not exist'}, status=404)
    else:
        return render(request, 'flight_control/delete_aircraft.html', {'aircraft_id': aircraft_id})


@jwt_authentication_required
@csrf_exempt
def delete_airline(request, airline_id):
    if request.method == 'POST':
        try:
            airline = Airline.objects.get(id=airline_id)
            airline.delete()
            response_data = {'message': 'Airline deleted'}
            return JsonResponse(response_data, status=200)
        except Airline.DoesNotExist:
            return JsonResponse({'error': 'Airline does not exist'}, status=404)
    else:
        return render(request, 'flight_control/delete_airline.html', {'airline_id': airline_id})


@csrf_exempt
def obtain_authentication_token(request):
    if request.method == 'POST':
        token = jwt.encode({'username': 'username'}, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({'token': token.decode('utf-8')})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


# @csrf_exempt
# def jwt_authentication(view_func):
#     def wrapper(request, *args, **kwargs):
#         # Extract the token from the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             try:
#                 # Verify and decode the token
#                 token = auth_header.split(' ')[1]
#                 decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#                 # Add the decoded token to the request for further processing
#                 request.jwt_payload = decoded_token
#                 # Call the view function
#                 return view_func(request, *args, **kwargs)
#             except jwt.ExpiredSignatureError:
#                 return JsonResponse({"error": "Token has expired"}, status=401)
#             except jwt.InvalidTokenError:
#                 return JsonResponse({"error": "Invalid token"}, status=401)
#         else:
#             return JsonResponse({"error": "Authorization header required"}, status=401)
#     return wrapper

# # Apply JWT authentication to specific views
# create_airline = jwt_authentication(create_airline)
# update_airline = jwt_authentication(update_airline)
# retrieve_airline = jwt_authentication(retrieve_airline)
# list_airlines = jwt_authentication(list_airlines)
# create_aircraft = jwt_authentication(create_aircraft)
# update_aircraft = jwt_authentication(update_aircraft)
# retrieve_aircraft = jwt_authentication(retrieve_aircraft)
# delete_aircraft = jwt_authentication(delete_aircraft)
# delete_airline = jwt_authentication(delete_airline)