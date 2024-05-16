from diana.abstract.serializers import DynamicDepthSerializer, GenericSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import SerializerMethodField
from . import models
from diana.utils import get_fields, DEFAULT_FIELDS
from .models import *


class TIFFImageSerializer(DynamicDepthSerializer):
    
    class Meta:
        model = Image
        fields = get_fields(Image, exclude=DEFAULT_FIELDS)+ ['id']
        
    
class LocationSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Location
        fields = get_fields(Location, exclude=DEFAULT_FIELDS)+ ['id']
        geo_field = 'geometry'
        depth = 1
        

class StaffMemberSerializer(DynamicDepthSerializer):

    class Meta:
        model = StaffMember
        fields = get_fields(StaffMember, exclude=DEFAULT_FIELDS)+ ['id']


class Object3DHopSerializer(DynamicDepthSerializer):
    
    class Meta:
        model = Object3DHop
        fields = get_fields(Object3DHop, exclude=DEFAULT_FIELDS)+ ['id']


class ObjectPointCloudSerializer(DynamicDepthSerializer):

    class Meta:
        model = ObjectPointCloud
        fields = get_fields(ObjectPointCloud, exclude=DEFAULT_FIELDS)+ ['id']


class DocumentSerializer(DynamicDepthSerializer):
    type_names = SerializerMethodField()
    
    class Meta:
        model = Document
        fields = get_fields(Document, exclude=DEFAULT_FIELDS)+ ['id', 'type_names']

    def get_type_names(self, obj):
        type_names = []
        types = obj.type.all()
        for type in types:
            type_names.append(type.text)
        return type_names