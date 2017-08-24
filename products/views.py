from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.contrib import messages

from .models import Vendor, Product, Contact, VendorProduct, Sourcing
from .forms import VendorForm, ProductForm, ContactForm
from .forms import SourcingPriceForm, SourcingProductForm, SourcingSimpleForm
# Create your views here.

EXCHANGE_RATE = 6.66

###############################################
########### VENDOR 
###############################################
@login_required
def vendor_list(request):
    vendor_list = Vendor.objects.prefetch_related('tags').filter(gprelation='CURRENT')
    context = {
        'vendor_list': vendor_list,
        'active' : 'Vendor',
    }
    return render(request, 'products/vendor_list.html', context)


@login_required
def vendor_detail(request, id):
    # vendor = get_object_or_404(vendor, id=id)
    vendor = Vendor.objects.prefetch_related('vendorproduct_set', 'contact_set').get(id=id)
    vendorproducts = VendorProduct.objects.prefetch_related('quotation_set').filter(vendor=vendor)
    context = {
        'vendor': vendor, 
        'vendorproducts': vendorproducts,
        'active' : 'Vendor',
    }
    return render(request, 'products/vendor_detail.html', context)


@staff_member_required
def vendor_add(request, template_name='products/vendor_add.html'):
    if request.method == 'POST':
        form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, 'Vendor was successfully added!!!')
            return redirect('chemical:sourcingvendor_list')
    else:
        form = VendorForm()
        context = {
            'form':form,
            'active' : 'Vendor',
        }
    return render(request, template_name, context)


@staff_member_required
def vendor_update(request, id, template_name='products/vendor_add.html'):
    vendor = get_object_or_404(Vendor, id=id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, 'Vendor was successfully updated!!!')
            return redirect('chemical:sourcingvendor_list')
    else:
        form = VendorForm(instance=vendor)
        context = {
            'form':form,
            'active' : 'Vendor',
        }
    return render(request, template_name, context )


###############################################
########### SOURCING 
###############################################
@login_required
def sourcingvendor_list(request):
    vendor_list = Vendor.objects.prefetch_related('tags').all()
    # vendor_list = Vendor.objects.prefetch_related('tags').exclude(gprelation='CURRENT')
    context = {
        'vendor_list': vendor_list,
        'active' : 'Sourcing',
    }
    return render(request, 'products/sourcingvendor_list.html', context)

@login_required
def sourcingvendor_detail(request, id):
    # vendor = get_object_or_404(vendor, id=id)
    vendor = Vendor.objects.prefetch_related('vendorproduct_set', 'contact_set').get(id=id)
    vendorproducts = VendorProduct.objects.prefetch_related('sourcing_set').filter(vendor=vendor)
    context = {
        'vendor': vendor, 
        'vendorproducts': vendorproducts,
        'active' : 'Sourcing',
    }
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

            buying_price = form.cleaned_data.get('buying_price')

            if product_id and vendor_id:
                vendor = get_object_or_404(Vendor, id=vendor_id)
                product = get_object_or_404(Product, en_name=product_id)
                vendorproduct, created = VendorProduct.objects.get_or_create(vendor=vendor, product=product, ptype=ptype)

                sourcing = form.save(commit=False)
                sourcing.vendorproduct = vendorproduct
                rate_taxrefund = int(product.rate_taxrefund)/100
                sourcing.usd_price = (buying_price - 
                                    (buying_price/1.17*rate_taxrefund))/EXCHANGE_RATE
                sourcing.save()
                return redirect('chemical:sourcingvendor_detail', vendor_id)
    else:
        vendor_id = request.GET.get('vendor_id')
        vendor = get_object_or_404(Vendor, id=vendor_id)
        form = SourcingProductForm(initial={
                    'vendor':vendor_id, 
                    'vendor_name':vendor.en_name
                })
        context = {
            'form': form, 
            'active' : 'Sourcing',
        }
    return render(request, template_name, context)


