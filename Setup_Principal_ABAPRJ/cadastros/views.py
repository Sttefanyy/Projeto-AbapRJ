from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.forms import inlineformset_factory

from cadastros.form import LoginForm, VoluntarioForm, CadastroEspelhoForm
from cadastros.models import (
    Cadastro,
    Login,
    CadastroVoluntario,
    MembroFamilia,
    EsqueciSenha, )

from django.core.mail import send_mail
from django.contrib import messages
from pixqrcodegen import Payload


# ----------------------------------------------------------------------------------------------------------------------
# TODO Direcionar para pág. --------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Login Pág.
# ----------------------------------------------------------------------------------------------------------------------
class ChamarLogin(CreateView):
    model = Login
    form_class = LoginForm

    def form_valid(self, form):
        # Obter a instância do objeto Login
        login = form.save(commit=False)

        # Continuar com a lógica original
        if login.opcao in "Func":
            return redirect("funcionario_listagem_crianca")
        else:
            return redirect("homeAdmin")


# ----------------------------------------------------------------------------------------------------------------------
# Index Home Pág.
# ----------------------------------------------------------------------------------------------------------------------
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
# Apoie Pág.
# ----------------------------------------------------------------------------------------------------------------------
class ChamaApoie(ListView):
    model = CadastroVoluntario
    template_name = "interface/apoie.html"
    context_object_name = "parceiros"
    paginate_by = 10

    def get_queryset(self):
        return CadastroVoluntario.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalhes do Cadastro"
        return context


# ----------------------------------------------------------------------------------------------------------------------
# Recuperarsenha Pág.
# ----------------------------------------------------------------------------------------------------------------------
class ChamarRecuperarsenha(CreateView):
    model = EsqueciSenha
    fields = ["email"]
    template_name = "cadastros/e-mail/EsqueciSenha_form.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try:
            esqueci_senha = EsqueciSenha(email=email)
            senha = esqueci_senha.verificar_email()
            send_mail(
                subject="Relembrar senha",
                message=f"Sua senha é {senha}",
                from_email="projeto.abaprj@gmail.com",
                recipient_list=[email],
            )
            messages.success(
                self.request,
                "Um email com sua senha foi enviado para o endereço fornecido.",
            )
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        except Exception as e:
            messages.error(
                self.request,
                "Ocorreu um erro ao enviar o e-mail. Por favor, tente novamente.",
            )
            return self.form_invalid(form)
        return redirect("login")


# ----------------------------------------------------------------------------------------------------------------------
# Registro Pág. e cadastro
# ----------------------------------------------------------------------------------------------------------------------
class CadVoluntario(CreateView):
    model = CadastroVoluntario
    form_class = VoluntarioForm
    success_url = reverse_lazy("home")


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# TODO Crud Criança Dados ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Cadastrar Criança
# ----------------------------------------------------------------------------------------------------------------------
class CadCreateView(CreateView):
    model = Cadastro
    fields = "__all__"
    success_url = reverse_lazy("funcionario_listagem_crianca")

    def get_context_data(self, **kwargs):
        data = super(CadCreateView, self).get_context_data(**kwargs)
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
# Atualizar Criança
# ----------------------------------------------------------------------------------------------------------------------
class CadUpdateView(UpdateView):
    model = Cadastro
    form_class = CadastroEspelhoForm
    success_url = reverse_lazy("funcionario_listagem_crianca")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        MembroFamiliaFormSet = inlineformset_factory(
            Cadastro, MembroFamilia, fields="__all__", extra=0
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
# Listar Criança
# ----------------------------------------------------------------------------------------------------------------------
class CadListView(ListView):
    model = Cadastro
    paginate_by = 10
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# TODO Botões Funcionais ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Completar criança para Funcionário
# ----------------------------------------------------------------------------------------------------------------------
class CadCompleteView(View):
    @staticmethod
    def get(request, pk):
        finalizar = get_object_or_404(Cadastro, pk=pk)
        finalizar.mark_has_complete()
        return redirect("adimin_listagem_crianca")


# ----------------------------------------------------------------------------------------------------------------------
# Aceitar Voluntario, como Funcionario
# ----------------------------------------------------------------------------------------------------------------------
class ValidarFuncionario(View):
    @staticmethod
    def get(request, pk):
        finalizar = get_object_or_404(CadastroVoluntario, pk=pk)
        finalizar.mark_has_complete()
        return redirect("adimin_listagem_funcionario")


# ----------------------------------------------------------------------------------------------------------------------
# Gerar QR CODE, AJax
# ----------------------------------------------------------------------------------------------------------------------
def gerar_payload(request):
    if request.method == 'POST':
        valor = request.POST.get('valor')
        if valor:
            payload = Payload(
                "Pedro Cezar Silva de Souza",
                "+5521995897270",
                valor,
                "São Gonçalo",
                "ProjetoABAPRJ",
            )
            payload.gerarPayload()
            response_data = {
                'message': 'Payload gerado com sucesso!',
                'qrcode_url': '/static/imagens/pixqrcodegen.png'
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'message': 'Valor não pode estar vazio.'}, status=400)
    return JsonResponse({'message': 'Método não permitido.'}, status=405)


# ----------------------------------------------------------------------------------------------------------------------
# TODO Buscar e Visualizando, por pesquisa  ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# buscar criança, página
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# buscar criança
# ----------------------------------------------------------------------------------------------------------------------
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
                Q(nome__icontains=procurar_termo) | Q(cpf__icontains=procurar_termo) | Q(cidade__istartswith=procurar_termo),
            )
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        procurar_termo = self.request.GET.get("q", "").strip()
        context["page_title"] = f'Procurar por "{procurar_termo}" |',
        context["procurar_termo"] = procurar_termo
        context["total_resultados"] = self.get_queryset().count()
        return context
