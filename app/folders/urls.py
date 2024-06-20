from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import CreateFolder, UpdateFolder, DeleteFolder, FolderList

urlpatterns = [
    path("folder/create", CreateFolder.as_view(), name="create_folder"),
    path(
        "folder/update/<int:folder_id>",
        UpdateFolder.as_view(),
        name="update_folder",
    ),
    path(
        "folder/delete/<int:folder_id>",
        DeleteFolder.as_view(),
        name="delete_folder",
    ),
    path("list/<int:member_id>",FolderList.as_view(), name="folder_list"),   
]