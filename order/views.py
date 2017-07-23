from django.shortcuts import render

from .models import POrder, POrderItem
from .forms import POrderForm, POrderItemForm
# Create your views here.

def porder_add(request):

    if request.method == 'POST':
        form = POrderForm(request.POST)

        if form.is_valid():
            order = form.save()
            return redirect("order:porderitem_add", id=order.id)
    else:
        form = POrderForm()

    return render(request, 'order/porder_add.html', {'form':form})


def porderitem_add(request, id):
    porder = POrder.objects.select_related('vendor').get(id=id)

    if request.method == 'POST':
        order_form = POrderForm(request.POST, instance=porder)

        if order_form.is_valid():
            created_order = order_form.save(commit=False)
            formset = POrderItemFormSet(request.POST, instance=created_order)

            if formset.is_valid():
                created_order.save()
                formset.save()
                return redirect('order:porderitem_add', id=id)

    else:
        order_form = POrderForm(instance=porder)
        formset = POrderItemFormSet(instance=porder)
        product_list = Product.objects.filter(vendorproduct__vendor=proder.vendor)
        quotation_list = Quotation.objects.filter(vendorproduct__vendor=proder.vendor)
        for form in formset:
            form.fields['produt'].queryset = product_list
            form.fields['quotation'].queryset = quotation_list

    return render(request, 'order:porderitem_add.html', {
            'order_form':order_form, 'formset':formset,
        })