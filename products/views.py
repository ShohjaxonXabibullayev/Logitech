from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import TechsForm, CommentForm,  UpdateProfileForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib import messages

@login_required(login_url='login')
def technos(request):
    query_n = request.GET.get('n', '')
    query_p = request.GET.get('p', '')
    if query_n and query_p:
        techs = Techs.objects.filter(
            Q(title__icontains=query_n) & Q(price=query_p)
        )
    elif query_n:
        techs = Techs.objects.filter(
            Q(title__icontains=query_n)
        )
    else:
        techs = Techs.objects.all()
    categories = Catagory.objects.all()
    return render(request, 'products.html', {'categories': categories, 'techs': techs})


@login_required(login_url='login')
def category_filter(request, cat_id):
    categories = Catagory.objects.all()
    selected_category = Catagory.objects.get(id=cat_id)
    techs = Techs.objects.filter(category=selected_category)
    return render(request, 'products.html', {
        'techs': techs,
        'categories': categories,
        'selected_category': selected_category
    })


class MahsulotlarDetail(View):
    def get(self, request, pk):
        mahsulot = Techs.objects.get(id=pk)
        comments = mahsulot.comments.all()
        form = CommentForm()
        return render(request, 'Mahsulotlar_detail.html', {
            'mahsulot': mahsulot,
            'comments': comments,
            'form': form
        })

    def post(self, request, pk):
        mahsulot = Techs.objects.get(id=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tech = mahsulot
            comment.save()
            return redirect('products_detail', pk=pk)
        comments = mahsulot.comments.all()
        return render(request, 'Mahsulotlar_detail.html', {
            'mahsulot': mahsulot,
            'comments': comments,
            'form': form
        })

class MahsulotlarCreate(View):
    def get(self, request):
        form = TechsForm()
        return render(request, 'mahsulotlar_create.html', {'form': form})

    def post(self, request):
        form = TechsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
        return render(request, 'mahsulotlar_create.html', {'form':form})

class MahsulotlarUpdate(View):
    def get(self, request, pk):
        mahsulot = Techs.objects.get(id=pk)
        form = TechsForm(instance=mahsulot)
        return render(request, 'mahsulotlar_update.html', {'form':form, 'mahsulot': mahsulot})

    def post(self, request, pk):
        mahsulot = Techs.objects.get(id=pk)
        form = TechsForm(request.POST, request.FILES, instance=mahsulot)
        if form.is_valid():
            form.save()
            return redirect('products_detail', mahsulot.id)
        return render(request, 'mahsulotlar_update.html', {'form':form, 'mahsulot': mahsulot})

class MahsulotlarDelete(View):
    def get(self, request, pk):
        mahsulot = Techs.objects.get(id=pk)
        return render(request, 'mahsulotlar_delete.html', {'mahsulot':mahsulot})

    def post(self, request, pk):
        mahsulot = Techs.objects.get(id=pk)
        mahsulot.delete()
        return redirect('products')

@login_required
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'account/profile.html', {'user':user})

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('products_detail', pk=comment.tech.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('products_detail', pk=comment.tech.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comment_edit.html', {'form': form, 'comment': comment})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    tech_id = comment.tech.id
    if request.user == comment.user:
        comment.delete()
    return redirect('products_detail', pk=tech_id)

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=user)
    return render(request, 'account/update_profile.html', {'form': form})
