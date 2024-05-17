# from django.db import models
from django.contrib.gis.db import models
import diana.abstract.models as abstract
from django.utils.translation import gettext_lazy as _
from diana.storages import OriginalFileStorage
from diana.abstract.models import get_original_path
from ckeditor.fields import RichTextField
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from datetime import date
from .validators import validate_file_extension, validate_image_extension
# Create your models here.

from django.contrib.postgres.fields import ArrayField
def get_list_zeros():
    return [0.0, 0.0, 0.0]
def get_min_max_default():
    return [-180, 180]


class Tag(abstract.AbstractTagModel):
    
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return str(self)


class TypeOfImage(abstract.AbstractTagModel):

    class Meta:
        verbose_name = _("Type of image")
        verbose_name_plural = _("Types of image")

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return str(self)
    
    
class TypeOfDocument(abstract.AbstractTagModel):

    class Meta:
        verbose_name = _("Type of document")
        verbose_name_plural = _("Types of document")

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return str(self)
    

class Technique3D(abstract.AbstractTagModel):

    class Meta:
        verbose_name = _("3D technique")
        verbose_name_plural = _("3D techniques")

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return str(self)
    

class StaffMember(abstract.AbstractBaseModel):
    firstname = models.CharField(max_length=256, blank=True, null=True)
    lastname = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"


class Location(abstract.AbstractBaseModel):
    
    name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("name"), help_text=_("Please enter the name of the location"))
    geometry = models.GeometryField(verbose_name=_("geometry"), blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, help_text=_("Tags attached to the location"))
    
    def __str__(self) -> str:
        return self.name


class Project(abstract.AbstractBaseModel):
    name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("name"), help_text=_("Please enter the name of the project"))
    subtitle = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("subtitle"), default = None)
    location = models.ForeignKey(Location, verbose_name=_("location"), blank=True, null=True, on_delete=models.SET_NULL, related_name="projects_in_location")
    staff_member = models.ManyToManyField(StaffMember, blank=True, help_text=_("Staff members working on the project"), related_name="projects_for_member")
    description = RichTextField(null=True, blank=True, help_text=("Descriptive text about the project"))
    
    def __str__(self) -> str:
        return self.name
    

class Image(abstract.AbstractTIFFImageModel):

    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("title"))
    staff_member = models.ManyToManyField(StaffMember, blank=True, verbose_name=_("Staff member"), help_text=_("staff member responsible for this piece of data"))
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("Project attached to this media"), related_name="image_in_project")
    type_of_image = models.ManyToManyField(TypeOfImage, blank=True)
    description = RichTextField(null=True, blank=True, help_text=("Descriptive text about the images"))
    date = models.DateField(default=date.today, help_text=_("Date in which the image was taken"))
    location = models.ForeignKey(Location, verbose_name=_("Location"), blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.title}"
        

