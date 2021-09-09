from Appartus.models import tbl_appartus
from University.models import tbl_courses
from django.db import models

# Create your models here.

class tbl_input_parameter(models.Model):
    input_parameter_name = models.CharField("Input Parameter",default="",blank=True,null=True,max_length=50)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class tbl_output_parameter(models.Model):
    output_parameter_name = models.CharField("Output Parameter",default="",blank=True,null=True,max_length=50)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class tbl_fixed_input_parameter(models.Model):
    fixed_input_parameter_name = models.CharField("Fixed Input Parameter",default="",blank=True,null=True,max_length=50)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class tbl_fixed_output_parameter(models.Model):
    fixed_output_parameter_name = models.CharField("Fixed Output Parameter",default="",blank=True,null=True,max_length=50)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class tbl_practical(models.Model):
    course_id = models.ForeignKey(tbl_courses,related_name="practical_course_id",on_delete=models.CASCADE,blank=True,null=True)
    practical_name = models.CharField("Practical Name",default="",blank=True,null=True,max_length=100)
    practical_feature_image = models.ImageField(upload_to="Practical/Practical-Feature-Images",default="",max_length=200,blank=True,null=True)
    practical_procedure = models.TextField("Procedure",default="",null=True,blank=True)
    practical_application = models.TextField("Application",default="",null=True,blank=True)
    practical_advantages = models.TextField("Advantages",default="",null=True,blank=True)
    practical_conclusion = models.TextField("Conclusion",default="",null=True,blank=True)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class tbl_multiple_practical_images(models.Model):
    practical_id = models.ForeignKey(tbl_practical,related_name="multiple_practical_images_practical_id",on_delete=models.CASCADE,blank=True,null=True)
    image_path = models.CharField("Practical/Multiple-Practical-Images/{practical_id.practical_name}",default="",blank=True,null=True,max_length=200)

class tbl_multiple_appartus(models.Model):
    practical_id = models.ForeignKey(tbl_practical,related_name="multiple_appartus_practical_id",on_delete=models.CASCADE,blank=True,null=True)
    appartus_id = models.ForeignKey(tbl_appartus,related_name="multiple_appartus_appartus_id",on_delete=models.CASCADE,blank=True,null=True)

class tbl_multiple_youtube_links(models.Model):
    practical_id = models.ForeignKey(tbl_practical,related_name="multiple_youtube_links_practical_id",on_delete=models.CASCADE,blank=True,null=True)
    youtube_video_title = models.CharField("Title",default="",blank=True,null=True,max_length=50)
    youtube_video_links = models.CharField("Youtube Link",default="",blank=True,null=True,max_length=200)

class tbl_multiple_materials(models.Model):
    practical_id = models.ForeignKey(tbl_practical,related_name="multiple_materials_practical_id",on_delete=models.CASCADE,blank=True,null=True)
    material_name = models.CharField("Material Name",default="",blank=True,null=True,max_length=50)
    material_file_path = models.CharField("Practical/Materials/{practical_id.practical_name}",default="",blank=True,null=True,max_length=200)

class tbl_multiple_input_parameter(models.Model):
    practical_id = models.ForeignKey(tbl_practical,related_name="multiple_materials_practical_id",on_delete=models.CASCADE,blank=True,null=True)
    input_parameter_id = models.ForeignKey(tbl_input_parameter,related_name="multiple_input_parameter_input_parameter_id",on_delete=models.CASCADE,blank=True,null=True)
    input_parameter_name = models.CharField("Input Parameter Name",default="",blank=True,null=True,max_length=100)
    input_parameter_value = models.CharField("Input Parameter Value",default="",blank=True,null=True,max_length=100)

class tbl_multiple_output_parameter(models.Model):
    practical_id = models.ForeignKey(tbl_practical,related_name="multiple_materials_practical_id",on_delete=models.CASCADE,blank=True,null=True)
    output_parameter_id = models.ForeignKey(tbl_output_parameter,related_name="multiple_output_parameter_output_parameter_id",on_delete=models.CASCADE,blank=True,null=True)
    output_parameter_name = models.CharField("Output Parameter Name",default="",blank=True,null=True,max_length=100)
    output_parameter_value = models.CharField("Output Parameter Value",default="",blank=True,null=True,max_length=100)

class tbl_multiple_fixed_input_parameter(models.Model):
    practical_id = models.ForeignKey(tbl_practical,related_name="multiple_materials_practical_id",on_delete=models.CASCADE,blank=True,null=True)
    fixed_input_parameter_id = models.ForeignKey(tbl_fixed_input_parameter,related_name="multiple_fixed_input_parameter_fixed_input_parameter_id",on_delete=models.CASCADE,blank=True,null=True)
    fixed_input_parameter_name = models.CharField("Fixed Input Parameter Name",default="",blank=True,null=True,max_length=100)
    fixed_input_parameter_value = models.CharField("Fixed Input Parameter Value",default="",blank=True,null=True,max_length=100)

class tbl_multiple_fixed_output_parameter(models.Model):
    practical_id = models.ForeignKey(tbl_practical,related_name="multiple_materials_practical_id",on_delete=models.CASCADE,blank=True,null=True)
    fixed_output_parameter_id = models.ForeignKey(tbl_fixed_output_parameter,related_name="multiple_fixed_output_parameter_fixed_output_parameter_id",on_delete=models.CASCADE,blank=True,null=True)
    fixed_output_parameter_name = models.CharField("Fixed Output Parameter Name",default="",blank=True,null=True,max_length=100)
    fixed_output_parameter_value = models.CharField("Fixed Output Parameter Value",default="",blank=True,null=True,max_length=100)