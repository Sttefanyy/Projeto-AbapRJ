from django.db import transaction
from django.db.models import Q

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.forms import inlineformset_factory
from cadastroAdmin.form import AdminForm

from django.core.mail import send_mail
from django.core.paginator import Paginator

from cadastroAdmin.models import (
    CadastroEspelho,
    AdminEspelho,
    MembroFamiliaEspelho,
    CadastroVoluntarioEspelho, )
from cadastros.models import CadastroVoluntario

from cadastros.views import CadastroEspelhoForm

# Senha de gerência
senhaGerente = "senhaPadrao"


# ----------------------------------------------------------------------------------------------------------------------
# TODO Direcionar para pág. --------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Administração Pág.
# ----------------------------------------------------------------------------------------------------------------------
class AdminHome(ListView):
    model = AdminEspelho
    template_name = "interface/admin.html"
    context_object_name = "funcionarios"
    paginate_by = 10

    def get_queryset(self):
        return AdminEspelho.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# ----------------------------------------------------------------------------------------------------------------------
# Gerência Pág.
# ----------------------------------------------------------------------------------------------------------------------
class Gerenrecia(View):
    def post(self, request, **kwargs):
        senha = request.POST.get("senha")

        if senha == senhaGerente:
            success_url = reverse_lazy("adimin_listagem")
            return HttpResponseRedirect(success_url)
        else:
            success_url = reverse_lazy("homeAdmin")
            return HttpResponseRedirect(success_url)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# TODO Cadastrar Dados -------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Cadastrar Administração
# ----------------------------------------------------------------------------------------------------------------------
class CadAdmin(CreateView):
    model = AdminEspelho
    form_class = AdminForm
    success_url = reverse_lazy("homeAdmin")


