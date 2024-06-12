from cadastros.models import Cadastro, MembroFamilia, CadastroVoluntario, Admin


class CadastroEspelho(Cadastro):
    class Meta:
        proxy = True


class MembroFamiliaEspelho(MembroFamilia):
    class Meta:
        proxy = True


class CadastroVoluntarioEspelho(CadastroVoluntario):
    class Meta:
        proxy = True


class AdminEspelho(Admin):
    class Meta:
        proxy = True
