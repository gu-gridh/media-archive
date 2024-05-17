from unittest.mock import DEFAULT
from . import models, serializers
from django.db.models import Q
from diana.abstract.views import DynamicDepthViewSet, GeoViewSet
from diana.abstract.models import get_fields, DEFAULT_FIELDS
from django.db.models import Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
import json
    

class LocationViewSet(GeoViewSet):
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all().order_by('id')
    filterset_fields = get_fields(models.Location, exclude=DEFAULT_FIELDS + ['geometry'])


class ProjectViewSet(DynamicDepthViewSet):

    queryset = models.Project.objects.all().order_by('id')
    serializer_class = serializers.ProjectSerializer
    filterset_fields = get_fields(models.Project, exclude=DEFAULT_FIELDS)#, 'images_count', 'threedhop_count', 'pointcloud_count'])
    search_fields = ["name"]


class IIIFImageViewSet(DynamicDepthViewSet):
    """
    retrieve:
    Returns a single image instance.

    list:
    Returns a list of all the existing images in the database, paginated.

    count:
    Returns a count of the existing images after the application of any filter.
    """
    
    queryset = models.Image.objects.all().order_by('id')
    serializer_class = serializers.TIFFImageSerializer
    filterset_fields = get_fields(models.Image, exclude=DEFAULT_FIELDS + ['iiif_file', 'file'])



class Object3DHopViewSet(DynamicDepthViewSet):
    
    queryset = models.Object3DHop.objects.all()
    serializer_class = serializers.Object3DHopSerializer
    filterset_fields = get_fields(models.Object3DHop, exclude=DEFAULT_FIELDS+['preview_image', 'trackball_start', 
                                                                              'start_angle', 'start_pan', 
                                                                              'min_max_phi', 'min_max_theta'])


class ObjectPointcloudViewSet(DynamicDepthViewSet):
    
    queryset = models.ObjectPointCloud.objects.all()
    serializer_class = serializers.ObjectPointCloudSerializer
    filterset_fields = get_fields(models.ObjectPointCloud, exclude=DEFAULT_FIELDS+['preview_image', 'camera_position', 
                                                                                   'look_at'])


class DocumentViewSet(DynamicDepthViewSet):
    
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    filterset_fields = get_fields(models.Document, exclude=DEFAULT_FIELDS+['upload'])