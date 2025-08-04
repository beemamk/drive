# from django.urls import path
# from . import views

# url_patterns = [
#     path('upload/', views.upload_file_view, name='upload_file'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # path('upload/', views.upload_file_view, name='upload_file'),
    # path('file_list/', views.file_list_view, name='file_list'),

    path('upload/', views.upload_file_view, name='upload_file'),
    path('upload/<int:folder_id>/', views.upload_file_view, name='upload_file_folder'),
    path('file_list/', views.file_list_view, name='file_list'),
    path('file_list/<int:folder_id>/', views.file_list_view, name='file_list_folder'),
    path('create_folder/', views.create_folder_view, name='create_folder'),
    path('create_folder/<int:folder_id>/', views.create_folder_view, name='create_folder_in'),
]