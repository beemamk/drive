# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import File
# from .forms import FileUploadForm

# # Create your views here.

# def upload_file_view(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_instance = form.save()
#             file_instance.file_size = request.FILES['file'].size
#             file_instance.save()
#             messages.success(request, 'File uploaded successfully!')
#             return redirect('file_list')
#         else:
#             messages.error(request, 'Error uploading file. Please try again.')
#     else:        
#         form = FileUploadForm()
#         return render(request, 'upload.html',{'form':form})
    

# def file_list_view(request):
#     files = File.objects.all()
#     return render(request, 'file_list.html',{'files': files})

        



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UploadFileForm, FolderForm
from .models import File, Folder
import os

def upload_file_view(request, folder_id=None):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.file_size = request.FILES['file'].size
            uploaded_file = request.FILES['file']
            file_name, file_ext = os.path.splitext(uploaded_file.name)
            file_instance.file_name = file_name
            file_instance.file_type = file_ext.lstrip('.').lower()
            # Prioritize folder_id from URL over form
            if folder_id:
                try:
                    file_instance.folder = get_object_or_404(Folder, id=folder_id)
                except Folder.DoesNotExist:
                    messages.error(request, 'Invalid folder specified.')
                    return redirect('file_list')
            else:
                file_instance.folder = form.cleaned_data['folder']  # Use form's folder if no folder_id
            file_instance.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('file_list_folder', folder_id=folder_id) if folder_id else redirect('file_list')
        else:
            messages.error(request, 'Error uploading file. Please try again.')
            print(form.errors)
    else:
        initial_folder = get_object_or_404(Folder, id=folder_id) if folder_id else None
        form = UploadFileForm(initial={'folder': initial_folder})
    return render(request, 'upload.html', {
        'form': form,
        'current_folder': initial_folder
    })


# def file_list_view(request, folder_id=None):
#     folder = None
#     if folder_id:
#         folder = Folder.objects.get(id=folder_id)
#         files = File.objects.filter(folder=folder)
#         folders = Folder.objects.filter(parent=folder)
#     else:
#         files = File.objects.filter(folder__isnull=True)
#         folders = Folder.objects.filter(parent__isnull=True)
#     return render(request, 'file_list.html', {'files': files, 'folders': folders, 'current_folder': folder})


from django.shortcuts import render, get_object_or_404

def file_list_view(request, folder_id=None):
    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id)
        files = File.objects.filter(folder=folder)
        folders = Folder.objects.filter(parent=folder)
    else:
        files = File.objects.filter(folder__isnull=True)
        folders = Folder.objects.filter(parent__isnull=True)
    
    context = {
        'files': files,
        'folders': folders,
        'current_folder': folder,
    }
    return render(request, 'file_list.html', context)

def create_folder_view(request, folder_id=None):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            if folder_id:
                folder.parent = get_object_or_404(Folder, id=folder_id)
            folder.save()
            messages.success(request, 'Folder created successfully!')
            return redirect('file_list_folder', folder_id=folder_id) if folder_id else redirect('file_list')
        else:
            messages.error(request, 'Error creating folder. Please try again.')
            print(form.errors)
    else:
        initial_parent = get_object_or_404(Folder, id=folder_id) if folder_id else None
        form = FolderForm(initial={'parent': initial_parent})
    return render(request, 'create_folder.html', {
        'form': form,
        'current_folder': initial_parent
    })