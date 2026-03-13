from django.shortcuts import render,redirect
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

@login_required
def addproducts(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('home')
    else:
        form = ProductForm()
    
    return render(request, 'addproducts.html', {'form': form})