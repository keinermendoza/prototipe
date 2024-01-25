from django.contrib import admin
from enquetes.models import User, Enquete, Pergunta, Opcoes,\
    EnqueteEmUso, PerguntaEmUso

class OpcoesInline(admin.TabularInline):
    model = Opcoes
    extra = 1

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    inlines = [OpcoesInline]


class PerguntaInline(admin.TabularInline):
    model = Pergunta
    extra = 1
    show_change_link = True

@admin.register(Enquete)
class EnqueteAdmin(admin.ModelAdmin):
    list_display = ["titulo", "criador"]
    search_fields = ["titulo", "criador"]
    inlines = [PerguntaInline]


class PerguntaEmUsoInline(admin.TabularInline):
    model = PerguntaEmUso
    extra = 1

# TODO implementar algo como get_queryset para filtrar as opcoes valida no formulario
@admin.register(EnqueteEmUso)
class EnqueteEmUsoAdmin(admin.ModelAdmin):
    list_display = ["enquete", "compretado"]
    inlines = [PerguntaEmUsoInline]

admin.site.register(User)