# Generated by Django 5.0.4 on 2024-05-08 15:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cadastros", "0002_alter_cadastrovoluntario_situacao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cadastrovoluntario",
            name="situacao",
            field=models.CharField(
                max_length=100, null=True, verbose_name="Situação"
            ),
        ),
    ]