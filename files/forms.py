from django import forms
from .models import File,Folder

class UploadFileForm(forms.ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(),required=False,empty_label="No folder")

    class Meta:
        model = File
        fields = ['file']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent']


