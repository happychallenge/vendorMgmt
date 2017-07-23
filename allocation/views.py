from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from products.models import Product, Vendor
from .models import DemandClient, Demand, Supply
from .forms import DemandForm, DemandClientFormSet5, DemandClientFormSet
from .forms import SupplyForm, SupplyVendorFormSet, SupplyVendorFormSet5


# Create your views here.
from datetime import date

def product_demandsupply_list(request):

    product_list = Product.objects.all()
    today = date.today()
    year = today.year
    month = today.month 
    if month < 10:
        year_month = [ "{}/{}".format(year, x) for x in range(month, month+4) ]
    # if month == 10:

    return render(request, 'allocation/product_list.html', 
            {'product_list':product_list, 'year_month':year_month})


def product_demandsupply_detail(request, id, year_month):
    product = get_object_or_404(Product, id=id)
    year, month = year_month.split('/')

    try:
        demand = Demand.objects.prefetch_related('demandclient_set').get(product=product,
                        year=int(year), month=int(month))
        supply = Supply.objects.get(demand=demand)
    except Demand.DoesNotExist:
        raise Http404

    demand_form = DemandForm(instance=demand)
    demandformset = DemandClientFormSet(instance=demand)

    supply_form = SupplyForm(instance=supply)
    supplyformset = SupplyVendorFormSet(instance=supply)

    return render(request, 'allocation/product_demandsupply_detail.html',{
                'demand_form':demand_form, 'demandformset':demandformset,
                'supply_form':supply_form, 'supplyformset':supplyformset,
                'product': product.id, 'year':year, 'month':month,
                'supply':supply.id,
            })


def client_demand_add(request):

    if request.method == 'POST':
        product_id = request.POST.get('product')
        product = get_object_or_404(Product, id=product_id)
        year = request.POST.get('year')
        month = request.POST.get('month')
        year_month = "{}/{}".format(year, month)

        try:
            demand = get_object_or_404(Demand, product=product, 
                            year=int(year), month=int(month))
        except Exception:
            demand = Demand()

        demand_form = DemandForm(request.POST, instance=demand)

        if demand_form.is_valid():
            created_demand = demand_form.save(commit=False)
            formset = DemandClientFormSet5(request.POST, instance=created_demand)
            
            if formset.is_valid():
                created_demand.save()
                formset.save()
                return redirect('allocation:product_demandsupply_detail', 
                        id=product_id, year_month=year_month)
    else:
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        year_month = request.GET.get('year_month')
        year, month = year_month.split('/')

        try:
            demand = get_object_or_404(Demand, product=product, 
                            year=int(year), month=int(month))
        except Exception:
            demand = Demand()

        demand_form = DemandForm(instance=demand)
        formset = DemandClientFormSet5(instance=demand)
        
    return render(request, 'allocation/client_demand_add.html', 
            {'demand_form':demand_form, 'formset':formset})


def vendor_supply_add(request):
    if request.method == 'POST':
        demand_id = request.POST.get('demand')
        demand = get_object_or_404(Demand, id=demand_id)
        supply = get_object_or_404(Supply, demand=demand)
        supply_form = SupplyForm(request.POST, instance=supply)
        year=supply.demand.year
        month=supply.demand.month
        year_month = "{}/{}".format(year, month)

        if supply_form.is_valid():
            created_supply = supply_form.save(commit=False)
            formset = SupplyVendorFormSet5(request.POST, instance=created_supply)
            
            if formset.is_valid():
                created_supply.save()
                formset.save()
                return redirect('allocation:product_demandsupply_detail', 
                        id=supply.demand.product.id, year_month=year_month)
    else:
        supply_id = request.GET.get('supply')
        supply = get_object_or_404(Supply, id=supply_id)
        demand = get_object_or_404(Demand, id=supply.demand.id)

        vendor_list = Vendor.objects.filter(vendorproduct__product=demand.product)
        supply_form = SupplyForm(instance=supply)
        demand_form = DemandForm(instance=demand)
        formset = SupplyVendorFormSet5(instance=supply)
        for form in formset:
            form.fields['vendor'].queryset = vendor_list
        
    return render(request, 'allocation/vendor_supply_add.html', 
            { 'demand_form':demand_form, 'supply_form':supply_form, 'formset':formset})
