from django import forms
from cadastroAdmin.models import AdminEspelho, CadastroEspelho, MembroFamiliaEspelho

# para cadastrar Administrador
# ----------------------------------------------------------------------------------------------------------------------
class AdminForm(forms.ModelForm):
    class Meta:
        model = AdminEspelho
        fields = ["nome", "email", "cpf", "senha", "telefone"]
        widgets = {
            "senha": forms.PasswordInput(),
        }

# ----------------------------------------------------------------------------------------------------------------------


# para atualizar e cadastrar crianças
# ----------------------------------------------------------------------------------------------------------------------
class CadastroEspelhoForm(forms.ModelForm):
    class Meta:
        model = CadastroEspelho
        fields = '__all__'
        exclude = ['finished_at']


class MembroFamiliaEspelhoForm(forms.ModelForm):
    class Meta:
        model = MembroFamiliaEspelho
        fields = '__all__'

# ----------------------------------------------------------------------------------------------------------------------
