from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


# cadastros ------------------------------------------------------------------------------------------------------------
# Login ----------------------------------------------------------------------------------------------------------------
class Login(models.Model):
    tipos = (
        ("Adm", "Admin"),
        ("Func", "Funcionário"),
    )
    email = models.EmailField(verbose_name="E-mail", max_length=255)
    senha = models.CharField(max_length=100)
    opcao = models.CharField(choices=tipos, max_length=100)

    def clean(self):
        # Verifica se a opção selecionada é "Func"
        if self.opcao == "Func":
            # Tenta recuperar um CadastroVoluntario com a situação 'Funcionario', email e senha fornecidos
            try:
                cadastro = CadastroVoluntario.objects.get(
                    situacao="Funcionario", email=self.email, senha=self.senha
                )
            except CadastroVoluntario.DoesNotExist:
                # Se não encontrar, levanta uma exceção de validação
                raise ValidationError(
                    "Cadastro de Funcionário não encontrado ou e-mail/senha incorretos."
                )
        else:
            # Verifica se existe um registro no modelo Admin com o email e senha fornecidos
            try:
                admin = Admin.objects.get(email=self.email, senha=self.senha)
            except Admin.DoesNotExist:
                # Se não houver nenhum registro com o email e senha fornecidos, levanta uma exceção
                raise ValidationError("E-mail ou senha incorretos para Admin.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# Adimin----------------------------------------------------------------------------------------------------------------
class Admin(models.Model):
    nome = models.CharField(
        max_length=100,
        null=False,
        verbose_name="Nome",
        help_text="Digite o nome aqui.",
    )
    email = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        unique=True,
        help_text="Digite o E-mail aqui.",
        error_messages={
            "blank": "Este campo não pode ficar em branco.",
            "invalid": "O valor fornecido é inválido, verifique se tem @.",
        },
    )
    senha = models.CharField(max_length=100)
    telefone = models.CharField(
        max_length=15,
        null=False,
        blank=True,
        verbose_name="Telefone",
        help_text="Digite seu Telefone aqui. (21) 90000-0000",
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=False,
        blank=True,
        verbose_name="CPF",
        help_text="Digite seu CPF aqui modelo: 000.000.000-00",
    )


# voluntario------------------------------------------------------------------------------------------------------------


class CadastroVoluntario(models.Model):
    nome = models.CharField(
        max_length=100,
        null=False,
        verbose_name="Nome",
        help_text="Digite o nome aqui.",
    )
    email = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        unique=True,
        help_text="Digite o E-mail aqui.",
        error_messages={
            "blank": "Este campo não pode ficar em branco.",
            "invalid": "O valor fornecido é inválido, verifique se tem @.",
        },
    )
    senha = models.CharField(max_length=100)
    confirmar_senha = models.CharField(max_length=100)

    def clean(self):
        if self.senha != self.confirmar_senha:
            raise ValidationError("As senhas não coincidem.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    telefone = models.CharField(
        max_length=15,
        null=False,
        blank=True,
        verbose_name="Telefone",
        help_text="Digite seu Telefone aqui. como no exemplo: (21) 9xxxx-xxxx",
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=False,
        blank=True,
        verbose_name="CPF",
        help_text="Digite seu CPF aqui modelo: 000.000.000-00",
    )
    descricao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descrição",
    )
    situacao = models.CharField(
        max_length=100, verbose_name="Situação", default="Candidato"
    )

    def mark_has_complete(self):
        if self.situacao:
            self.situacao = "Funcionario"
            self.save()


# Dados criança---------------------------------------------------------------------------------------------------------


