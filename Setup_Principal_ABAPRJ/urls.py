from django.urls import path
import hashlib


def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()


from cadastros.views import (
    # funções basicas
    CadCriancaCreateView,
    CadListView,
    CadCompleteView,
    ValidarFuncionario,
    # buscas e html
    Procurar,
    DadosCadastros,
    CadVoluntario,
    ChamaApoie,
    ChamaHome,
    ChamarLogin,
)

from cadastroAdimin.views import (
    CadastroEspelhoLista,
    FuncListView,
    AdiminHome,
    CadAdimin,
    CadCreateView,
    DadosCadastrosVoluntarios,
    ProcurarVoluntario,
    ProcurarCrianca,
    DadosCadastrosCriancas,
    CadUpdateView,
    CadDeleteView,
    FuncDeleteView,
)

urlpatterns = [
    # Funcionais links -------------------------------------------------------------------------------------------------
    path("", ChamaHome.as_view(), name="home"),
    path(f"apoiar/{generate_hash('apoie')}", ChamaApoie.as_view(), name="apoie"),
    path(f"login/{generate_hash('login')}", ChamarLogin.as_view(), name="login"),
    path(
        f"Candidatar/{generate_hash('candidato')}",
        CadVoluntario.as_view(),
        name="candidato",
    ),
    # ------------------------------------------------------------------------------------------------------------------
    # Adimin links -----------------------------------------------------------------------------------------------
    path(
        f"Home-Adimin/{generate_hash('homeAdimin')}",
        AdiminHome.as_view(),
        name="homeAdimin",
    ),
    path(
        f"Home-Adimin/cadstrarAdimin/{generate_hash('cadastra_adimin')}",
        CadAdimin.as_view(),
        name="cadastrar_adimin",
    ),
    path(
        f"Home-Adimin/ListaDeCriança/{generate_hash('lista_crianca')}",
        CadastroEspelhoLista.as_view(),
        name="adimin_listagem_crianca",
    ),
    path(
        f"Home-Adimin/ListaDeFuncionario/{generate_hash('lista_funcionario')}",
        FuncListView.as_view(),
        name="adimin_listagem_funcionario",
    ),
    path(
        f"Home-Adimin/Cadastrar-Criança/{generate_hash('cadastra_crianca')}",
        CadCreateView.as_view(),
        name="adimim_cadastra_crianca",
    ),
    path(
        f"Home-Adimin/Atualizar/{generate_hash('atualizar_crianca')}-<int:pk>",
        CadUpdateView.as_view(),
        name="adimin_cadastro_atualizar",
    ),
    path(
        f"Home-Adimin/Delete-Crianças/{generate_hash('deletar_crianca')}-<int:pk>",
        CadDeleteView.as_view(),
        name="adimin_cadastro_deletar",
    ),
    path(
        f"Home-Adimin/Delete-Funcionarios/{generate_hash('deletar_crianca')}-<int:pk>",
        FuncDeleteView.as_view(),
        name="adimin_candidato_deletar",
    ),
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Busca ------------------------------------------------------------------------------------------------------------
    path(
        f"Adimin/buscar-Funcionario/{generate_hash('procurarVoluntarios')}",
        ProcurarVoluntario.as_view(),
        name="procurarVoluntarios",
    ),
    path(
        f"Adimin/buscar-Funcionario/dados/{generate_hash('dadosVoluntarios')}-<int:dados_id>",
        DadosCadastrosVoluntarios.as_view(),
        name="dadosVoluntarios",
    ),
    path(
        f"Adimin/buscar-Criança/{generate_hash('procurarVoluntarios')}",
        ProcurarCrianca.as_view(),
        name="procurarCrianca",
    ),
    path(
        f"Adimin/buscar-Criança/dados/{generate_hash('dadosCrianca')}-<int:dados_id>",
        DadosCadastrosCriancas.as_view(),
        name="dadosCrianca",
    ),
    # Funcionarios links -----------------------------------------------------------------------------------------------
    path(
        f"Funcionario-cadastrar/{generate_hash('cadastro_crianca')}",
        CadCriancaCreateView.as_view(),
        name="funcionario_cadastro_crianca",
    ),
    path(
        f"Funcionario-ListaDeCriança/{generate_hash('listagem_crianca')}",
        CadListView.as_view(),
        name="funcionario_listagem_crianca",
    ),
    # path(f"Home-Adimin/Atualizar/{generate_hash('atualizar_crianca')}-<int:pk>", CadUpdateView.as_view(), name="adimin_cadastro_atualizar")
    # falta lógica de atualização remover membro
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Busca ------------------------------------------------------------------------------------------------------------
    path(
        f"Funcionario/buscar-Criança/{generate_hash('procurarVoluntarios')}",
        Procurar.as_view(),
        name="procurar",
    ),
    path(
        f"Funcionario/buscar-Criança/dados/{generate_hash('dadosCrianca')}-<int:dados_id>",
        DadosCadastros.as_view(),
        name="dados",
    ),
    # botões -----------------------------------------------------------------------------------------------------------
    path(
        f"btn-complete/criança/{generate_hash('cad_complete')}-<int:pk>",
        CadCompleteView.as_view(),
        name="cad_complete",
    ),
    path(
        f"btn-complete/funcionario/{generate_hash('func_complete')}-<int:pk>",
        ValidarFuncionario.as_view(),
        name="func_complete",
    ),
]
