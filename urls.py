from django.urls import path, include
from rest_framework import routers
from . import views
import diana.utils as utils


router = routers.DefaultRouter()
endpoint = utils.build_app_endpoint("mediaarchive")
documentation = utils.build_app_api_documentation("mediaarchive", endpoint)

router.register(rf'{endpoint}/geojson/location', views.LocationViewSet, basename='place on geojson')
router.register(rf'{endpoint}/image', views.IIIFImageViewSet, basename='image')
router.register(rf'{endpoint}/document', views.DocumentViewSet, basename='document')
router.register(rf'{endpoint}/object3dhop', views.Object3DHopViewSet, basename='object 3D hop')
router.register(rf'{endpoint}/objectpointcloud', views.ObjectPointcloudViewSet, basename='object point cloud')


urlpatterns = [
    path('', include(router.urls)),

    # Automatically generated views
    *utils.get_model_urls('mediaarchive', endpoint, 
        exclude=['image', 'location', 'document', 'object3dhop', 'objectpointcloud']),

    *utils.get_model_urls('mediaarchive', f'{endpoint}', exclude=['image', 'location', 'document', 'object3dhop', 'objectpointcloud']),
    *documentation
]