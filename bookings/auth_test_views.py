from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json


@csrf_exempt
def test_login(request):
    """Test login functionality"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username and password required'
                }, status=400)
            
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful',
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                        'has_profile': hasattr(user, 'profile'),
                        'is_admin': hasattr(user, 'profile') and user.profile.is_admin if hasattr(user, 'profile') else False
                    }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid credentials'
                }, status=401)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Login test failed: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'POST method required'
        }, status=405)


@csrf_exempt
def test_register(request):
    """Test registration functionality"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password1 = data.get('password1')
            password2 = data.get('password2')
            
            if not all([username, email, password1, password2]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'All fields required'
                }, status=400)
            
            if password1 != password2:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Passwords do not match'
                }, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username already exists'
                }, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email already exists'
                }, status=400)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            from bookings.models import UserProfile
            UserProfile.objects.create(user=user)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Registration successful',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'has_profile': hasattr(user, 'profile')
                }
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Registration test failed: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'POST method required'
        }, status=405)
