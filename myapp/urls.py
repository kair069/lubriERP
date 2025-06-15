from django.urls import path, include
# from django_plotly_dash.views import DashAppView
urlpatterns = [
    path('', include('django_plotly_dash.urls')),  # Dash manejará directamente todas las rutas de esta app
    # path('dash/', DashAppView.as_view(), name='dash'),
]
