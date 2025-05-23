from http.client import HTTPResponse

from django.shortcuts import render, redirect
from core.forms import LoginForm, AgendaForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest

import ipdb

from core.models import Agenda


def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        context = {'acesso_negado': True}
        return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':LoginForm()})

        
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, 'index.html', context)

@login_required
def cadastrar(request):
    context = {}

    if request.method == "POST":
        form = AgendaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                raise Exception("Não foi possível salver o contato")
        else:
            context['form'] = form

    return render(request,"cadastrar.html", context)


@login_required
def listar(request):
    agendas = Agenda.objects.all()
    context = {"agendas": agendas}
    return render(request, "listar.html", context)

@login_required
def editar(request):
    context = {}
    if request.GET.get("id"):

        model = Agenda.objects.all()
        id =  request.GET.get("id")
        try:
            data = model.filter(id = id).values('id', 'nome_completo', 'telefone', 'email', "observacao")

            if (data):
                return JsonResponse(list(data), safe=False)
            else:
                raise Exception("Não foi possivel carregar contato")
        except Exception as e:
            return HttpResponseBadRequest(e)

    if request.method == "POST":
        context = {}
        try:
            id = int(request.POST.get("id"))
            model = Agenda.objects.get(pk=id)
            form = AgendaForm(request.POST, instance=model)
            if form.is_valid():
                form.save()
        except Exception as e:
            context["error"]= "Não foi possível salver o contato"

    ids = Agenda.objects.all().values("id", "nome_completo")
    context["ids"] = ids

    return render(request, "editar.html", context)

@login_required
def excluir(request):
    context = {}

    if request.method == "POST":
        try:
            id = int(request.POST.get("id"))
            model = Agenda.objects.get(pk=id)
            model.delete()
        except Exception as e:
            context["erro"] = "Não foi possível deletar" , e

    contatos = Agenda.objects.all()
    context["contatos"] = contatos

    return render(request, "excluir.html", context)