class Object3DHop(abstract.AbstractBaseModel):
    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("Title"))
    staff_member = models.ManyToManyField(StaffMember, blank=True, verbose_name=_("Staff member"), help_text=_("staff member responsible for this piece of data"))
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("Project attached to this media"), related_name="object3dhop_in_project")
    url_public = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("URL for API call"))
    url_optimized = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("URL of optimized model"))
    url_full_resolution = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("URL of full resolution model"))
    triangles_optimized = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Triangles (optimized)"), help_text=_("number of triangles of the optimized mesh, e.g.: 250 millions"))
    triangles_full_resolution = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Triangles (full resolution)"), help_text=_("number of triangles of the full resolution mesh, e.g.: 1.3 billions"))
    description = RichTextField(null=True, blank=True, help_text=("Descriptive text about the 3D object"))
    date = models.DateField(default=date.today, help_text=_("Date in which the 3D object was created"))
    technique = models.ForeignKey(Technique3D, null=True, blank=True, on_delete=models.SET_NULL, help_text=_("Technique used to generate the 3D model"))
    scaled = models.BooleanField(help_text=_("If the model is scaled, please check the box"), default=False)
    
    trackball_start = ArrayField(models.FloatField(), size=6, default=list)
    start_angle = ArrayField(models.FloatField(), size=2, default=list, verbose_name=_("Start angle (phi, theta)"), help_text=_("Format: 2 comma-separated float numbers, e.g.: 0.0, 1.1"))
    start_distance = models.FloatField(null=True, blank=True, verbose_name=_("initial mesh distance"))
    start_pan = ArrayField(models.FloatField(), size=3, default=get_list_zeros, help_text=_("Format: 3 comma-separated float numbers, e.g.: 0.0, 1.1, 2.2"))
    min_max_phi = ArrayField(models.FloatField(), size=2, default=get_min_max_default, verbose_name=_("maximal vertical camera angles"), help_text=_("Format: 2 comma-separated float numbers, e.g.: 0.0, 1.1"))
    min_max_theta = ArrayField(models.FloatField(), size=2, default=get_min_max_default, verbose_name=_("maximal horizontal camera angles"), help_text=_("Format: 2 comma-separated float numbers, e.g.: 0.0, 1.1"))

    preview_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, verbose_name=_("Location"), blank=True, null=True, on_delete=models.SET_NULL)


    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = _("Object 3D-hop")
        verbose_name_plural = _("Objects 3D-hop")


class ObjectPointCloud(abstract.AbstractBaseModel):
    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("title"))
    subtitle = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("subtitle"))
    staff_member = models.ManyToManyField(StaffMember, blank=True, verbose_name=_("Staff member"), help_text=_("staff member responsible for this piece of data"))
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("Project attached to this media"), related_name="pointcloud_in_project")
    url_public = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("URL for API call"))
    url_optimized = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("URL of optimized model"))
    url_full_resolution = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("URL of full resolution model"))
    points_optimized = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Points (optimized)"), help_text=_("number of points of the optimized models, e.g.: 250 millions"))
    points_full_resolution = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Points (full resolution)"),  help_text=_("number of points of the full resolution model, e.g.: 1.3 billions"))
    description = RichTextField(null=True, blank=True, help_text=("Descriptive text about the 3D object"))
    date = models.DateField(default=date.today, help_text=_("Date in which the 3D object was created"))
    technique = models.ForeignKey(Technique3D, null=True, blank=True, on_delete=models.SET_NULL, help_text=_("Technique used to generate the 3D model"))
    scaled = models.BooleanField(help_text=_("If the model is scaled, please check the box"), default=False)

    camera_position = ArrayField(models.FloatField(), size=3, default=list, help_text=_("Format: 3 comma-separated float numbers, e.g.: 0.0, 1.1, 2.2"))
    look_at = ArrayField(models.FloatField(), size=3, default=list, help_text=_("Format: 3 comma-separated float numbers, e.g.: 0.0, 1.1, 2.2"))

    preview_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, verbose_name=_("Location"), blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = _("Object Pointcloud")
        verbose_name_plural = _("Objects Pointcloud")


class Document(abstract.AbstractBaseModel):
    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("title"))
    staff_member = models.ManyToManyField(StaffMember, blank=True, verbose_name=_("Staff member"), help_text=_("staff member responsible for this piece of data"))
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("Project attached to this media"), related_name="document_in_project")
    upload = models.FileField(null=True, blank=True, storage=OriginalFileStorage, upload_to=get_original_path, verbose_name=_("file"), validators=[validate_file_extension])
    type = models.ManyToManyField(TypeOfDocument, blank=True, verbose_name=_("Type of document: Report, Thesis, etc"))
    size = models.FloatField(null=True, blank=True, help_text=_("Document size in mb"), default=None)
    description = RichTextField(null=True, blank=True, help_text=("Descriptive text about the document"))
    date = models.DateField(default=date.today, help_text=_("Date in which the document was created"))
    location = models.ForeignKey(Location, verbose_name=_("Location"), blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = _("Document")