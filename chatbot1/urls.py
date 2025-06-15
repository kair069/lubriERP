from django.urls import path
from .views import chatbot_view,chatbot_page

urlpatterns = [
    path("chatbot/", chatbot_view, name="chatbot_api"),  # Ruta para la API
    path("chatbota/", chatbot_page, name="chatbot_page"),
]
