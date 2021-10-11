from Practical.models import TblPractical, TblInputParameter, TblOutputParameter, TblMultipleMaterials, TblMultipleYoutubeLinks, TblMultiplePracticalImages
from Practical.serializers import TblPracticalSerializer, TblMultipleYoutubeLinksSerializer, TblMultiplePracticalImagesSerializer, TblMultipleMaterialsSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from VirtualLab.settings import MEDIA_ROOT
import pandas as pd

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_practicals(request):
    course_id = request.GET['course_id']
    practicals = TblPractical.objects.filter(course_id=course_id)
    serializer = TblPracticalSerializer(practicals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_practical_values(request):
    practical_id = request.GET['practical_id']
    practical = TblPractical.objects.get(id=practical_id)
    materials = TblMultipleMaterials.objects.filter(practical_id=practical)
    dic = {'input': {}, 'output': {}, 'f_input': {}, 'f_output': {}}
    if not materials:
        return Response(0)
    else:
        input_parameter = TblInputParameter.objects.filter(practical_id=practical)
        output_parameter = TblOutputParameter.objects.filter(practical_id=practical)
        for material in materials:
            print(MEDIA_ROOT + '\\' + material.material_file_path.name, type(material.material_file_path.name))
            try:
                df_ip = pd.read_excel(MEDIA_ROOT + '\\' + material.material_file_path.name, 'input', engine='openpyxl')
                for i in input_parameter:
                    dic['input'][i.input_parameter_name] = list(df_ip[i.input_parameter_name])
            except KeyError:
                continue
            try:
                df_op = pd.read_excel(MEDIA_ROOT + '\\' + material.material_file_path.name, 'output', engine='openpyxl')
                for i in output_parameter:
                    dic['output'][i.output_parameter_name] = list(df_op[i.output_parameter_name])
            except KeyError:
                continue
            try:
                df_f_in = pd.read_excel(MEDIA_ROOT + '\\' + material.material_file_path.name, 'f_input', engine='openpyxl')
                for i in input_parameter:
                    dic['f_input'][i.input_parameter_name] = list(df_f_in[i.input_parameter_name])
            except KeyError:
                continue
            try:
                df_f_op = pd.read_excel(MEDIA_ROOT + '\\' + material.material_file_path.name, 'f_output', engine='openpyxl')
                for i in input_parameter:
                    dic['f_output'][i.input_parameter_name] = list(df_f_op[i.input_parameter_name])
            except KeyError:
                continue
        return Response(dic)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_youtube_links(request):
    practical_id = request.GET['practical_id']
    practical = TblPractical.objects.get(id=practical_id)
    youtube_links = TblMultipleYoutubeLinks.objects.filter(practical_id=practical)
    serializer = TblMultipleYoutubeLinksSerializer(youtube_links, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_practical_images(request):
    practical_id = request.GET['practical_id']
    practical = TblPractical.objects.get(id=practical_id)
    practical_images = TblMultiplePracticalImages.objects.filter(practical_id=practical)
    serializer = TblMultiplePracticalImagesSerializer(practical_images, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_practical_materials(request):
    practical_id = request.GET['practical_id']
    practical = TblPractical.objects.get(id=practical_id)
    practical_materials = TblMultipleMaterials.objects.filter(practical_id=practical)
    serializer = TblMultipleMaterialsSerializer(practical_materials, many=True)
    return Response(serializer.data)
