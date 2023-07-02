from django.urls import path
from .views import CustomerAPIView

urlpatterns = [
    path('deal/', CustomerAPIView.as_view()),
]