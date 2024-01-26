from django.contrib import admin
from enquetes.models import User, Enquete, Pergunta, Opcoes,\
    EnqueteEmUso, Voto

class OpcoesInline(admin.TabularInline):
    """para registrar as Opcoes como parte da admin view de Perguntas"""
    
    model = Opcoes
    extra = 1

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    """registra o modelo Pergunta e coloca um formset de Opcoes dentro dele"""
    
    inlines = [OpcoesInline]

class PerguntaInline(admin.TabularInline):
    """para registrar as Perguntas como parte da admin view de Enquete"""
    
    model = Pergunta
    extra = 1
    show_change_link = True

@admin.register(Enquete)
class EnqueteAdmin(admin.ModelAdmin):
    """registra o modelo Enquete y coloca um form de Pergunta dentro dele"""

    list_display = ["titulo", "criador"]
    search_fields = ["titulo", "criador"]
    inlines = [PerguntaInline]

@admin.register(EnqueteEmUso)
class EnqueteEmUsoAdmin(admin.ModelAdmin):
    """registra o modelo Enquete em Uso"""

    list_display = ["enquete", "compretado"]

@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    """registra o modelo Voto em Uso"""
    pass

# registra o modelo User
admin.site.register(User)