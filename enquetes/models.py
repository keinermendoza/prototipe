from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import Truncator

class User(AbstractUser):
    pass
    
    def __str__(self):
        return self.username

class Enquete(models.Model):
    titulo = models.CharField(max_length=120)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enquetes_criados")

    def __str__(self):
        return self.titulo
    
class Pergunta(models.Model):
    titulo = models.CharField(max_length=120)
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name="perguntas")
    
    def __str__(self):
        return self.titulo
    
class Opcoes(models.Model):
    descricao = models.TextField()
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name="perguntas")

    def __str__(self):
        return Truncator(self.descricao).words(5)
    
# MODELOS INTERMEDIARIOS

class EnqueteEmUso(models.Model):
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name="em_uso")
    usuario = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="enquetes_participados")
    compretado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.enquete} #{self.enquete.id}'
    
class PerguntaEmUso(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name="em_uso")
    enqute_em_uso = models.ForeignKey(EnqueteEmUso, on_delete=models.CASCADE, related_name="perguntas_em_uso")
    eleicao = models.ForeignKey(Opcoes, null=True, on_delete=models.SET_NULL, related_name="escolhda_em_pergunta")

    def __str__(self):
        return f'{self.pergunta} #{self.pergunta.id}'
