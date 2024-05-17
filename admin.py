from django.contrib.gis.db import models
from .models import *
from django.utils.html import format_html
from django.contrib.gis import admin
from django.utils.translation import gettext_lazy as _
from diana.utils import get_fields, DEFAULT_FIELDS, DEFAULT_EXCLUDE
from admin_auto_filters.filters import AutocompleteFilter, AutocompleteFilterFactory
from rangefilter.filters import NumericRangeFilter
from django.contrib.admin import EmptyFieldListFilter

from leaflet.admin import LeafletGeoAdminMixin, LeafletGeoAdmin
from leaflet_admin_list.admin import LeafletAdminListMixin

from django.conf import settings
from PIL import Image as ima
import os
import base64 
from io import StringIO


DEFAULT_LONGITUDE =  11.9900
DEFAULT_LATITUDE  = 58.0000
DEFAULT_ZOOM = 10
MAX_ZOOM = 16
MIN_ZOOM = 5



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['text']
    search_fields = ['text']


@admin.register(TypeOfImage)
class TypeOfImageAdmin(admin.ModelAdmin):
    list_display = ['text']
    search_fields = ['text']


@admin.register(TypeOfDocument)
class TypeOfDocumentAdmin(admin.ModelAdmin):
    list_display = ['text']
    search_fields = ['text']


@admin.register(Technique3D)
class Technique3DAdmin(admin.ModelAdmin):
    list_display = [*get_fields(Technique3D, exclude=['id'])]
    search_fields = ['title', 'type']


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['lastname', 'firstname']
    search_fields = ['firstname', 'lastname']


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    display_raw = True
    list_display = ['name', 'geometry'] # 'parent_id'
    search_fields = ['name']
    filter_horizontal = ['tags']

    # overrides base setting of Leaflet Geo Widget
    settings_overrides = {
       'DEFAULT_CENTER': (DEFAULT_LATITUDE, DEFAULT_LONGITUDE),
       'DEFAULT_ZOOM': DEFAULT_ZOOM,
       'MAX_ZOOM': MAX_ZOOM,
       'MIN_ZOOM': MIN_ZOOM
    }


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'subtitle', 'location'] # [*get_fields(Object3DHop, exclude=['id', 'author'])]
    search_fields = ['name', 'staff_member']
    

@admin.register(Image)
class ImageModel(admin.ModelAdmin):

    fields              = ['image_preview', *get_fields(Image, exclude=['id'])]
    readonly_fields     = ['iiif_file', 'uuid', 'image_preview', *DEFAULT_FIELDS]
    autocomplete_fields = ['staff_member']
    list_display        = ['thumbnail_preview', 'title', 'file']
    search_fields       = ['title', 'file', 'staff_member']
    
    list_per_page = 10

    def image_preview(self, obj):
        return format_html(f'<img src="{settings.IIIF_URL}{obj.iiif_file}/full/full/0/default.jpg" height="300" />')

    def thumbnail_preview(self, obj):
        return format_html(f'<img src="{settings.IIIF_URL}{obj.iiif_file}/full/full/0/default.jpg" height="100" />')

    

@admin.register(Object3DHop)
class Object3DHopAdmin(admin.ModelAdmin):
    list_display = ['title', 'scaled', 'project'] # [*get_fields(Object3DHop, exclude=['id', 'author'])]
    search_fields = ['title', 'staff_member']
    autocomplete_fields = ['preview_image']
    

@admin.register(ObjectPointCloud)
class ObjectPointCloudAdmin(admin.ModelAdmin):
    list_display = ['title', 'scaled', 'preview_image'] # [*get_fields(ObjectPointCloud, exclude=['id', 'author'])]
    search_fields = ['title', 'staff_member']
    autocomplete_fields = ['preview_image']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'size']# [*get_fields(Document, exclude=['id', 'type', 'place'])]
    search_fields = ['title', 'staff_member']