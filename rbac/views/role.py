from django.http import HttpResponse
from django.shortcuts import render, redirect
from rbac import models
from django.urls import reverse


def role_list(request):
    role_queryset = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'role_queryset': role_queryset})


from django import forms


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


def role_add(request):
    if request.method == 'GET':
        form = RoleModelForm()
    else:
        form = RoleModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/role_add.html', {'form': form})


def role_edit(request, rid):
    obj = models.Role.objects.filter(id=rid).first()
    if not obj:
        return HttpResponse('角色不存在')

    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
    else:
        form = RoleModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/role_edit.html', {'form': form})
