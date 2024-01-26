from django.test import TestCase
from django.db.models import Count
from enquetes.models import (
    User,
    Enquete,
    EnqueteEmUso,
    Pergunta,
    Opcoes,
    Voto,
)

class TestVoto(TestCase):
    def setUp(self):

        # ==== USERS ====
        user_1_data = {
            'username': 'Joao',
            'password': '1234',
        }
        user_2_data = {
            'username': 'tiago',
            'password': '5678',
        }
        user_3_data = {
            'username': 'maximiliano',
            'password': 'password',
        }
        self.user1 = User.objects.create(**user_1_data)
        self.user2 = User.objects.create(**user_2_data)
        self.user3 = User.objects.create(**user_3_data)

        # ==== ENQUETES ====
        
        enquete_1_data = {
            'titulo': 'Comidas do Brasil',
            'criador': self.user1,
            # categoria pode ser null
            # usuario nao precisa porque é many to many
            # aberto é True por default
        }

        self.enquete1 = Enquete.objects.create(**enquete_1_data)

        # ==== PERGUNTAS ====

        # pra enquete1

        pergunta_1 = {
            'titulo' : 'Qual é a comida mais gostosa do Brasil?',
            'enquete' : self.enquete1
        }

        self.enquete1_pergunta_1 = Pergunta.objects.create(**pergunta_1)
        
        
        # ==== OPCOES ====

        # pra enquete1
        #       pergunta1

        opcao_1 = {
            'descricao' : "O Päo de Queijo",
            'pergunta' : self.enquete1_pergunta_1
        }
        opcao_2 = {
            'descricao' : "A farofa de Mandioca",
            'pergunta' : self.enquete1_pergunta_1
        }
        opcao_3 = {
            'descricao' : "Feijoada",
            'pergunta' : self.enquete1_pergunta_1
        }

        self.enquete1_pergunta_1_opcao_1 = Opcoes.objects.create(**opcao_1)
        self.enquete1_pergunta_1_opcao_2 = Opcoes.objects.create(**opcao_2)
        self.enquete1_pergunta_1_opcao_3 = Opcoes.objects.create(**opcao_3)

    def test_configuration(self):
        """checks the setUp is correct"""
        self.assertIsInstance(self.user1, User)
        self.assertIsInstance(self.user2, User)
        self.assertIsInstance(self.user3, User)
        self.assertIsInstance(self.enquete1, Enquete)
        self.assertIsInstance(self.enquete1_pergunta_1, Pergunta)
        self.assertIsInstance(self.enquete1_pergunta_1_opcao_1, Opcoes)
        self.assertIsInstance(self.enquete1_pergunta_1_opcao_2, Opcoes)
        self.assertIsInstance(self.enquete1_pergunta_1_opcao_3, Opcoes)
        
    def test_users_can_vote(self):
        voto = Voto(
            usuario=self.user2,
            enquete=self.enquete1,
            pergunta=self.enquete1_pergunta_1,
            resposta=self.enquete1_pergunta_1_opcao_2
        )
        instancias_da_enquete1 = self.enquete1.em_uso.all().count()
        self.assertIsInstance(voto, Voto)

        ### AQUI VI QUE DA PRA FAZER VOTO SEM CRIAR 
        ### MODELO DE ENQUETE EM USO
        
        self.assertEquals(1, instancias_da_enquete1)