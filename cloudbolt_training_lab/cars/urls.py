from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter

from cloudbolt_training_lab.cars import views

router = SimpleRouter()

router.register(r'manufacturer', views.ManufacturerViewSet, basename='manufacturer')
router.register(r'make', views.MakeViewSet, basename='vehicle')
router.register(r'trim', views.TrimViewSet, basename='trim')

app_name = "cars"
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('api/', include(router.urls)),
    path('api/list/', views.ListView.as_view(), name='list'),
]
