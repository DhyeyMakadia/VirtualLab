from rest_framework import serializers

from Practical.models import TblInputParameter, TblOutputParameter, TblFixedInputParameter, TblFixedOutputParameter, TblPractical, TblMultiplePracticalImages, TblMultipleAppartus, TblMultipleYoutubeLinks, TblMultipleMaterials, TblMultipleInputParameter, TblMultipleOutputParameter, TblMultipleFixedInputParameter, TblMultipleFixedOutputParameter


class TblInputParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblInputParameter
        fields = ['input_parameter_name',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblOutputParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblOutputParameter
        fields = ['output_parameter_name',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblFixedInputParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblFixedInputParameter
        fields = ['fixed_input_parameter_name',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblFixedOutputParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblFixedOutputParameter
        fields = ['fixed_output_parameter_name',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblPracticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblPractical
        fields = ['course_id',
                  'practical_name',
                  'practical_feature_image',
                  'practical_procedure',
                  'practical_application',
                  'practical_advantages',
                  'practical_conclusion',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblMultiplePracticalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMultiplePracticalImages
        fields = ['practical_id',
                  'image_path']


class TblMultipleAppartusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMultipleAppartus
        fields = ['practical_id',
                  'appartus_id']


class TblMultipleYoutubeLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMultipleYoutubeLinks
        fields = ['practical_id',
                  'youtube_video_title',
                  'youtube_video_links']


class TblMultipleMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMultipleMaterials
        fields = ['practical_id',
                  'material_name',
                  'material_file_path']


class TblMultipleInputParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMultipleInputParameter
        fields = ['practical_id',
                  'input_parameter_id',
                  'input_parameter_name',
                  'input_parameter_value']


class TblMultipleOutputParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMultipleOutputParameter
        fields = ['practical_id',
                  'output_parameter_id',
                  'output_parameter_name',
                  'output_parameter_value']


class TblMultipleFixedInputParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMultipleFixedInputParameter
        fields = ['practical_id',
                  'fixed_input_parameter_id',
                  'fixed_input_parameter_name',
                  'fixed_input_parameter_value']


class TblMultipleFixedOutputParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMultipleFixedOutputParameter
        fields = ['practical_id',
                  'fixed_output_parameter_id',
                  'fixed_output_parameter_name',
                  'fixed_output_parameter_value']
