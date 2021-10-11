from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from User.models import Account, TblUsers
from User.serializers import RegistrationSerializer, TblUserSerializer

from University.models import TblDepartments

# Create your views here.


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
        return Response(account_serializer.errors, status=202)
    department_id = request.POST['department_id']
    try:
        department = TblDepartments.objects.get(id=department_id)
    except TblDepartments.DoesNotExist:
        return Response({'error': ['There does not exist such department, Please try again.']}, status=400)
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
        return Response({'error': ['Email Id Does Not Exist']}, status=400)
    user = TblUsers.objects.get(account_id=account)
    if user.is_approved:
        return Response(1, status=200)
    else:
        return Response({'error': ['Account is not Approved']}, status=400)


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

