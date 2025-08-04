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

        



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm, FolderForm
from .models import File, Folder
import os

from django.http import Http404

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
            # Set folder from URL if not specified in form
            if folder_id and not form.cleaned_data['folder']:
                try:
                    file_instance.folder = Folder.objects.get(id=folder_id)
                except Folder.DoesNotExist:
                    messages.error(request, 'Invalid folder specified.')
                    return redirect('file_list')
            file_instance.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('file_list_folder', folder_id=folder_id) if folder_id else redirect('file_list')
        else:
            messages.error(request, 'Error uploading file. Please try again.')
            print(form.errors)
    else:
        form = UploadFileForm(initial={'folder': Folder.objects.get(id=folder_id) if folder_id else None})
    return render(request, 'upload.html', {'form': form, 'current_folder': Folder.objects.get(id=folder_id) if folder_id else None})


def file_list_view(request, folder_id=None):
    folder = None
    if folder_id:
        folder = Folder.objects.get(id=folder_id)
        files = File.objects.filter(folder=folder)
        folders = Folder.objects.filter(parent=folder)
    else:
        files = File.objects.filter(folder__isnull=True)
        folders = Folder.objects.filter(parent__isnull=True)
    return render(request, 'file_list.html', {'files': files, 'folders': folders, 'current_folder': folder})

def create_folder_view(request, folder_id=None):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder_instance = form.save(commit=False)
            if folder_id and not form.cleaned_data['parent']:
                folder_instance.parent = Folder.objects.get(id=folder_id)
            folder_instance.save()
            messages.success(request, 'Folder created successfully!')
            return redirect('file_list_folder', folder_id=folder_id) if folder_id else redirect('file_list')
        else:
            messages.error(request, 'Error creating folder. Please try again.')
    else:
        form = FolderForm(initial={'parent': Folder.objects.get(id=folder_id) if folder_id else None})
    return render(request, 'create_folder.html', {'form': form, 'current_folder': Folder.objects.get(id=folder_id) if folder_id else None})