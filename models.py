from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from mixins.models import SlugMixin, ImageMixin
import datetime

class Gallery(SlugMixin):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    members_only = models.BooleanField(default=0)
    slugValue = 'name'
    
    class Meta:
        ordering = ('created_date',)
        verbose_name_plural = 'Galleries'
        
    def get_main(self):
        try:
            return self.image_set.get(is_main=True)
        except Image.DoesNotExist:
            return None
        
    def __unicode__(self):
        return u"%s" % self.name

def get_image_path(instance, filename):
    if instance.gallery:
        return 'media/galleries/%s/%s' % (instance.gallery.slug, filename)
    else:
        return 'media/galleries/unknown/%s' % filename

class Image(ImageMixin):
    description = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey(Gallery, null=True, blank=True)
    is_main = models.BooleanField('Main image for gallery', default=False)
    uploaded_by = models.ForeignKey(User)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('uploaded_date',)
        
    def __unicode__(self):
        return u"%s" % self.image.path
    
    def caption(self):
        from time import strftime
        from django.utils.html import escape
        return "%s <div class='image_caption_specs'>Uploaded on <span class='light'>%s</span> by <span class='light'>%s</span>.</div>" % (escape(self.description), self.uploaded_date.strftime("%B %d, %Y"), self.uploaded_by)

class ImageInline(admin.StackedInline):
    model = Image
    extra = 10

class GalleryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name', 'description', 'created_by', 'members_only']}),
    ]
    inlines = [ImageInline,]
    list_display = ('name','created_date')
    list_filter = ['created_date']
    search_fields = ['name','description']
    date_hierarchy = 'created_date'

admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Image)