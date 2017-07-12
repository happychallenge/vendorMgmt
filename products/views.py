from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import Vendor, Product, Contact, VendorProduct, Sourcing
from .forms import VendorForm, ProductForm, ContactForm
from .forms import SourcingPriceForm, SourcingProductForm, SourcingSimpleForm
# Create your views here.

###############################################
########### VENDOR 
###############################################
@login_required
def vendor_list(request):
    vendor_list = Vendor.objects.prefetch_related('tags').all()
    return render(request, 'products/vendor_list.html', {'vendor_list': vendor_list})


@login_required
def vendor_detail(request, id):
    # vendor = get_object_or_404(vendor, id=id)
    vendor = Vendor.objects.prefetch_related('vendorproduct_set', 'contact_set').get(id=id)
    vendorproducts = VendorProduct.objects.prefetch_related('quotation_set').filter(vendor=vendor)
    return render(request, 'products/vendor_detail.html', 
            {'vendor': vendor, 'vendorproducts': vendorproducts})


@staff_member_required
def vendor_add(request, template_name='products/vendor_add.html'):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, 'Vendor was successfully added!!!')
            return redirect('chemical:vendor_list')
    else:
        form = VendorForm()
    return render(request, template_name, {'form':form})


@staff_member_required
def vendor_update(request, id, template_name='products/vendor_add.html'):
    vendor = get_object_or_404(Vendor, id=id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, 'Vendor was successfully updated!!!')
            return redirect('chemical:vendor_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, template_name, {'form':form})


###############################################
########### SOURCING 
###############################################
@login_required
def sourcingvendor_list(request):
    vendor_list = Vendor.objects.prefetch_related('tags').all()
    return render(request, 'products/sourcingvendor_list.html', {'vendor_list': vendor_list})

@login_required
def sourcingvendor_detail(request, id):
    # vendor = get_object_or_404(vendor, id=id)
    vendor = Vendor.objects.prefetch_related('vendorproduct_set', 'contact_set').get(id=id)
    vendorproducts = VendorProduct.objects.prefetch_related('sourcing_set').filter(vendor=vendor)
    return render(request, 'products/sourcingvendor_detail.html', 
            {'vendor': vendor, 'vendorproducts': vendorproducts})


# 신규로 상품과 가격(RMB) 을 모두 생성할 때.
@staff_member_required
def sourcing_productadd(request, template_name='products/sourcing_productadd.html'):
    if request.method == 'POST':
        form = SourcingProductForm(request.POST)
        
        if form.is_valid():
            vendor_id = form.cleaned_data.get('vendor')
            product_id = form.cleaned_data.get('product')
            ptype = form.cleaned_data.get('ptype')

            if product_id and vendor_id:
                vendor = get_object_or_404(Vendor, id=vendor_id)
                product = get_object_or_404(Product, en_name=product_id)
                vendorproduct, created = VendorProduct.objects.get_or_create(vendor=vendor, product=product, ptype=ptype)

                quotation = form.save(commit=False)
                quotation.vendorproduct = vendorproduct
                quotation.save()
                return redirect('chemical:sourcingvendor_detail', vendor_id)
    else:
        vendor_id = request.GET.get('vendor_id')
        vendor = get_object_or_404(Vendor, id=vendor_id)
        form = SourcingProductForm(initial={
                    'vendor':vendor_id, 
                    'vendor_name':vendor.en_name
                })
    return render(request, template_name, {'form':form})


# 신규 Sourcing Price 만  추가할 때.
@staff_member_required
def sourcing_priceadd(request, template_name='products/sourcing_priceadd.html'):
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor')
        product_id = request.POST.get('product')
        ptype = request.POST.get('ptype')
        form = SourcingPriceForm(request.POST)

        if form.is_valid():

            vendorproduct = VendorProduct.objects.select_related("vendor").filter(
                    vendor=vendor_id, product=product_id, ptype=ptype
                )[0]
            # print("Form Error : = ", form.)
            sourcing = form.save(commit=False)
            sourcing.vendorproduct = vendorproduct
            sourcing.save()
            return redirect('chemical:sourcingvendor_detail', vendorproduct.vendor_id)
    else:
        vendorproduct_id = request.GET.get('vendorproduct')
        vendorproduct = VendorProduct.objects.select_related("vendor", "product").get(id=vendorproduct_id)
        form = SourcingPriceForm(initial={
                    'vendor': vendorproduct.vendor_id,
                    'product': vendorproduct.product_id,
                    'vendor_name': vendorproduct.vendor.en_name,
                    'product_name': vendorproduct.product.en_name,
                    'ptype': vendorproduct.ptype,
                })
    return render(request, template_name, {'form':form})


# Quotaion 가격만 변경할 때.
@staff_member_required
def sourcing_simpleadd(request):
    if request.method == 'POST':
        form = SourcingSimpleForm(request.POST)
        
        if form.is_valid():
            sourcing = form.cleaned_data.get('sourcing')
            vendor_id = form.cleaned_data.get('vendor')
            newprice = form.cleaned_data.get('newprice')

            if sourcing and newprice:
                old = get_object_or_404(Sourcing, id=sourcing)
                old.status = 'I'        # 기존 견적을 Invlid 
                old.save()

                sourcing = Sourcing.objects.create(
                    vendorproduct=old.vendorproduct, 
                    buying_price=newprice,
                    effective_date=old.effective_date,
                    payterm=old.payterm,
                    status='V',
                    comments=old.comments,
                )
    
    return redirect('chemical:sourcingvendor_detail', vendor_id)


###############################################
########### PRODUCT 
###############################################
@login_required
def product_list(request):
    product_list = Product.objects.all()
    return render(request, 'products/product_list.html', {'product_list': product_list})

@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})

@staff_member_required
def product_add(request, template_name='products/product_add.html'):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'product was successfully added!!!')
            return redirect('chemical:product_list')
    else:
        form = ProductForm()

    return render(request, template_name, {'form':form})

@staff_member_required
def product_update(request, id, template_name='products/product_add.html'):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'product was successfully updated!!!')
            return redirect('chemical:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, template_name, {'form':form})


###############################################
########### CONTACT 
###############################################
@login_required
def contact_list(request):
    contact_list = Contact.objects.select_related('vendor').all()
    return render(request, 'products/contact_list.html', {'contact_list': contact_list})


@staff_member_required
def contact_add(request, template_name='products/contact_add.html'):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save()
            messages.success(request, 'Contact was successfully added!!!')
            return redirect('chemical:contact_list')
    else:
        form = ContactForm()

    return render(request, template_name, {'form':form})


@staff_member_required
def contact_update(request, id, template_name='products/contact_add.html'):
    contact = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            messages.success(request, 'contact was successfully updated!!!')
            return redirect('chemical:contact_list')
    else:
        form = ContactForm(instance=contact)

    return render(request, template_name, {'form':form})