# ----------------------------------------------------------------------------------------------------------------------
# Cadastrar Criança
# ----------------------------------------------------------------------------------------------------------------------
class AdminCadCreate(CreateView):
    model = CadastroEspelho
    fields = "__all__"
    success_url = reverse_lazy("adimin_listagem_crianca")

    def get_context_data(self, **kwargs):
        data = super(AdminCadCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            MembroFamiliaFormSet = inlineformset_factory(
                CadastroEspelho, MembroFamiliaEspelho, fields="__all__", extra=0
            )
            data["membros_form"] = MembroFamiliaFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix="membros",
            )

        else:
            MembroFamiliaFormSet = inlineformset_factory(
                CadastroEspelho, MembroFamiliaEspelho, fields="__all__", extra=1
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
                MembroFamiliaEspelho(
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


# ----------------------------------------------------------------------------------------------------------------------
# TODO Atualizar Dados -------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Atulizar Administração
# ----------------------------------------------------------------------------------------------------------------------
class AdminUpdateView(UpdateView):
    model = AdminEspelho
    context_object_name = "admin"

    fields = ["nome", "email", "cpf", "senha", "telefone", "situacao_atual"]
    success_url = reverse_lazy("adimin_listagem")

    def form_valid(self, form):
        situacao = form.cleaned_data.get("situacao_atual")
        if situacao == "Adm.":
            form.instance.cod_acesso = "negado"
        else:
            form.instance.cod_acesso = senhaGerente
            send_mail(
                subject="Relembrar senha",
                message=f"Sua senha é {form.instance.cod_acesso}",
                from_email="projeto.abaprj@gmail.com",
                recipient_list=[
                    form.instance.email
                ],  # Acessa o campo de email do objeto
            )
        return super().form_valid(form)


# ----------------------------------------------------------------------------------------------------------------------
# Atulizar Funcionário
# ----------------------------------------------------------------------------------------------------------------------
class FuncUpdateView(UpdateView):
    model = CadastroVoluntario
    fields = ["nome", "email", "telefone", "cpf"]
    template_name = "cadastros/CadastroVoluntario_form.html"
    success_url = reverse_lazy("adimin_listagem_funcionario")


# ----------------------------------------------------------------------------------------------------------------------
# Atulizar Criança
# ----------------------------------------------------------------------------------------------------------------------
class AdminCadUpdate(UpdateView):
    model = CadastroEspelho
    form_class = CadastroEspelhoForm
    success_url = reverse_lazy("adimin_listagem_crianca")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        MembroFamiliaFormSet = inlineformset_factory(
            CadastroEspelho, MembroFamiliaEspelho, fields="__all__", extra=0
        )  # Alterado para extra=0 para não adicionar membros dinamicamente na edição
        if self.request.POST:
            data["membros_form"] = MembroFamiliaFormSet(
                self.request.POST,
                instance=self.object,
                prefix="membros",
            )
        else:
            data["membros_form"] = MembroFamiliaFormSet(
                instance=self.object, prefix="membros"
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        membros_form = context["membros_form"]

        if membros_form.is_valid():
            with transaction.atomic():
                self.object = form.save()  # Salvar o formulário principal primeiro
                membros_form.save()  # Salvar o formset de membros da família
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# TODO Listar cadastrados ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Listagem Dados Administração
# ----------------------------------------------------------------------------------------------------------------------
class AdminListView(ListView):
    model = AdminEspelho
    paginate_by = 10
    context_object_name = "adiminespelho_list"


# ----------------------------------------------------------------------------------------------------------------------
# Listagem Dados Funcionário
# ----------------------------------------------------------------------------------------------------------------------
class FuncListView(ListView):
    model = CadastroVoluntarioEspelho
    paginate_by = 20  # 20 itens por página
    context_object_name = "cadastrovoluntario_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Queryset combinado para funcionários e candidatos
        queryset = CadastroVoluntarioEspelho.objects.filter(
            Q(situacao="Funcionario") | Q(situacao="Candidato")
        )

        # Número da página atual
        page_number = self.request.GET.get("page")

        # Paginador para o queryset combinado, com o valor de paginate_by
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(page_number)

        # Divide a página em funcionários e candidatos
        funcionarios = []
        candidatos = []
        for item in page_obj.object_list:
            if item.situacao == "Funcionario":
                funcionarios.append(item)
            elif item.situacao == "Candidato":
                candidatos.append(item)

        # Ajusta as listas para corresponder ao número de exibição necessário
        funcionarios = funcionarios[:10]
        candidatos = candidatos[:10]

        context["page_obj"] = page_obj
        context["funcionarios"] = funcionarios
        context["candidatos"] = candidatos
        context["is_paginated"] = page_obj.has_other_pages()

        return context


# ----------------------------------------------------------------------------------------------------------------------
# Listagem Dados Criança
# ----------------------------------------------------------------------------------------------------------------------
class CadastroEspelhoLista(ListView):
    model = CadastroEspelho
    paginate_by = 5
    context_object_name = "cadastroespelho_list"
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# TODO Deletar Cadastros -----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Deletar Dados Criança
# ----------------------------------------------------------------------------------------------------------------------
class CadDeleteView(DeleteView):
    model = CadastroEspelho
    success_url = reverse_lazy("adimin_listagem_crianca")


# ----------------------------------------------------------------------------------------------------------------------
# Deletar Dados Funcionário
# ----------------------------------------------------------------------------------------------------------------------
class FuncDeleteView(DeleteView):
    model = CadastroVoluntarioEspelho
    success_url = reverse_lazy("adimin_listagem_funcionario")


# ----------------------------------------------------------------------------------------------------------------------
# Deletar Dados Administração
# ----------------------------------------------------------------------------------------------------------------------
class AdminDeleteView(DeleteView):
    model = AdminEspelho
    success_url = reverse_lazy("adimin_listagem")


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# TODO Buscar e Visualizando, por pesquisa  ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# buscar criança, página
# ----------------------------------------------------------------------------------------------------------------------
class DadosCadastrosCriancas(ListView):
    model = CadastroEspelho
    template_name = "cadastroAdmin/buscas/criancas/Dados_cadastroCrianca.html"

    def get_queryset(self):
        dados_id = self.kwargs.get("dados_id")
        return CadastroEspelho.objects.filter(id=dados_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# -----------------------------------------------------------------------------------------------------------------------
# buscar Voluntario, página
# ----------------------------------------------------------------------------------------------------------------------
class DadosCadastrosVoluntarios(ListView):
    model = CadastroVoluntarioEspelho
    template_name = "cadastroAdmin/buscas/voluntarios/Dados_cadastroVoluntario.html"

    def get_queryset(self):
        dados_id = self.kwargs.get("dados_id")
        return CadastroVoluntarioEspelho.objects.filter(id=dados_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# ----------------------------------------------------------------------------------------------------------------------
# buscar Administrador, página
# ----------------------------------------------------------------------------------------------------------------------
class DadosCadastrosAdmin(ListView):
    model = AdminEspelho
    template_name = "cadastroAdmin/buscas/admin/Dados_cadastroAdmin.html"

    def get_queryset(self):
        dados_id = self.kwargs.get("dados_id")
        return AdminEspelho.objects.filter(id=dados_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# ----------------------------------------------------------------------------------------------------------------------
# buscar Criança
# ----------------------------------------------------------------------------------------------------------------------
class ProcurarCrianca(ListView):
    model = CadastroEspelho
    template_name = "cadastroAdmin/buscas/criancas/ProcurarCrianca.html"
    success_url = reverse_lazy("procurarCrianca")

    def get_queryset(self):
        procurar_termo = self.request.GET.get("q", "").strip()
        if not procurar_termo:
            raise Http404()

        return CadastroEspelho.objects.filter(
            Q(
                Q(nome__istartswith=procurar_termo) | Q(cpf__icontains=procurar_termo) | Q(cidade__istartswith=procurar_termo),
            )
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        procurar_termo = self.request.GET.get("q", "").strip()
        context["page_title"] = f'Procurar por "{procurar_termo}" |',
        context["procurar_termo"] = procurar_termo
        context["total_resultados"] = self.get_queryset().count()
        return context


# -----------------------------------------------------------------------------------------------------------------------
# buscar Voluntario
# ----------------------------------------------------------------------------------------------------------------------
class ProcurarVoluntario(ListView):
    model = CadastroVoluntarioEspelho
    template_name = "cadastroAdmin/buscas/voluntarios/ProcurarVoluntarios.html"
    success_url = reverse_lazy("procurarCrianca")

    def get_queryset(self):
        procurar_termo = self.request.GET.get("q", "").strip()
        if not procurar_termo:
            raise Http404()

        return CadastroVoluntarioEspelho.objects.filter(
            Q(
                Q(nome__istartswith=procurar_termo) | Q(cpf__icontains=procurar_termo),
            )
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        procurar_termo = self.request.GET.get("q", "").strip()
        context["page_title"] = f'Procurar por "{procurar_termo}" |',
        context["procurar_termo"] = procurar_termo
        context["total_resultados"] = self.get_queryset().count()
        return context


# ---------------------------------------------------------------------------------------------------------------------
# buscar Administrador
# ----------------------------------------------------------------------------------------------------------------------

class ProcurarAdmin(ListView):
    model = AdminEspelho
    template_name = "cadastroAdmin/buscas/admin/ProcurarAdmin.html"
    success_url = reverse_lazy("procurarAdmin")

    def get_queryset(self):
        procurar_termo = self.request.GET.get("q", "").strip()
        if not procurar_termo:
            raise Http404()

        return AdminEspelho.objects.filter(
            Q(
                Q(nome__istartswith=procurar_termo) | Q(cpf__icontains=procurar_termo),
            )
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        procurar_termo = self.request.GET.get("q", "").strip()
        context["page_title"] = f'Procurar por "{procurar_termo}" |',
        context["procurar_termo"] = procurar_termo
        context["total_resultados"] = self.get_queryset().count()
        return context
# ----------------------------------------------------------------------------------------------------------------------
