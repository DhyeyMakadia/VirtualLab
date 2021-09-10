from rest_framework import serializers

from Appartus.models import TblAppartus, TblAppartusCategory, TblAppartusSubcategory


class TblAppartusCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAppartusCategory
        fields = ['appartus_category_name',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblAppartusSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAppartusSubcategory
        fields = ['appartus_category_id',
                  'appartus_subcategory_name',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblAppartusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAppartus
        fields = ['appartus_category_id',
                  'appartus_subcategory_id',
                  'appartus_name',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']
