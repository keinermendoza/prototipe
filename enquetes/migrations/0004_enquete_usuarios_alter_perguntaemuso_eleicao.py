# Generated by Django 5.0.1 on 2024-01-25 23:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enquetes", "0003_alter_opcoes_pergunta"),
    ]

    operations = [
        migrations.AddField(
            model_name="enquete",
            name="usuarios",
            field=models.ManyToManyField(
                through="enquetes.EnqueteEmUso", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="perguntaemuso",
            name="eleicao",
            field=models.ForeignKey(
                limit_choices_to=models.Q(
                    ("pergunta__opcoes", models.F("pergunta__opcoes"))
                ),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="escolhda_em_pergunta",
                to="enquetes.opcoes",
            ),
        ),
    ]
