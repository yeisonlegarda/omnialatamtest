from user.views import CreateUserView, TokenAuthenticathionView
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token', TokenAuthenticathionView.as_view(), name='token'),
]
