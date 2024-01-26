# Generated by Django 5.0.1 on 2024-01-25 22:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enquetes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="perguntaemuso",
            name="eleicao",
            field=models.ForeignKey(
                limit_choices_to=models.Q(("pergunta", models.F("pergunta"))),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="escolhda_em_pergunta",
                to="enquetes.opcoes",
            ),
        ),
    ]
