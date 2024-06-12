from django.urls import path
import hashlib


def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()


from cadastros.views import (

    # Candastros Crud
    CadCreateView,
    CadVoluntario,
    CadUpdateView,

    # Listagem de funções
    CadListView,

    # Botões
    CadCompleteView,
    ValidarFuncionario,

    # buscas
    Procurar,
    DadosCadastros,

    # Páginas de visualização
    ChamaApoie,
    ChamaHome,
    ChamarLogin,
    ChamarRecuperarsenha,
    gerar_payload

)

from cadastroAdmin.views import (
    # Atualizações
    AdminUpdateView,
    FuncUpdateView,
    AdminCadUpdate,

    # Candastros
    AdminCadCreate,
    CadAdmin,

    # Listagens
    FuncListView,
    AdminHome,
    AdminListView,
    CadastroEspelhoLista,
    # listagem com senha
    Gerenrecia,

    # buscas e html
    DadosCadastrosVoluntarios,
    DadosCadastrosAdmin,
    DadosCadastrosCriancas,
    ProcurarVoluntario,
    ProcurarCrianca,
    ProcurarAdmin,

    # Deletar
    CadDeleteView,
    FuncDeleteView,
    AdminDeleteView,

)

urlpatterns = [
    # Direcionais e iniciais links -------------------------------------------------------------------------------------
    path("", ChamaHome.as_view(), name="home"),
    path(f"apoiar/{generate_hash('apoie')}", ChamaApoie.as_view(), name="apoie"),
    path(f"login/{generate_hash('login')}", ChamarLogin.as_view(), name="login"),
    path(f"Candidatar/{generate_hash('candidato')}", CadVoluntario.as_view(), name="candidato"),
    path(f"RecuperarSenha/{generate_hash('RecuperarSenha-Site')}", ChamarRecuperarsenha.as_view(),
         name="RecuperarSenha"),
    path(f"Home-Admin/{generate_hash('homeAdmin')}", AdminHome.as_view(), name="homeAdmin"),

    # ------------------------------------------------------------------------------------------------------------------

    # Adimin links -----------------------------------------------------------------------------------------------------
    path(f"Home-Admin/cadstrarAdmin/{generate_hash('cadastra_admin')}", CadAdmin.as_view(), name="cadastrar_adimin")
    ,
    path(f"Home-Admin/Cadastrar-Criança/{generate_hash('cadastra_crianca')}", AdminCadCreate.as_view(),
         name="adimim_cadastra_crianca"),

    path(f"Home-Admin/ListaDeCriança/{generate_hash('lista_crianca')}", CadastroEspelhoLista.as_view(),
         name="adimin_listagem_crianca"),
    path(f"Home-Admin/ListaDeFuncionario/{generate_hash('lista_funcionario')}", FuncListView.as_view(),
         name="adimin_listagem_funcionario"),
    path(f"Home-Admin/ListaDeAdmin/{generate_hash('admin_listagem')}", AdminListView.as_view(),
         name="adimin_listagem"),

    path(f"Home-Admin/Atualizar-Criança/{generate_hash('atualizar_crianca')}-<int:pk>", AdminCadUpdate.as_view(),
         name="adimin_cadastro_atualizar"),
    path(f"Home-Admin/Atualizar-Funcionário/{generate_hash('atualizar_admin')}-<int:pk>", FuncUpdateView.as_view(),
         name="adimin_func_atualizar"),
    path(f"Home-Admin/Atualizar/{generate_hash('atualizar_admin')}-<int:pk>", AdminUpdateView.as_view(),
         name="adimin_atualizar"),

    path(f"Home-Admin/Delete-Crianças/{generate_hash('deletar_crianca')}-<int:pk>", CadDeleteView.as_view(),
         name="adimin_cadastro_deletar"),
    path(f"Home-Admin/Delete-Funcionarios/{generate_hash('deletar_funcionario')}-<int:pk>", FuncDeleteView.as_view(),
         name="adimin_candidato_deletar"),
    path(f"Home-Admin/Delete-Administrador/{generate_hash('deletar_admin')}-<int:pk>", AdminDeleteView.as_view(),
         name="adimin_deletar"),

    path(f"btn-senha/{generate_hash('senha-gerente')}", Gerenrecia.as_view(), name="senha"),
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # Busca ------------------------------------------------------------------------------------------------------------
    path(f"Admin/buscar-Funcionario/{generate_hash('procurarVoluntarios')}", ProcurarVoluntario.as_view(),
         name="procurarVoluntarios"),
    path(f"Admin/buscar-Funcionario/dados/{generate_hash('dadosVoluntarios')}-<int:dados_id>",
         DadosCadastrosVoluntarios.as_view(), name="dadosVoluntarios"),
    path(f"Admin/buscar-Criança/{generate_hash('procurarCrianca')}", ProcurarCrianca.as_view(),
         name="procurarCrianca"),
    path(f"Admin/buscar-Criança/dados/{generate_hash('dadosCrianca')}-<int:dados_id>",
         DadosCadastrosCriancas.as_view(), name="dadosCrianca"),
    path(f"Admin/buscar-Admin/{generate_hash('procurarAdmin')}", ProcurarAdmin.as_view(),
         name="procurarAdmin"),
    path(f"Admin/buscar-Admin/dados/{generate_hash('dadosAdmin')}-<int:dados_id>",
         DadosCadastrosAdmin.as_view(), name="dadosAdmin"),
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # Funcionário links -----------------------------------------------------------------------------------------------
    path(f"Funcionario-cadastrarCriança/{generate_hash('cadastro_crianca')}", CadCreateView.as_view(),
         name="funcionario_cadastro_crianca"),
    path(f"funcionario/Atualizar-Criança/{generate_hash('atualizar_crianca')}-<int:pk>", CadUpdateView.as_view(),
         name="funcionario_cadastro_atualizar"),
    path(f"Funcionario-ListarCriança/{generate_hash('listagem_crianca')}", CadListView.as_view(),
         name="funcionario_listagem_crianca"),
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # Busca ------------------------------------------------------------------------------------------------------------
    path(f"Funcionario/buscar-Criança/{generate_hash('procurarVoluntarios')}", Procurar.as_view(), name="procurar"),
    path(f"Funcionario/buscar-Criança/dados/{generate_hash('dadosCrianca')}-<int:dados_id>", DadosCadastros.as_view(),
         name="dados"),

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # botões -----------------------------------------------------------------------------------------------------------
    path(f"btn-complete/criança/{generate_hash('cad_complete')}-<int:pk>", CadCompleteView.as_view(),
         name="cad_complete"),
    path(f"btn-complete/funcionario/{generate_hash('func_complete')}-<int:pk>", ValidarFuncionario.as_view(),
         name="func_complete"),
    path('gerar-payload/', gerar_payload, name='gerar_payload'),

]
