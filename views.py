from django.contrib.auth.models import User
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from gallery.models import *

def gallery_404():
    return HttpResponseRedirect(reverse('gallery.views.default'))

def render_with_context(request, url, vars):
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    
    return render_to_response(url, vars, context_instance=RequestContext(request))

def default(request, template_name='gallery/defaults/default.html'):
    galleries = Gallery.objects.filter(members_only__lte=request.user.is_authenticated())
    return render_with_context(request, template_name, { 'galleries': galleries })

def determine_images(request, gallery):
    page = 1
    if request.GET.has_key('p'):
        try:
            page = int(request.GET['p'])
        except ValueError:
            pass
    per_page = 15
    if hasattr(settings, 'GALLERY_IMAGES_PER_PAGE'):
        per_page = int(settings.GALLERY_IMAGES_PER_PAGE)
    start = (page - 1) * per_page
    end = start + per_page
    images = gallery.image_set.all()#[start:end+1]
    for spot, image in enumerate(images):
        if spot >= start and spot < end:
            images[spot].showImage = True
    has_next = 0
    if len(images) > end:
        has_next = page + 1
    has_prev = page - 1
    #images = images[:per_page]
    return [images, has_next, has_prev]

def view_gallery(request, template_name='gallery/defaults/view_gallery.html', **kwargs):
    try:
        if kwargs.has_key('gallery_id'):
            gallery = Gallery.objects.get(pk=kwargs['gallery_id'], members_only__lte=request.user.is_authenticated())
        elif kwargs.has_key('slug'):
            gallery = Gallery.objects.get(slug__exact=kwargs['slug'], members_only__lte=request.user.is_authenticated())
        images, has_next, has_prev = determine_images(request, gallery)
        return render_with_context(request, template_name, { 'title': gallery.name, 'gallery': gallery, 'images': images, 'has_next': has_next, 'has_prev': has_prev })
    except Gallery.DoesNotExist:
        return gallery_404()
    