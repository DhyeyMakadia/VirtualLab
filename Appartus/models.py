from django.db import models

# Create your models here.

class tbl_appartus_category(models.Model):
    appartus_category_name = models.CharField("Category",default="",blank=True,null=True,max_length=50)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class tbl_appartus_subcategory(models.Model):
    appartus_category_id =models.ForeignKey(tbl_appartus_category,related_name="appartus_subcategory_appartus_category_id",on_delete=models.CASCADE,blank=True,null=True)
    appartus_subcategory_name = models.CharField("Sub Category",default="",blank=True,null=True,max_length=50)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class tbl_appartus(models.Model):
    appartus_category_id = models.ForeignKey(tbl_appartus_category,related_name="appartus_appartus_category_id",on_delete=models.CASCADE,blank=True,null=True)
    appartus_subcategory_id = models.ForeignKey(tbl_appartus_subcategory,related_name="appartus_appartus_subcategory_id",on_delete=models.CASCADE,blank=True,null=True) 
    appartus_name = models.CharField("Name",default="",blank=True,null=True,max_length=100)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)