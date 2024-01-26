from django.contrib import admin
from enquetes.models import User, Enquete, Pergunta, Opcoes,\
    EnqueteEmUso, PerguntaEmUso

class OpcoesInline(admin.TabularInline):
    """para registrar as Opcoes como parte do modelo PerguntasAdmin no admin"""
    model = Opcoes
    extra = 1

# TODO implementar algo como get_queryset para filtrar as opcoes valida no formulario
class PerguntaEmUsoInline(admin.TabularInline):
    """para registrar as PerguntasEmUso como parte do modelo EnqueteAdmin no admin"""
    model = PerguntaEmUso
    extra = 1

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    """registra o modelo Pergunta y asigna de fato os modelos Opcoes e
    Pergumtas em Uso dentro dele"""

    inlines = [OpcoesInline, PerguntaEmUsoInline]


class PerguntaInline(admin.TabularInline):
    """para registrar as Perguntas como parte do modelo Enquete no admin"""
    
    model = Pergunta
    extra = 1
    show_change_link = True



@admin.register(Enquete)
class EnqueteAdmin(admin.ModelAdmin):
    """registra o modelo Enquete y asigna de fato o modelos Pergunta dentro dele"""

    list_display = ["titulo", "criador"]
    search_fields = ["titulo", "criador"]
    inlines = [PerguntaInline]



@admin.register(EnqueteEmUso)
class EnqueteEmUsoAdmin(admin.ModelAdmin):
    """registra o modelo Enquete em Uso"""
    list_display = ["enquete", "compretado"]

# registra o modelo User
admin.site.register(User)