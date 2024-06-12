from django import forms

from cadastros.models import Login, CadastroVoluntario, Cadastro, MembroFamilia

# Login e formulário
class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = [
            "email",
            "senha",
            "opcao"
        ]
        widgets = {
            "senha": forms.PasswordInput(),
        }


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
# ----------------------------------------------------------------------------------------------------------------------


# Lógica pra cadastrar.
class CadastroEspelhoForm(forms.ModelForm):
    class Meta:
        model = Cadastro
        fields = '__all__'
        exclude = ['finished_at']


class MembroFamiliaForm(forms.ModelForm):
    class Meta:
        model = MembroFamilia
        fields = '__all__'