class Cadastro(models.Model):
    tipos_beneficio_Gov = (
        ("Fed", "Federais"),
        ("Est", "Estaduais"),
        ("Mun", "Municipais"),
        ("BF", "Bolsa Familia"),
        ("BPC", "Benefício de Prestação Continuada"),
        ("PETI", "Programa de Erradicação do Trabalho Infantil"),
        ("O", "Outros"),
    )
    sexo_tipo = (("M", "Masculino"), ("F", "Feminino"))
    # separa termo no html
    nome = models.CharField(
        max_length=100,
        null=False,
        verbose_name="Nome",
        help_text="Digite o nome aqui.",
    )
    telefone = models.CharField(
        max_length=20,
        null=False,
        verbose_name="Telefone",
        help_text="Digite o número de telefone aqui.",
    )
    celular = models.CharField(
        max_length=15,
        null=False,
        blank=True,
        verbose_name="Telefone",
        help_text="Digite seu Telefone aqui. como no exemplo: (21) 9xxxx-xxxx",
    )

    sexo = models.CharField(max_length=1, choices=sexo_tipo, verbose_name="Sexo")
    data_nascimento = models.DateField(
        verbose_name="Data de nascimento", help_text="Data de nascimento"
    )
    endereco = models.CharField(
        max_length=200,
        null=True,
        verbose_name="Endereço",
        help_text="Digite o endereço ",
    )
    bairro = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Bairro",
        help_text="Digite o bairro aqui.",
    )
    cidade = models.CharField(
        max_length=100,
        null=True,
        verbose_name="Cidade",
        help_text="Digite a cidade aqui.",
    )
    estado = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Estado",
        help_text="Digite o estado aqui.",
    )
    cep = models.CharField(
        max_length=9,
        null=True,
        blank=True,
        verbose_name="CEP",
        help_text="Digite o CEP aqui no formato XXXXX-XXX.",
    )
    complemento = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Complemento",
        help_text="Digite o complemento do endereço aqui.",
    )

    def idade(self):
        if self.data_nascimento:
            hoje = date.today()
            idade = hoje.year - self.data_nascimento.year
            return idade
        else:
            return None

    estado_civil = models.CharField(max_length=100, verbose_name="Estado Civil")
    rg = models.CharField(max_length=20, verbose_name="RG", null=False)
    DExp = models.CharField(
        max_length=20,
        verbose_name="Data expiração",
        null=False,
        help_text="Diga a data de expedição do documento",
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=False,
        blank=True,
        verbose_name="CPF",
        help_text="Digite seu CPF aqui modelo: 000.000.000-00",
    )
    escolaridade = models.CharField(max_length=100, null=True)
    profissao = models.CharField(max_length=100, verbose_name="Profissão")
    renda = models.FloatField(null=True, verbose_name="Renda")
    ocupacao_atual = models.CharField(
        max_length=100, null=True, verbose_name="Ocupação atual"
    )
    beneficio_Gov = models.CharField(
        max_length=4, null=True, choices=tipos_beneficio_Gov
    )
    renda_gov = models.FloatField(null=True, verbose_name="Renda do governo")

    tipo_moradia = (
        ("A", "Aluguel"),
        ("C", "Cessão"),
        ("F", "Financiada"),
        ("I", "Invasão"),
        ("P", "Própria"),
    )
    tipo_morada = (
        ("Alvenida", "Alvenida"),
        ("Papelão", "Papelão"),
        ("Palafita", "Palafita"),
        ("Madeira", "Madeira"),
        ("Lona", "Lona"),
        ("Plástico", "Plástico"),
    )
    minha_moradia = models.CharField(
        max_length=1, choices=tipo_moradia, verbose_name="Estado da moradia"
    )
    minha_morada = models.CharField(
        max_length=10, choices=tipo_morada, verbose_name="Detalhes da moradia"
    )
    quantidade_comodos = models.IntegerField(
        null=False, default=0, verbose_name="Quantidade de cômodo"
    )
    quartos = models.IntegerField(verbose_name="Quantidade de quarto(s)")
    sala = models.IntegerField(verbose_name="Quantidade de sala(s)")
    cozinha = models.IntegerField(verbose_name="QuantidAade de cozinha(s)")
    banheiro = models.IntegerField(verbose_name="Quantidade de banheiro(s)")
    # no html pergunta se tem:
    agua_encanada = models.BooleanField(default=False, verbose_name="Água encanada")
    esgoto = models.BooleanField(default=False, verbose_name="Esgoto")
    energia = models.BooleanField(default=False, verbose_name="Energia")
    coleta_lixo = models.BooleanField(default=False, verbose_name="Coleta de lixo")
    # valores da pessoa que cadastrou
    finished_at = models.DateField(null=True, verbose_name="Data finalizado")

    def mark_has_complete(self):
        if not self.finished_at:
            self.finished_at = date.today()
            self.save()


# Dados Parentes da criança---------------------------------------------------------------------------------------------


class MembroFamilia(models.Model):
    sexo_tipo = (("M", "Masculino"), ("F", "Feminino"))
    cadastro = models.ForeignKey(
        Cadastro, on_delete=models.CASCADE, related_name="membroFamilia"
    )
    nome = models.CharField(
        max_length=100,
        null=False,
        verbose_name="Nome",
        help_text="Digite o nome aqui.",
    )
    sexo = models.CharField(max_length=1, choices=sexo_tipo, verbose_name="Sexo")
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    estado_civil = models.CharField(
        max_length=100, verbose_name="Estado Civil", null=False
    )
    vinculo_familia = models.CharField(max_length=100, null=True)
    # separa termo no html
    telefone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Telefone",
        help_text="Digite o número de telefone aqui.",
    )
    celular = models.CharField(
        max_length=15,
        null=False,
        blank=True,
        verbose_name="Telefone",
        help_text="Digite seu Telefone aqui. como no exemplo: (21) 9xxxx-xxxx",
    )

    escolaridade = models.CharField(max_length=100, null=True)
    profissao = models.CharField(max_length=100, verbose_name="Profissão")
    renda = models.FloatField(null=True, verbose_name="Renda")
    ocupacao_atual = models.CharField(
        max_length=100, null=True, verbose_name="Ocupação atual"
    )
