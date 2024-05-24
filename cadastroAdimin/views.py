from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.forms import inlineformset_factory
from django import forms
from cadastroAdimin.models import CadastroEspelho, AdminEspelho, MembroFamiliaEspelho, CadastroVoluntarioEspelho
from cadastros.models import Admin


# ----------------------------------------------------------------------------------------------------------------------
# TODO Adimin home
class AdiminHome(ListView):
    template_name = "interface/admin.html"

    def get_queryset(self):
        homeAdm = self.kwargs.get("dados_id")
        return Admin.objects.filter(id=homeAdm)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# ----------------------------------------------------------------------------------------------------------------------
# TODO Cadastrar Adimin

class AdminForm(forms.ModelForm):
    class Meta:
        model = AdminEspelho
        fields = ['nome', 'email', 'cpf', 'senha', 'telefone']
        widgets = {
            'senha': forms.PasswordInput(),
        }


class CadAdimin(CreateView):
    model = AdminEspelho
    form_class = AdminForm
    success_url = reverse_lazy("homeAdimin")

    # ----------------------------------------------------------------------------------------------------------------------


# TODO Listagem de Funcionario
class FuncListView(ListView):
    model = CadastroVoluntarioEspelho
    paginate_by = 15
    context_object_name = 'cadastrovoluntario_list'


# TODO Listagem de criança
class CadastroEspelhoLista(ListView):
    model = CadastroEspelho
    paginate_by = 15
    context_object_name = 'cadastroespelho_list'


# Deletar as linhas de Criança e funcionario ---------------------------------------------------------------------------
class CadDeleteView(DeleteView):
    model = CadastroEspelho
    success_url = reverse_lazy("adimin_listagem_crianca")


# Deletar funcionario---------------------------------------------------------------------------------------------------

class FuncDeleteView(DeleteView):
    model = CadastroVoluntarioEspelho
    success_url = reverse_lazy("adimin_listagem_funcionario")


# Busca Visualizando ---------------------------------------------------------------------------------------------------
# TODO busca criança página
class DadosCadastrosCriancas(ListView):
    model = CadastroEspelho
    template_name = "cadastroAdimin/buscas/criancas/Dados_cadastroCrianca.html"

    def get_queryset(self):
        dados_id = self.kwargs.get("dados_id")
        return CadastroEspelho.objects.filter(id=dados_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# -----------------------------------------------------------------------------------------------------------------------
# TODO busca Voluntario página
class DadosCadastrosVoluntarios(ListView):
    model = CadastroVoluntarioEspelho
    template_name = 'cadastroAdimin/buscas/voluntarios/Dados_cadastroVoluntario.html'

    def get_queryset(self):
        dados_id = self.kwargs.get("dados_id")
        return CadastroVoluntarioEspelho.objects.filter(id=dados_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


#  Busca da consulta ---------------------------------------------------------------------------------------------------
# TODO busca Criança
class ProcurarCrianca(ListView):
    model = CadastroEspelho
    template_name = "cadastroAdimin/buscas/criancas/ProcurarCrianca.html"
    success_url = reverse_lazy("procurarCrianca")

    def get_queryset(self):
        procurar_termo = self.request.GET.get("q", "").strip()
        if not procurar_termo:
            raise Http404()

        return CadastroEspelho.objects.filter(
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


# -----------------------------------------------------------------------------------------------------------------------
# TODO busca Funcionario
class ProcurarVoluntario(ListView):
    model = CadastroVoluntarioEspelho
    template_name = "cadastroAdimin/buscas/voluntarios/ProcurarVoluntarios.html"
    success_url = reverse_lazy("procurarCrianca")

    def get_queryset(self):
        procurar_termo = self.request.GET.get("q", "").strip()
        if not procurar_termo:
            raise Http404()

        return CadastroVoluntarioEspelho.objects.filter(
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


# Cadastro Criança, Adimin --------------------------------------------------------------------------------
# TODO Cadastrar criança
class CadCreateView(CreateView):
    model = CadastroEspelho
    fields = '__all__'
    success_url = reverse_lazy('homeAdimin')

    def get_context_data(self, **kwargs):
        data = super(CadCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            MembroFamiliaFormSet = inlineformset_factory(CadastroEspelho, MembroFamiliaEspelho, fields='__all__',
                                                         extra=0)
            data['membros_form'] = MembroFamiliaFormSet(self.request.POST, self.request.FILES, instance=self.object,
                                                        prefix='membros')
            # Verificando os dados do POST
            print(self.request.POST)
        else:
            MembroFamiliaFormSet = inlineformset_factory(CadastroEspelho, MembroFamiliaEspelho, fields='__all__',
                                                         extra=1)
            data['membros_form'] = MembroFamiliaFormSet(instance=self.object, prefix='membros')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        membros_form = context['membros_form']

        # Lógica para criar membros da família diretamente do formulário principal
        nome2 = self.request.POST.getlist('nome2')
        sexo = self.request.POST.getlist('sexo')
        membros = []
        for nome_membro, sexo_membro in zip(nome2, sexo):
            membros.append(MembroFamiliaEspelho(
                nome=nome_membro,
                sexo=sexo_membro,
            ))

        if membros_form.is_valid():
            with transaction.atomic():
                self.object = form.save()  # Salvar o formulário principal primeiro
                for membro in membros:
                    membro.cadastro = self.object  # Atribuir a instância de Cadastro
                    membro.save()
                membros_form.instance = self.object  # Atribuir a instância de Cadastro ao formset
                membros_form.save()  # Salvar o formset de membros da família

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Remova campos específicos do formulário conforme necessário
        campos_removidos = ['finished_at']
        for campo in campos_removidos:
            form.fields.pop(campo, None)
        return form


class CadUpdateView(UpdateView):
    model = CadastroEspelho
    fields = "__all__"
    success_url = reverse_lazy("adimin_listagem_crianca")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Remova campos específicos do formulário conforme necessário
        campos_removidos = ['finished_at']
        for campo in campos_removidos:
            form.fields.pop(campo, None)
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            MembroFamiliaFormSet = inlineformset_factory(CadastroEspelho, MembroFamiliaEspelho, fields='__all__',
                                                         extra=0)
            data['membros_form'] = MembroFamiliaFormSet(self.request.POST, instance=self.object, prefix='membros')
        else:
            MembroFamiliaFormSet = inlineformset_factory(CadastroEspelho, MembroFamiliaEspelho, fields='__all__',
                                                         extra=0)
            data['membros_form'] = MembroFamiliaFormSet(instance=self.object, prefix='membros')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        membros_form = context['membros_form']

        if membros_form.is_valid():
            with transaction.atomic():
                self.object = form.save()
                membros_form.instance = self.object
                membros_form.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)
