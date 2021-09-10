from django.shortcuts import render

# modules for rest api
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, TblUserSerializer


from University.models import TblDepartments
from User.models import Account, TblUsers

# Create your views here.


# ========================= rest api views ==============================

@api_view(['POST'])
def registration(request):
    account_dic = {'email': request.POST['email'],
                   'password': request.POST['password'],
                   'password2': request.POST['password2']}
    account_serializer = RegistrationSerializer(data=account_dic)
    if account_serializer.is_valid():
        account = account_serializer.save()
        print(account)
    else:
        return Response({'error': 202,
                         'message': 'There was an error in account registration, Please try again.',
                         'serializer_error': account_serializer.errors}, status=500)
    department_id = request.POST['department_id']
    try:
        department = TblDepartments.objects.get(id=department_id)
    except TblDepartments.DoesNotExist:
        return Response({'error': 201,
                         'message': 'There does not exist such department, Please try again.'}, status=500)
    user_dic = {'account_id': account.id,
                'institute_id': department.institute_id.id,
                'department_id': department.id,
                'user_name': request.POST['user_name'],
                'user_mobile_number': request.POST['user_mobile_number'],
                'user_enrollment_number': request.POST['user_enrollment_number']}
    user_serializer = TblUserSerializer(data=user_dic, partial=True)
    if user_serializer.is_valid():
        user = user_serializer.save()
        print(user_serializer.data)
    else:
        account.delete()
        return Response({'error': 203,
                         'message': 'There was an error in user registration, Please try again',
                         'serializer_error': user_serializer.errors}, status=500)
    response = Response()
    response.status_code = 200
    response.data = account_dic
    return response


@api_view(['GET'])
def fetch_user_approval(request):
    email = request.GET['email']
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return Response({'error': 204,
                         'message': 'Account with such email id does not exist'}, status=404)
    user = TblUsers.objects.get(account_id=account)
    if user.is_approved:
        return Response(1, status=200)
    else:
        return Response(0, status=403)
