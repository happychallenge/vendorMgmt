from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from decorators import ajax_required
from products.models import Vendor
from .models import Comment
from .forms import CommentForm

# Create your views here.
@ajax_required
def ajax_comment_add(request, vendor_id):
    data = dict()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        vendor = get_object_or_404(Vendor, id=vendor_id)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.vendor = vendor
            comment.save()

            data['form_is_valid'] = True
            comment_list = Comment.objects.filter(vendor=vendor)
            context = { 'comment_list': comment_list, 'vendor': vendor}
            data['html_result'] = render_to_string('products/partial/ajax_comment_list.html', context)
            
        else:
            data['form_is_valid'] = False
    else:
        vendor = get_object_or_404(Vendor, id=vendor_id)
        form = CommentForm()
    
    data['html_form'] = render_to_string('products/partial/ajax_comment_add.html', {
                'form': form, 'vendor':vendor 
        }, request=request)
    return JsonResponse(data)

@ajax_required
def ajax_comment_update(request, comment_id):
    data = dict()
    comment = get_object_or_404(Comment, id=comment_id)
    vendor = comment.vendor

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            comment = form.save()
            comment.save()

            data['form_is_valid'] = True
            comment_list = Comment.objects.filter(vendor=vendor)
            context = { 'comment_list': comment_list, 'vendor': vendor}
            data['html_result'] = render_to_string('products/partial/ajax_comment_list.html', context)
            
        else:
            data['form_is_valid'] = False
    else:
        form = CommentForm(instance=comment)
    
    data['html_form'] = render_to_string('products/partial/ajax_comment_update.html', {
                'form': form, 'vendor':vendor 
        }, request=request)
    return JsonResponse(data)