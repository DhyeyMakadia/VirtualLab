from django.shortcuts import redirect, render
from University.views import *

# modules for rest api
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, TblUserSerializer


from University.models import TblDepartments
from User.models import Account, TblUsers

# Create your views here.


# ========================= Admin Panel views ==============================

def login(request):
    err = ''
    if request.POST:
        em = request.POST['em1']
        pwd = request.POST['pass']

        try:
            obj = Account.objects.get(email=em)
            if obj.check_password(pwd):
                request.session['admin_session'] = obj.id
                return redirect('dashboard')
            else:
                err = 'Wrong Password'
        except:
            err = 'Wrong Email'
    return render(request,'login.html',{'error':err})

def profile(request):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        role = TblRoles.objects.get(admin_id = User_Admin)
        perm = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        if request.POST:
            nm = request.POST['nm1']
            cno = request.POST['cno1']
            prof1 = request.FILES.get('prof1')

            User_Admin.admin_name = nm
            User_Admin.admin_contact_number = cno
            if prof1 != None:
                User_Admin.admin_image = prof1
            User_Admin.save()
        return render(request,'profile.html',{'Users':User,'univ':univ,'admin':User_Admin,'role':role,'perm':perm})
    else:
        return redirect('login')

def changepassword(request):
    err = suc = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        univ = TblUniversity.objects.all()
        if request.POST:
            pwd = request.POST['pwd']
            pwd1 = request.POST['pwd1']
            pwd2 = request.POST['pwd2']

            if User.check_password(pwd):
                if pwd1 == pwd2:
                    print('1')
                    serializer = RegistrationSerializer(User,data={'email':User.email,'password':pwd1,'password2':pwd2},partial=True)
                    print(2)
                    if serializer.is_valid():
                        print(3)
                        account = serializer.save()
                        suc = 'Password Changed Successfully'
                    else:
                        err = "Invalid Input"
                        print(serializer.errors)
                else:
                    err = 'Password Must Match !!'
            else:
                err = 'Wrong Password'

        return render(request,'changepassword.html',{'Users':User,'univ':univ,'admin':User_Admin,'error':err,'success':suc})
    else:
        return redirect('login')

def logout(request):
    if 'admin_session' in request.session.keys():
        del request.session['admin_session']
        return redirect('login')
    else:
        print('session not found')

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
