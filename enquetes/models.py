from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser
from django.utils.text import Truncator

class User(AbstractUser):
    """Extende o modelo base do Django
    aqui podemos adicionar campos personalizados"""

    pass
    
    def __str__(self):
        return self.username

class Enquete(models.Model):
    """informação necesaria e basica de um enquete"""

    titulo = models.CharField(max_length=120)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enquetes_criados")
    usuarios = models.ManyToManyField(User, through="EnqueteEmUso") # through indica a Django que usaremos uma tabela intermediaria pra adicionar iformações 

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

# TODO de todos esse modelo é o que ainda não estou certo de como pode ficar
class PerguntaEmUso(models.Model):
    """A ideia de esto é fazer seguimento das resposatas dadas pelo usuario
    """
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name="em_uso")
    
    # tenho duvidas se ussar esse campo, pois o modelo pode servir sem ele 
    # enqute_em_uso = models.ForeignKey(EnqueteEmUso, on_delete=models.CASCADE, related_name="perguntas_em_uso")
    
    eleicao = models.ForeignKey(Opcoes, null=True, on_delete=models.SET_NULL, related_name="escolhda_em_pergunta")

    def save(self, *args, **kwargs):
        """conferindo qua a eleicao forme parte das opcoes da pergunta correspondiente"""

        if self.eleicao not in self.pergunta.opcoes.all():
            raise ValueError('Eleicao invalida, por favor eliga uma opcao que corresponda á pergunta')

        super(PerguntaEmUso, self).save(*args, **kwargs) # chamo ao metodo save 'original'
        
    class Meta:
        pass

        # TODO aggregar uma constrain para impedir que o usuario responda duas veces a misma pergunta 
    
    def __str__(self):
        return f'{self.pergunta} #{self.pergunta.id}'
