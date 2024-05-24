from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.forms import inlineformset_factory
from cadastros.models import Cadastro, Login, CadastroVoluntario, MembroFamilia
from django import forms


#  Redirecionar para paginas (12 - 59) ---------------------------------------------------------------------------------
# TODO logar
class ChamarLogin(CreateView):
    model = Login
    fields = "__all__"

    def form_valid(self, form):
        # Obter a instância do objeto Login
        login = form.save(commit=False)

        # Continuar com a lógica original
        if login.opcao in "Func":
            return redirect("funcionario_lista_crianca")
        else:
            return redirect("homeAdimin")


# ----------------------------------------------------------------------------------------------------------------------
# TODO Home
class ChamaHome(ListView):
    template_name = "interface/index.html"

    def get_queryset(self):
        home = self.kwargs.get("dados_id")
        return Cadastro.objects.filter(id=home)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# ----------------------------------------------------------------------------------------------------------------------
# TODO Apoie
class ChamaApoie(ListView):
    model = CadastroVoluntario
    template_name = "interface/apoie.html"
    context_object_name = 'parceiros'

    def get_queryset(self):
        apoie = self.kwargs.get("dados_id")
        return Cadastro.objects.filter(id=apoie)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# ----------------------------------------------------------------------------------------------------------------------


# Cadastro Criança e menbro, Funcionario,  -----------------------------------------------------------------------------
# TODO Cadastrar criança
class CadCriancaCreateView(CreateView):
    model = Cadastro
    fields = "__all__"
    success_url = reverse_lazy("funcionario_listagem_crianca")

    def get_context_data(self, **kwargs):
        data = super(CadCriancaCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            MembroFamiliaFormSet = inlineformset_factory(
                Cadastro, MembroFamilia, fields="__all__", extra=0
            )
            data["membros_form"] = MembroFamiliaFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix="membros",
            )
            # Verificando os dados do POST
            print(self.request.POST)
        else:
            MembroFamiliaFormSet = inlineformset_factory(
                Cadastro, MembroFamilia, fields="__all__", extra=1
            )
            data["membros_form"] = MembroFamiliaFormSet(
                instance=self.object, prefix="membros"
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        membros_form = context["membros_form"]

        # Lógica para criar membros da família diretamente do formulário principal
        nome2 = self.request.POST.getlist("nome2")
        sexo = self.request.POST.getlist("sexo")
        membros = []
        for nome_membro, sexo_membro in zip(nome2, sexo):
            membros.append(
                MembroFamilia(
                    nome=nome_membro,
                    sexo=sexo_membro,
                )
            )

        if membros_form.is_valid():
            with transaction.atomic():
                self.object = form.save()  # Salvar o formulário principal primeiro
                for membro in membros:
                    membro.cadastro = self.object  # Atribuir a instância de Cadastro
                    membro.save()
                membros_form.instance = (
                    self.object
                )  # Atribuir a instância de Cadastro ao formset
                membros_form.save()  # Salvar o formset de membros da família

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Remova campos específicos do formulário conforme necessário
        campos_removidos = ["finished_at"]
        for campo in campos_removidos:
            form.fields.pop(campo, None)
        return form


# ----------------------------------------------------------------------------------------------------------------------
# TODO Cadastrar Funcionario - candidatar


class VoluntarioForm(forms.ModelForm):
    class Meta:
        model = CadastroVoluntario
        fields = [
            "nome",
            "cpf",
            "email",
            "senha",
            "confirmar_senha",
            "telefone",
            "descricao",
        ]
        widgets = {
            "senha": forms.PasswordInput(),
            "confirmar_senha": forms.PasswordInput(),
        }


class CadVoluntario(CreateView):
    model = CadastroVoluntario
    form_class = VoluntarioForm
    success_url = reverse_lazy("home")


# ----------------------------------------------------------------------------------------------------------------------

# listagem de criança --------------------------------------------------------------------------------------------------
# TODO Listagem de Criança


class CadListView(ListView):
    model = Cadastro
    paginate_by = 10


# Atualizar criança ----------------------------------------------------------------------------------------------------


class CadUpdateView(UpdateView):
    model = Cadastro
    fields = "__all__"
    success_url = reverse_lazy("func_cad_crianca")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Remova campos específicos do formulário conforme necessário
        campos_removidos = ["finished_at"]
        for campo in campos_removidos:
            form.fields.pop(campo, None)
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            MembroFamiliaFormSet = inlineformset_factory(
                Cadastro, MembroFamilia, fields="__all__", extra=0
            )
            data["membros_form"] = MembroFamiliaFormSet(
                self.request.POST, instance=self.object, prefix="membros"
            )
        else:
            MembroFamiliaFormSet = inlineformset_factory(
                Cadastro, MembroFamilia, fields="__all__", extra=0
            )
            data["membros_form"] = MembroFamiliaFormSet(
                instance=self.object, prefix="membros"
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        membros_form = context["membros_form"]

        if membros_form.is_valid():
            with transaction.atomic():
                self.object = form.save()
                membros_form.instance = self.object
                membros_form.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


# Busca Visualizando ---------------------------------------------------------------------------------------------------
# TODO busca criança página
class DadosCadastros(ListView):
    model = Cadastro
    template_name = "cadastros/busca/criancas/Dados_cadastro.html"

    def get_queryset(self):
        dados_id = self.kwargs.get("dados_id")
        return Cadastro.objects.filter(id=dados_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


#  Busca da consulta ---------------------------------------------------------------------------------------------------
# TODO busca Criança
class Procurar(ListView):
    model = Cadastro
    template_name = "cadastros/busca/criancas/Procurar.html"
    success_url = reverse_lazy("procurar")

    def get_queryset(self):
        procurar_termo = self.request.GET.get("q", "").strip()
        if not procurar_termo:
            raise Http404()

        return Cadastro.objects.filter(
            Q(
                Q(nome__icontains=procurar_termo) | Q(cpf__icontains=procurar_termo),
            )
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        procurar_termo = self.request.GET.get("q", "").strip()
        context["page_title"] = (f'Procurar por "{procurar_termo}" |',)
        context["procurar_termo"] = (procurar_termo,)
        return context


# validações externas por click ----------------------------------------------------------------------------------------
# TODO validar data, cadastro criança
# falta, fazer em cascata!
class CadCompleteView(View):
    @staticmethod
    def get(request, pk):
        finalizar = get_object_or_404(Cadastro, pk=pk)
        finalizar.mark_has_complete()
        return redirect("adimin_listagem_crianca")


# ----------------------------------------------------------------------------------------------------------------------
# TODO Aceitar como funcionario
class ValidarFuncionario(View):
    @staticmethod
    def get(request, pk):
        finalizar = get_object_or_404(CadastroVoluntario, pk=pk)
        finalizar.mark_has_complete()
        return redirect("adimin_listagem_funcionario")


# ----------------------------------------------------------------------------------------------------------------------
