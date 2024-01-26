from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser
from django.utils.text import Truncator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    """Extende o modelo base do Django
    aqui podemos adicionar campos personalizados"""

    pass
    
    def __str__(self):
        return self.username

class Categoria(models.Model):
    titulo = models.CharField(max_length=120)

    def __str__(self):
        return self.titulo

class Enquete(models.Model):
    """informação necesaria e basica de um enquete"""

    titulo = models.CharField(max_length=120)
    categoria = models.ForeignKey(Categoria, blank=True, null=True, related_name="enquetes", on_delete=models.SET_NULL)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enquetes_criados")
    usuarios = models.ManyToManyField(User, through="EnqueteEmUso") # through indica a Django que usaremos uma tabela intermediaria pra adicionar iformações 
    aberto = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
    
class Pergunta(models.Model):
    """informação necesaria e basica de uma pergunta"""

    titulo = models.CharField(max_length=120)
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name="perguntas")
    
    def __str__(self):
        return self.titulo
    
class Opcoes(models.Model):
    """informação necesaria e basica de uma opção"""

    descricao = models.TextField()
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name="opcoes")

    def __str__(self) -> str: 
        """o Truncator simplesmente limita o numero de palavras"""
        return Truncator(self.descricao).words(5)


class Voto(models.Model):
    """representa um voto"""

    usuario = models.ForeignKey(User, blank=True, related_name="votos", on_delete=models.CASCADE)
    enquete = models.ForeignKey(Enquete, related_name="votos", on_delete=models.DO_NOTHING)
    pergunta = models.ForeignKey(Pergunta, related_name="votos", on_delete=models.DO_NOTHING)
    resposta = models.ForeignKey(Opcoes, blank=True, null=True, related_name="votos", on_delete=models.SET_NULL)

    def __str__(self):
        return f"escolha #{self.resposta.id} em #{self.enquete.id}/{self.pergunta.id}"
    
    def save(self, *args, **kwargs):
        """conferindo qua a resposta corresponda á pergunta
        e a pergunta correspona ao enquete"""

        if self.resposta not in self.pergunta.opcoes.all():
            raise ValidationError('resposta invalida, por favor escolha uma opcao que corresponda á pergunta')
        
        if self.pergunta not in self.enquete.perguntas.all():
            raise ValidationError('pergunta invalida, por favor escolha uma opcao que corresponda ao enquete')

        super(Voto, self).save(*args, **kwargs) # chamo ao metodo save 'original'

    
# ====          MODELOS INTERMEDIARIOS          ===

class EnqueteEmUso(models.Model):
    """Tabela intermediaria, por enquanto a sua função é fazer seguimento
    de quando uma instacia de enquete tem se compretado, mais a gente pode
    agregar outras propriedades relacionadas com as instancias de enquetes"""

    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name="em_uso")
    usuario = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="enquetes_participados")
    compretado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.enquete} #{self.enquete.id}'
