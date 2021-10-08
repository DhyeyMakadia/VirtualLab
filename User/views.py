from django.shortcuts import redirect, render
from University.views import *

# modules for rest api
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, TblUserSerializer


from University.models import TblDepartments
from User.models import *

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
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        role = TblRoles.objects.get(admin_id = User_Admin)
        if request.POST:
            nm = request.POST['nm1']
            cno = request.POST['cno1']
            prof1 = request.FILES.get('prof1')

            User_Admin.admin_name = nm
            User_Admin.admin_contact_number = cno
            if prof1 != None:
                User_Admin.admin_image = prof1
            User_Admin.save()
        return render(request,'profile.html',{'Users':User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'role':role,'error':err})
    else:
        return redirect('login')

def changepassword(request):
    err = suc = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        if request.POST:
            pwd = request.POST['pwd']
            pwd1 = request.POST['pwd1']
            pwd2 = request.POST['pwd2']

            if User.check_password(pwd):
                if pwd1 == pwd2:
                    User.set_password(pwd1)
                    User.save()
                    suc = 'Password Changed Successfully'
                else:
                    err = 'Password Must Match !!'
            else:
                err = 'Wrong Password'

        return render(request,'changepassword.html',{'Users':User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'success':suc})
    else:
        return redirect('login')

def register_admin(request):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()

        # PERMISSION TO INSERT(ONLY TO SUPERUSER)
        if not User.is_superuser:
            return redirect('view_admin')

        if request.POST:
            em = request.POST['em1']
            pwd = request.POST['pass1']
            nm = request.POST['nm1']
            cno = request.POST['cno1']
            prof1 = request.FILES.get('prof1')

            # ACCOUNT
            serializer = RegistrationSerializer(data={'email':em,'password':pwd,'password2':pwd,'is_admin':True},partial=True)
            if serializer.is_valid():
                account = serializer.save()
            else:
                err = "Invalid Input"

            # ADMIN
            obj_account = Account.objects.get(email = em)
            obj_account.is_admin = True
            obj_account.is_staff = True
            obj_account.save()
            New_Admin = TblAdmin()
            New_Admin.account_id = obj_account
            New_Admin.admin_name = nm
            New_Admin.admin_contact_number = cno
            if prof1 != None:
                New_Admin.admin_image = prof1
            New_Admin.save()

            #ROLE
            obj_admin = TblAdmin.objects.get(account_id=obj_account)
            New_Role = TblRoles()
            New_Role.admin_id = obj_admin
            New_Role.role_name = str(obj_admin.admin_name) + "(admin)"
            New_Role.save()

            # PERMISSIONS
            obj_role = TblRoles.objects.get(admin_id=obj_admin)
            New_Permissions = TblPermissions()
            New_Permissions.admin_id = obj_admin
            New_Permissions.role_id = obj_role
            New_Permissions.save()
            return redirect('view_admin')

        return render(request, 'register_admin.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err})
    else:
        return redirect('login')

def view_admin(request):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        All_Admin = TblPermissions.objects.all()

        # PERMISSION TO VIEW
        if not User_Permissions.can_view:
            return redirect('dashboard')

        return render(request, 'view_admin.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'all_admin':All_Admin})
    else:
        return redirect('login')

def update_admin(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        univ = TblUniversity.objects.all()
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        Update_Admin = TblAdmin.objects.get(id = id)
        Update_Permissions = TblPermissions.objects.get(admin_id = Update_Admin)

        # RESTRICTED TO UPDATE OWN PROFILE
        if User_Admin.id == id:
            return redirect('view_admin')

        # PERMISSION TO UPDATE
        if not User_Permissions.can_edit:
            return redirect('view_admin')

        if request.POST:
            nm = request.POST['nm1']
            cno = request.POST['cno1']
            prof1 = request.FILES.get('prof1')
            can_view = request.POST['can_view']
            can_insert = request.POST['can_insert']
            can_edit = request.POST['can_edit']
            can_delete = request.POST['can_delete']

            Update_Admin.admin_name = nm
            Update_Admin.admin_contact_number = cno
            if prof1 != None:
                Update_Admin.admin_image = prof1

            if can_view == "true":
                Update_Permissions.can_view = True
            elif can_view == "false":
                Update_Permissions.can_view = False

            if can_insert == "true":
                Update_Permissions.can_insert = True
            elif can_insert == "false":
                Update_Permissions.can_insert = False

            if can_edit == "true":
                Update_Permissions.can_edit = True
            elif can_edit == "false":
                Update_Permissions.can_edit = False

            if can_delete == "true":
                Update_Permissions.can_delete = True
            elif can_delete == "false":
                Update_Permissions.can_delete = False

            Update_Permissions.save()
            Update_Admin.save()

        return render(request, 'update_admin.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'update_admin':Update_Admin,'update_permissions':Update_Permissions,'error':err})
    else:
        return redirect('login')

def delete_admin(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)

        # CAN'T DELETE OWN PROFILE
        if User.id == id:
            return redirect('view_admin')
        
        # PERMISSION TO DELETE
        if not User_Permissions.can_delete:
            return redirect('view_admin')
        else:
            Del_Admin = Account.objects.get(id = id)
            Del_Admin.delete()
            return redirect('view_admin')
    else:
        return redirect('login')

def logout(request):
    if 'admin_session' in request.session.keys():
        del request.session['admin_session']
        return redirect('login')
    else:
        return redirect('login')

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
        return Response(0, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_user_info(request):
    account = request.user
    user = TblUsers.objects.get(account_id=account)
    serializer = TblUserSerializer(user)
    dic = serializer.data
    dic['user_email'] = account.email
    dic['university_name'] = user.institute_id.university_id.university_name
    dic['institute_name'] = user.institute_id.institute_name
    dic['department_name'] = user.department_id.department_name
    return Response(dic)
