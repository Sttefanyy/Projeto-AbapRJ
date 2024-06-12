from django.contrib import admin
from .models import Cadastro, MembroFamilia, CadastroVoluntario


@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin): ...


@admin.register(MembroFamilia)
class MembroFamiliaAdmin(admin.ModelAdmin): ...


@admin.register(CadastroVoluntario)
class CadastroVoluntarioAdmin(admin.ModelAdmin): ...
