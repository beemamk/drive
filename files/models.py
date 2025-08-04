from django.db import models

# Create your models here.

def file_upload_path(instance, filename):
    if instance.folder:
        return f'uploads/{instance.folder.name}/{filename}'
    return f'uploads/{filename}'

class Folder(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name
    
    def get_parents(self):
        parents = []
        current = self
        while current.parent:
            parents.append(current.parent)
            current = current.parent
        return parents

class File(models.Model):
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE, null=True, blank=True)
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='file_upload_path')
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name