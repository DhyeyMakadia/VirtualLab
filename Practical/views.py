from django.shortcuts import render, redirect
from django.contrib import messages

from University.models import TblUniversity

from User.models import Account, TblAdmin

from django.contrib.auth.decorators import login_required

from .models import TblPractical, TblCourses, TblMultiplePracticalImages, TblMultipleYoutubeLinks, TblMultipleMaterials, \
    TblInputParameter, TblOutputParameter, TblFixedInputParameter, TblFixedOutputParameter

from guardian.shortcuts import assign_perm, get_objects_for_user, get_users_with_perms

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


@login_required
def view_practical(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    practical = TblPractical.objects.filter(course_id=id)
    parent_course = TblCourses.objects.get(id=id)
    # PERMISSION TO VIEW
    if not user.has_perm('Practical.view_tblpractical'):
        return redirect('dashboard')
    return render(request, 'practical.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'practical': practical, 'parent_course': parent_course})


@login_required
def add_practical(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_course = TblCourses.objects.get(id=id)
    # PERMISSION TO INSERT
    if not user.has_perm('Practical.add_tblpractical'):
        return redirect('view_practical', id=parent_course.id)
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
        try:
            faculty = get_users_with_perms(parent_course).get(groups__name='faculty')
            assign_perm('University.view_tblpractical', faculty, Add_Practical)
            assign_perm('University.change_tblpractical', faculty, Add_Practical)
            assign_perm('University.delete_tblpractical', faculty, Add_Practical)
        except Exception:
            messages.warning(request, 'Unable to find faculty of ' + parent_course.courses_name + '\n'
                             'View, Change and Delete permissions were not assigned')
        return redirect('view_practical_details', id=Add_Practical.id)
    return render(request, 'add_practical.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'parent_course': parent_course})


@login_required
def update_practical(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Practical = TblPractical.objects.get(id=id)
    parent_course = Update_Practical.course_id
    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.change_tblpractical'):
        return redirect('view_practical', id=parent_course.id)
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
        return redirect('view_practical_details', id=Update_Practical.id)
    return render(request, 'update_practical.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_practical': Update_Practical, 'parent_course': parent_course})


@login_required
def delete_practical(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Practical = TblPractical.objects.get(id=id)
    parent_course = Del_Practical.course_id
    # PERMISSION TO DELETE
    if not user.has_perm('Practical.delete_tblpractical'):
        return redirect('view_practical', id=parent_course.id)
    else:
        Del_Practical.delete()
        return redirect('view_practical', id=parent_course.id)


# ----------------------------Practical-Details-----------------------------------

@login_required
def view_practical_details(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    practical_details = TblPractical.objects.get(id=id)
    # PERMISSION TO VIEW
    if not user.has_perm('Practical.view_tblpractical'):
        return redirect('dashboard')
    return render(request, 'view_practical_details.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'practical_details': practical_details})


# ----------------------------Images-----------------------------------

@login_required
def add_multiple_images(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_practical = TblPractical.objects.get(id=id)
    # PERMISSION TO INSERT
    if not user.has_perm('Practical.add_tblmultiplepracticalimages'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        img1 = request.FILES.get('img1')
        Add_Multiple_Images = TblMultiplePracticalImages()
        Add_Multiple_Images.practical_id = parent_practical
        if img1 != None:
            Add_Multiple_Images.image_path = img1
        Add_Multiple_Images.save()
        if 'add_another' in request.POST:
            return redirect('add_multiple_images', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'add_images.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'parent_practical': parent_practical})


@login_required
def update_multiple_images(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Multiple_Images = TblMultiplePracticalImages.objects.filter(practical_id=id)
    parent_practical = TblPractical.objects.get(id=id)
    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.change_tblmultiplepracticalimages'):
        return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'update_multiple_images.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_multiple_images': Update_Multiple_Images, 'parent_practical': parent_practical})


@login_required
def update_images(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Images = TblMultiplePracticalImages.objects.get(id=id)
    parent_practical = Update_Images.practical_id
    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.change_tblmultiplepracticalimages'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        img1 = request.FILES.get('img1')
        if img1 != None:
            Update_Images.image_path = img1
        Update_Images.save()
        if 'add_another' in request.POST:
            return redirect('add_multiple_images', id=parent_practical.id)
        else:
            return redirect('update_multiple_images', id=parent_practical.id)
    return render(request, 'update_images.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_images': Update_Images, 'parent_practical': parent_practical})


@login_required
def delete_images(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Images = TblMultiplePracticalImages.objects.get(id=id)
    parent_practical = Del_Images.practical_id
    # PERMISSION TO DELETE
    if not user.has_perm('Practical.delete_tblmultiplepracticalimages'):
        return redirect('view_practical_details', id=parent_practical.id)
    else:
        Del_Images.delete()
        return redirect('update_multiple_images', id=parent_practical.id)


# ----------------------------Youtube-Links-----------------------------------

@login_required
def add_youtube_links(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_practical = TblPractical.objects.get(id=id)
    # PERMISSION TO INSERT
    if not user.has_perm('Practical.add_tblmultipleyoutubelinks'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        name1 = request.POST['nm1']
        link1 = request.POST['link1']
        Add_Youtube_Links = TblMultipleYoutubeLinks()
        Add_Youtube_Links.practical_id = parent_practical
        Add_Youtube_Links.youtube_video_title = name1
        Add_Youtube_Links.youtube_video_links = link1
        Add_Youtube_Links.save()
        if 'add_another' in request.POST:
            return redirect('add_youtube_links', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'add_youtube_links.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'parent_practical': parent_practical})


@login_required
def update_youtube_links(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Youtube_Links = TblMultipleYoutubeLinks.objects.get(id=id)
    parent_practical = Update_Youtube_Links.practical_id
    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.change_tblmultipleyoutubelinks'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        name1 = request.POST['nm1']
        link1 = request.POST['link1']
        Update_Youtube_Links.youtube_video_title = name1
        Update_Youtube_Links.youtube_video_links = link1
        Update_Youtube_Links.save()
        if 'add_another' in request.POST:
            return redirect('add_youtube_links', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'update_youtube_links.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_youtube_links': Update_Youtube_Links, 'parent_practical': parent_practical})


@login_required
def delete_youtube_links(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Youtube_Links = TblMultipleYoutubeLinks.objects.get(id=id)
    parent_practical = Del_Youtube_Links.practical_id
    # PERMISSION TO DELETE
    if not user.has_perm('Practical.delete_tblmultipleyoutubelinks'):
        return redirect('view_practical_details', id=parent_practical.id)
    else:
        Del_Youtube_Links.delete()
        return redirect('view_practical_details', id=parent_practical.id)


# ----------------------------Materials------------------------------------

@login_required
def add_materials(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_practical = TblPractical.objects.get(id=id)
    # PERMISSION TO INSERT
    if not user.has_perm('Practical.add_tblmultiplematerials'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        name1 = request.POST['nm1']
        path1 = request.FILES.get('path1')
        Add_Materials = TblMultipleMaterials()
        Add_Materials.practical_id = parent_practical
        Add_Materials.material_name = name1
        if path1 != None:
            Add_Materials.material_file_path = path1
        Add_Materials.save()
        if 'add_another' in request.POST:
            return redirect('add_materials', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'add_materials.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'parent_practical': parent_practical})


@login_required
def update_materials(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Materials = TblMultipleMaterials.objects.get(id=id)
    parent_practical = Update_Materials.practical_id
    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.change_tblmultiplematerials'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        name1 = request.POST['nm1']
        path1 = request.FILES.get('path1')
        Update_Materials.material_name = name1
        if path1 != None:
            Update_Materials.material_file_path = path1
        Update_Materials.save()
        if 'add_another' in request.POST:
            return redirect('add_materials', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'update_materials.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_materials': Update_Materials, 'parent_practical': parent_practical})


@login_required
def delete_materials(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Materials = TblMultipleMaterials.objects.get(id=id)
    parent_practical = Del_Materials.practical_id
    # PERMISSION TO DELETE
    if not user.has_perm('Practical.delete_tblmultiplematerials'):
        return redirect('view_practical_details', id=parent_practical.id)
    else:
        Del_Materials.delete()
        return redirect('view_practical_details', id=parent_practical.id)


# ----------------------------Input-Parameters------------------------------------

@login_required
def add_input_parameters(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_practical = TblPractical.objects.get(id=id)
    # PERMISSION TO INSERT
    if not user.has_perm('Practical.add_tblinputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        name1 = request.POST['parameter1']
        Add_Input_Parameters = TblInputParameter()
        Add_Input_Parameters.practical_id = parent_practical
        Add_Input_Parameters.input_parameter_name = name1
        Add_Input_Parameters.save()
        if 'add_another' in request.POST:
            return redirect('add_input_parameters', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'add_input_parameters.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'parent_practical': parent_practical})


@login_required
def update_input_parameters(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Input_Parameters = TblInputParameter.objects.get(id=id)
    parent_practical = Update_Input_Parameters.practical_id
    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.change_tblinputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        name1 = request.POST['parameter1']
        Update_Input_Parameters.input_parameter_name = name1
        Update_Input_Parameters.save()
        if 'add_another' in request.POST:
            return redirect('add_input_parameters', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'update_input_parameters.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_input_parameters': Update_Input_Parameters, 'parent_practical': parent_practical})


@login_required
def delete_input_parameters(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Input_Parameters = TblInputParameter.objects.get(id=id)
    parent_practical = Del_Input_Parameters.practical_id
    # PERMISSION TO DELETE
    if not user.has_perm('Practical.delete_tblinputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)
    else:
        Del_Input_Parameters.delete()
        return redirect('view_practical_details', id=parent_practical.id)


# ----------------------------Fixed-Input-Parameters------------------------------------

@login_required
def add_fixed_input_parameters(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_practical = TblPractical.objects.get(id=id)
    # PERMISSION TO INSERT
    if not user.has_perm('Practical.add_tblfixedinputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        name1 = request.POST['parameter1']
        Add_Fixed_Input_Parameters = TblFixedInputParameter()
        Add_Fixed_Input_Parameters.practical_id = parent_practical
        Add_Fixed_Input_Parameters.fixed_input_parameter_name = name1
        Add_Fixed_Input_Parameters.save()
        if 'add_another' in request.POST:
            return redirect('add_fixed_input_parameters', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'add_fixed_input_parameters.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'parent_practical': parent_practical})


@login_required
def update_fixed_input_parameters(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Fixed_Input_Parameters = TblFixedInputParameter.objects.get(id=id)
    parent_practical = Update_Fixed_Input_Parameters.practical_id
    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.change_tblfixedinputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)
    if request.POST:
        name1 = request.POST['parameter1']
        Update_Fixed_Input_Parameters.fixed_input_parameter_name = name1
        Update_Fixed_Input_Parameters.save()
        if 'add_another' in request.POST:
            return redirect('add_fixed_input_parameters', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)
    return render(request, 'update_fixed_input_parameters.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_fixed_input_parameters': Update_Fixed_Input_Parameters,
                   'parent_practical': parent_practical})


@login_required
def delete_fixed_input_parameters(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Fixed_Input_Parameters = TblFixedInputParameter.objects.get(id=id)
    parent_practical = Del_Fixed_Input_Parameters.practical_id

    # PERMISSION TO DELETE
    if not user.has_perm('Practical.delete_tblfixedinputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)
    else:
        Del_Fixed_Input_Parameters.delete()
        return redirect('view_practical_details', id=parent_practical.id)


# ----------------------------Output-Parameters------------------------------------

@login_required
def add_output_parameters(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_practical = TblPractical.objects.get(id=id)

    # PERMISSION TO INSERT
    if not user.has_perm('Practical.add_tbloutputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)

    if request.POST:
        name1 = request.POST['parameter1']

        Add_Output_Parameters = TblOutputParameter()
        Add_Output_Parameters.practical_id = parent_practical
        Add_Output_Parameters.output_parameter_name = name1
        Add_Output_Parameters.save()
        if 'add_another' in request.POST:
            return redirect('add_output_parameters', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)

    return render(request, 'add_output_parameters.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'parent_practical': parent_practical})


@login_required
def update_output_parameters(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Output_Parameters = TblOutputParameter.objects.get(id=id)
    parent_practical = Update_Output_Parameters.practical_id

    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.change_tbloutputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)

    if request.POST:
        name1 = request.POST['parameter1']

        Update_Output_Parameters.output_parameter_name = name1
        Update_Output_Parameters.save()
        if 'add_another' in request.POST:
            return redirect('add_output_parameters', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)

    return render(request, 'update_output_parameters.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_output_parameters': Update_Output_Parameters, 'parent_practical': parent_practical})


@login_required
def delete_output_parameters(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Output_Parameters = TblOutputParameter.objects.get(id=id)
    parent_practical = Del_Output_Parameters.practical_id

    # PERMISSION TO DELETE
    if not user.has_perm('Practical.delete_tbloutputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)
    else:
        Del_Output_Parameters.delete()
        return redirect('view_practical_details', id=parent_practical.id)


# ----------------------------Fixed-Output-Parameters------------------------------------

@login_required
def add_fixed_output_parameters(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_practical = TblPractical.objects.get(id=id)

    # PERMISSION TO INSERT
    if not user.has_perm('Practical.add_tblfixedoutputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)

    if request.POST:
        name1 = request.POST['parameter1']

        Add_Fixed_Output_Parameters = TblFixedOutputParameter()
        Add_Fixed_Output_Parameters.practical_id = parent_practical
        Add_Fixed_Output_Parameters.fixed_output_parameter_name = name1
        Add_Fixed_Output_Parameters.save()
        if 'add_another' in request.POST:
            return redirect('add_fixed_output_parameters', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)

    return render(request, 'add_fixed_output_parameters.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'parent_practical': parent_practical})


@login_required
def update_fixed_output_parameters(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Fixed_Output_Parameters = TblFixedOutputParameter.objects.get(id=id)
    parent_practical = Update_Fixed_Output_Parameters.practical_id

    # PERMISSION TO UPDATE
    if not user.has_perm('Practical.add_tblfixedoutputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)

    if request.POST:
        name1 = request.POST['parameter1']

        Update_Fixed_Output_Parameters.fixed_output_parameter_name = name1
        Update_Fixed_Output_Parameters.save()
        if 'add_another' in request.POST:
            return redirect('add_fixed_output_parameters', id=parent_practical.id)
        else:
            return redirect('view_practical_details', id=parent_practical.id)

    return render(request, 'update_fixed_output_parameters.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'update_fixed_output_parameters': Update_Fixed_Output_Parameters,
                   'parent_practical': parent_practical})


@login_required
def delete_fixed_output_parameters(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Fixed_Output_Parameters = TblFixedOutputParameter.objects.get(id=id)
    parent_practical = Del_Fixed_Output_Parameters.practical_id

    # PERMISSION TO DELETE
    if not user.has_perm('Practical.add_tblfixedoutputparameter'):
        return redirect('view_practical_details', id=parent_practical.id)
    else:
        Del_Fixed_Output_Parameters.delete()
        return redirect('view_practical_details', id=parent_practical.id)
