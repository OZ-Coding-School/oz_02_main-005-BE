from django.urls import path
from .views import CreateComment, CommentList, UpdateComment, DeleteComment, CreateRecomment

urlpatterns = [
     path('comment/create/<int:cardset_id>', CreateComment.as_view(), name="create_comment"),
     path('list/<int:cardset_id>', CommentList.as_view(), name="comment_list"),
     path('comment/update/<int:comment_id>', UpdateComment.as_view(), name='update_comment'),
     path('comment/delete/<int:comment_id>', DeleteComment.as_view(), name='delete_comment'),
     path('recomment/create/<int:cardset_id>/<int:parent_id>', CreateRecomment.as_view(), name="create_recomment"),

 ]