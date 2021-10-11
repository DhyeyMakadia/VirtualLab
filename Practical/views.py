from django.shortcuts import render,redirect
from University.models import TblDepartments, TblUniversity

from User.models import Account, TblAdmin, TblPermissions
from .models import *
# Create your views here.

# import pandas as pd
# df = pd.DataFrame(columns=['V', 'I'])
# writer = pd.ExcelWriter('hello.xlsx', engine='openpyxl')
# writer.sheets
# df2 = pd.DataFrame(columns=['R'])
# df.to_excel(writer, 'input')
# df2.to_excel(writer, 'output')
# writer.save()

# --------------------------------Practical-----------------------------------
def view_practical(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        practical = TblPractical.objects.filter(course_id=id)
        parent_course = TblCourses.objects.get(id = id)

        # PERMISSION TO VIEW
        if not User_Permissions.can_view:
            return redirect('dashboard')

        return render(request, 'practical.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'practical':practical,'parent_course':parent_course})
    else:
        return redirect('login')

def add_practical(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        parent_course = TblCourses.objects.get(id = id)

        # PERMISSION TO INSERT
        if not User_Permissions.can_insert:
            return redirect('view_practical',id=parent_course.id)

        if request.POST:
            name1 = request.POST['nm1']
            img1 = request.FILES.get('img1')
            procedure1 = request.POST['procedure1']
            application1 = request.POST['application1']
            advantages1 = request.POST['advantages1']
            conclusion1 = request.POST['conclusion1']

            Add_Practical = TblPractical()
            Add_Practical.course_id = parent_course
            Add_Practical.practical_name = name1
            if img1 != None:
                Add_Practical.practical_feature_image = img1
            Add_Practical.practical_procedure = procedure1
            Add_Practical.practical_application = application1
            Add_Practical.practical_advantages = advantages1
            Add_Practical.practical_conclusion = conclusion1
            Add_Practical.save()
            return redirect('view_practical',id=parent_course.id)

        return render(request, 'add_practical.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'parent_course':parent_course})
    else:
        return redirect('login')

def update_practical(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        Update_Practical = TblPractical.objects.get(id = id)
        parent_course = Update_Practical.course_id

        # PERMISSION TO UPDATE
        if not User_Permissions.can_edit:
            return redirect('view_practical',id=parent_course.id)

        if request.POST:
            name1 = request.POST['nm1']
            img1 = request.FILES.get('img1')
            procedure1 = request.POST['procedure1']
            application1 = request.POST['application1']
            advantages1 = request.POST['advantages1']
            conclusion1 = request.POST['conclusion1']

            Update_Practical.practical_name = name1
            if img1 != None:
                Update_Practical.practical_feature_image = img1
            Update_Practical.practical_procedure = procedure1
            Update_Practical.practical_application = application1
            Update_Practical.practical_advantages = advantages1
            Update_Practical.practical_conclusion = conclusion1
            Update_Practical.save()
            return redirect('view_practical',id=parent_course.id)

        return render(request, 'update_practical.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'update_practical':Update_Practical,'parent_course':parent_course})
    else:
        return redirect('login')

def delete_practical(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        Del_Practical = TblPractical.objects.get(id = id)
        parent_course = Del_Practical.course_id

        # PERMISSION TO DELETE
        if not User_Permissions.can_delete:
            return redirect('view_practical',id = parent_course.id)
        else:
            Del_Practical.delete()
            return redirect('view_practical',id = parent_course.id)
    else:
        return redirect('login')

# ----------------------------Practical-Details-----------------------------------
def view_practical_details(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        practical_details = TblPractical.objects.get(id=id)

        # PERMISSION TO VIEW
        if not User_Permissions.can_view:
            return redirect('dashboard')

        return render(request, 'view_practical_details.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'practical_details':practical_details})
    else:
        return redirect('login')

# ----------------------------Youtube-Links-----------------------------------
def add_youtube_links(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        parent_practical = TblPractical.objects.get(id = id)

        # PERMISSION TO INSERT
        if not User_Permissions.can_insert:
            return redirect('view_practical_details',id=parent_practical.id)

        if request.POST:
            name1 = request.POST['nm1']
            link1 = request.POST['link1']

            Add_Youtube_Links = TblMultipleYoutubeLinks()
            Add_Youtube_Links.practical_id = parent_practical
            Add_Youtube_Links.youtube_video_title = name1
            Add_Youtube_Links.youtube_video_links = link1
            Add_Youtube_Links.save()
            if 'add_another' in request.POST:
                return redirect('add_youtube_links',id=parent_practical.id)
            elif 'continue' in request.POST:
                pass
            else:
                return redirect('view_practical_details',id=parent_practical.id)

        return render(request, 'add_youtube_links.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'parent_practical':parent_practical})
    else:
        return redirect('login')

def update_youtube_links(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        Update_Youtube_Links = TblMultipleYoutubeLinks.objects.get(id = id)
        parent_practical = Update_Youtube_Links.practical_id

        # PERMISSION TO UPDATE
        if not User_Permissions.can_edit:
            return redirect('view_practical_details',id=parent_practical.id)

        if request.POST:
            name1 = request.POST['nm1']
            link1 = request.POST['link1']

            Update_Youtube_Links.youtube_video_title = name1
            Update_Youtube_Links.youtube_video_links = link1
            Update_Youtube_Links.save()
            if 'add_another' in request.POST:
                return redirect('add_youtube_links',id=parent_practical.id)
            else:
                return redirect('view_practical_details',id=parent_practical.id)

        return render(request, 'update_youtube_links.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'update_youtube_links':Update_Youtube_Links,'parent_practical':parent_practical})
    else:
        return redirect('login')

def delete_youtube_links(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        Del_Youtube_Links = TblMultipleYoutubeLinks.objects.get(id = id)
        parent_practical = Del_Youtube_Links.practical_id

        # PERMISSION TO DELETE
        if not User_Permissions.can_delete:
            return redirect('view_practical_details',id = parent_practical.id)
        else:
            Del_Youtube_Links.delete()
            return redirect('view_practical_details',id = parent_practical.id)
    else:
        return redirect('login')