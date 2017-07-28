from django.shortcuts import render, redirect, get_list_or_404

from products.models import Product, Quotation
from .models import POrder, POrderItem
from .forms import POrderForm, POrderItemForm, POrderItemFormSet, PayConditionForm
from .forms import PayConditionFormSet, ShippingForm, ShippingFormSet
# Create your views here.
def porder_list(request):
    porder_list = POrder.objects.all().order_by('-contract_date')

    return render(request, 'order/porder_list.html', {
            'porder_list': porder_list
        })


def porder_detail(request, id):
    porder = POrder.objects.prefetch_related("porderitem_set", "paycondition").get(id=id)

    return render(request, 'order/porder_detail.html', {
            'porder': porder
        })


def porder_add(request):

    if request.method == 'POST':
        form = POrderForm(request.POST)

        if form.is_valid():
            created_porder = form.save(commit=False)
            formset = PayConditionFormSet(request.POST, instance=created_porder)

            if formset.is_valid():
                created_porder.save()
                formset.save()

            return redirect("order:porderitem_add", id=created_porder.id)
    else:
        form = POrderForm()
        formset = PayConditionFormSet()

    return render(request, 'order/porder_add.html', {
            'form':form, 'formset':formset
        })


def porderitem_add(request, id):
    porder = POrder.objects.select_related('vendor').prefetch_related('porderitem_set').get(id=id)

    if request.method == 'POST':
        order_form = POrderForm(request.POST, instance=porder)

        if order_form.is_valid():
            created_order = order_form.save(commit=False)
            payformset = PayConditionFormSet(request.POST, instance=porder)
            formset = POrderItemFormSet(request.POST, instance=created_order)

            if formset.is_valid() and payformset.is_valid():
                created_order.save()
                payformset.save()
                formset.save()
                return redirect('order:porder_detail', id=id)

    else:
        order_form = POrderForm(instance=porder)
        payformset = PayConditionFormSet(instance=porder)
        orderformset = POrderItemFormSet(instance=porder)

        product_list = Product.objects.filter(vendorproduct__vendor=porder.vendor)
        for form in orderformset:
            form.fields['product'].queryset = product_list

    return render(request, 'order/porderitem_add.html', {
                'order_form':order_form, 'payformset':payformset,
                'orderformset':orderformset, 'order_id': porder.id,
            })


def shipping_add(request, id):
    porder = POrder.objects.select_related('vendor').prefetch_related('porderitem_set').get(id=id)

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)

        if shipping_form.is_valid():
            shipping = shipping_form.save(commit=False)
            shipping.porder = porder
            shipping.save()

            return redirect('order:porder_detail', id=id)
    else:
        order_form = POrderForm(instance=porder)
        payformset = PayConditionFormSet(instance=porder)
        orderformset = POrderItemFormSet(instance=porder)
        shippingset = ShippingFormSet(instance=porder)
        shipping_form = ShippingForm()

    return render(request, 'order/shipping_add.html', {
                'order_form':order_form, 'payformset':payformset,
                'orderformset':orderformset, 'shippingset':shippingset,
                'shipping_form':shipping_form, 'order_id': porder.id,
            })