# 신규 Sourcing Price 만  추가할 때.
@staff_member_required
def sourcing_priceadd(request, template_name='products/sourcing_priceadd.html'):
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor')
        product_id = request.POST.get('product')
        ptype = request.POST.get('ptype')
        form = SourcingPriceForm(request.POST)

        if form.is_valid():

            buying_price = form.cleaned_data.get('buying_price')
            vendorproduct = VendorProduct.objects.select_related("vendor").filter(
                    vendor=vendor_id, product=product_id, ptype=ptype
                )[0]
            # print("Form Error : = ", form.)
            sourcing = form.save(commit=False)
            sourcing.vendorproduct = vendorproduct
            rate_taxrefund = int(vendorproduct.product.rate_taxrefund)/100
            sourcing.usd_price = (buying_price - 
                                (buying_price/1.17*rate_taxrefund))/EXCHANGE_RATE
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
        context = {
            'form': form, 
            
            'active' : 'Sourcing',
        }
    return render(request, template_name, context)


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

                rate_taxrefund = int(old.vendorproduct.product.rate_taxrefund)/100
                usd_price = (newprice - 
                                    (newprice/1.17*rate_taxrefund))/EXCHANGE_RATE

                sourcing = Sourcing.objects.create(
                    vendorproduct=old.vendorproduct, 
                    buying_price=newprice,
                    usd_price=usd_price,
                    effective_date=old.effective_date,
                    payterm=old.payterm,
                    status='V',
                    comments=old.comments,
                )
    
    return redirect('chemical:sourcingvendor_detail', vendor_id)


@login_required
def sourcingproduct_list(request):
    product_list = Product.objects.prefetch_related("vendorproduct_set").all()
    context = {
        'product_list': product_list,
        'active' : 'SourcingProduct',
    }
    return render(request, 'products/sourcingproduct_list.html', context)

@login_required
def sourcingproduct_detail(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product,
        'active' : 'SourcingProduct',
    }
    return render(request, 'products/sourcingproduct_detail.html', context)



###############################################
########### PRODUCT 
###############################################
from datetime import date

@login_required
def product_list(request):
    product_list = Product.objects.all()
    today = date.today()
    year = today.year
    month = today.month 
    if month < 11:
        year_month = [ "{}/{}".format(year, x) for x in range(month+1, month+4) ]

    context = {
        'product_list': product_list,
        'active' : 'Product',
        'year_month':year_month,
    }
    return render(request, 'products/product_list.html', context)


@login_required
def product_detail(request, id):
    product = Product.objects.prefetch_related('vendorproduct_set').get(id=id)
    context = {
        'product': product,
        'active' : 'Product',
    }
    return render(request, 'products/product_detail.html', context)


@staff_member_required
def product_add(request, template_name='products/product_add.html'):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'product was successfully added!!!')
            return redirect('chemical:sourcingproduct_list')
    else:
        form = ProductForm()
        context = {
            'form': form,
            'active' : 'Product',
        }
    return render(request, template_name, context)

@staff_member_required
def product_update(request, id, template_name='products/product_add.html'):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'product was successfully updated!!!')
            return redirect('chemical:sourcingproduct_list')
    else:
        form = ProductForm(instance=product)
        context = {
            'form': form,
            'active' : 'Product',
        }
    return render(request, template_name, context)


###############################################
########### CONTACT 
###############################################
@login_required
def contact_list(request):
    contact_list = Contact.objects.select_related('vendor').all()
    context = {
        'contact_list': contact_list,
        'active' : 'Contact',
    }
    return render(request, 'products/contact_list.html', context)


@staff_member_required
def contact_add(request, vendor_id, template_name='products/contact_add.html'):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        vendor = get_object_or_404(Vendor, id=vendor_id)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.vendor = vendor
            contact.save()

            messages.success(request, '{} was successfully created!!!'.format(contact.en_name))
            return redirect('chemical:sourcingvendor_detail', vendor_id)
    else:
        form = ContactForm()
        context = {
            'form': form,
            'active' : 'SOURCING',
        }
    return render(request, template_name, context)


@staff_member_required
def contact_update(request, id, template_name='products/contact_add.html'):
    contact = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)

        if form.is_valid():
            contact = form.save(commit=True)
            contact.save()

            messages.success(request, '{} was successfully updated!!!'.format(contact.en_name))
            return redirect('chemical:sourcingvendor_detail', contact.vendor.id)
    else:
        form = ContactForm(instance=contact)
    return render(request, template_name, {
            'form': form,
            'active' : 'SOURCING',
        })



