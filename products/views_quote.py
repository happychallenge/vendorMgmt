from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Vendor, Product, VendorProduct, Quotation
from .forms import QuotationForm, QuotationSimpleForm, QuotationUpdateForm

###############################################
###########    QUOTATION 
###############################################

def save_quotation(request, vendor_id, form, template_name):
    data = dict()
    
    if request.method == 'POST':
        if form.is_valid():
            vendor_id = form.cleaned_data.get('vendor')
            product_id = form.cleaned_data.get('product')
            print(product_id, vendor_id)
            if product_id and vendor_id:
                vendor = get_object_or_404(Vendor, id=vendor_id)
                product = get_object_or_404(Product, cn_name=product_id)
                vendorproduct = VendorProduct.objects.create(vendor=vendor, product=product)

            quotation = form.save(commit=False)
            quotation.vendorproduct = vendorproduct
            quotation.save()

            data["form_is_valid"] = True
            vendor = Vendor.objects.prefetch_related('vendorproduct_set', 'contact_set').get(id=vendor_id)
            data["html_quotation"] = render_to_string('products/includes/ajax_quotation_detail.html', 
                                    {'vendor' : vendor});
    else:
        data["form_is_valid"] = False
        context = { 'form': form }
        data["html_form"] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)


@staff_member_required
def ajax_quotation_add(request, template_name='products/includes/ajax_quotation_add.html'):
    vendor_id = 0
    if request.method == 'POST':
        form = QuotationForm(request.POST)
    else:
        vendor_id = request.GET.get('vendor_id')
        vendor = Vendor.objects.get(id=vendor_id)
        form = QuotationForm(initial={'vendor':vendor_id, 'vendor_name':vendor.cn_name})
    return save_quotation(request, vendor_id, form, template_name)


# 신규로 상품과 Quotaion 을 모두 생성할 때.
@staff_member_required
def quotation_add(request, template_name='products/quotation_add.html'):
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            vendor_id = form.cleaned_data.get('vendor')
            product_id = form.cleaned_data.get('product')
            ptype = form.cleaned_data.get('ptype')

            if product_id and vendor_id:
                vendor = get_object_or_404(Vendor, id=vendor_id)
                product = get_object_or_404(Product, en_name=product_id)
                vendorproduct = VendorProduct.objects.create(vendor=vendor, product=product, ptype=ptype)

            quotation = form.save(commit=False)
            quotation.vendorproduct = vendorproduct
            quotation.save()
            return redirect('chemical:vendor_detail', vendor_id)
    else:
        vendor_id = request.GET.get('vendor_id')
        vendor = Vendor.objects.get(id=vendor_id)
        form = QuotationForm(initial={'vendor':vendor_id, 'vendor_name':vendor.cn_name})
    return render(request, template_name, {'form':form})

# Quotaion 가격만 변경할 때.
@staff_member_required
def quotation_simpleadd(request):
    if request.method == 'POST':
        form = QuotationSimpleForm(request.POST)
        
        if form.is_valid():
            vendor_id = form.cleaned_data.get('vendor')
            quotation = form.cleaned_data.get('quotation')
            newprice = form.cleaned_data.get('newprice')

            if quotation and newprice:
                old = get_object_or_404(Quotation, id=quotation)
                old.status = 'I'        # 기존 견적을 Invlid 
                old.save()

                quotation = Quotation.objects.create(
                    vendorproduct=old.vendorproduct, 
                    price=newprice,
                    effective_date=old.effective_date,
                    # ptype=old.ptype,
                    currency=old.currency,
                    payterm=old.payterm,
                    status='V',
                    comments=old.comments,
                )
    
    return redirect('chemical:vendor_detail', vendor_id)


# Quotaion 가격만 변경할 때.
@staff_member_required
def quotation_update(request, template_name='products/quotation_update.html'):
    if request.method == 'POST':
        quotation_id = request.POST.get('quotation')
        form = QuotationUpdateForm(request.POST)
        oldquotation = Quotation.objects.select_related('vendorproduct__vendor', 
                'vendorproduct__product').get(id=quotation_id)
        
        if form.is_valid():

            if quotation_id and oldquotation:
                oldquotation.status = 'I'        # 기존 견적을 Invlid 
                oldquotation.save()

                newquotation = form.save(commit=False)
                newquotation.vendorproduct = oldquotation.vendorproduct
                newquotation.save()
                return redirect('chemical:vendor_detail', oldquotation.vendorproduct.vendor.id)

            return redirect('chemical:vendor_detail', oldquotation.vendorproduct.vendor.id)
    else:
        quotation_id = request.GET.get('quotation')
        oldquotation = Quotation.objects.select_related('vendorproduct__vendor', 
                'vendorproduct__product').get(id=quotation_id)
        # initial={'quotation':quotation, 'product':product}
        print("INVALID")
        form = QuotationUpdateForm(initial={
                    'quotation':oldquotation.id, 
                    'vendor':oldquotation.vendorproduct.vendor.id, 
                    'vendor_name':oldquotation.vendorproduct.vendor.cn_name,
                    'product':oldquotation.vendorproduct.product.id,
                    'product_name':oldquotation.vendorproduct.product.en_name,
                    'oldprice':oldquotation.price,
                    'oldpayterm':oldquotation.payterm,
                })
    return render(request, template_name, {'form':form})
