from Practical.models import TblPractical
from Practical.serializers import TblPracticalSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_practicals(request):
    course_id = request.GET['course_id']
    practicals = TblPractical.objects.filter(course_id=course_id)
    serializer = TblPracticalSerializer(practicals, many=True)
    return Response(serializer.data)
