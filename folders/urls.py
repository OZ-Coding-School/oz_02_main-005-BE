from django.urls import path
from .views import CreateFolder

urlpatterns = [
    path("folder/create", CreateFolder.as_view(), name="create_folder"),

]