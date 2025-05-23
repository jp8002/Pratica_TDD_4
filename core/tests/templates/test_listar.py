from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus



class TestEmptyListarGet(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")

        self.resp = self.client.get(reverse("listar"))

    def test_response(self):
        self.assertEqual(HTTPStatus.OK, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, "listar.html")

    def test_empty_list(self):
        self.assertNotContains(self.resp, '<table id="lista-agendas"')

class TestListarGet(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")

        post_data = {
            "nome_completo": "João da Silva",
            "telefone": "(19) 99999-8888",
            "email": "joao.silva@example.com",
            "observacao": "Cliente importante, prefere contato por e-mail."}

        self.resp = self.client.post(reverse("cadastrar"), post_data)

        self.resp = self.client.get(reverse("listar"))

    def test_response(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, "listar.html")

    def test_list(self):
        self.assertContains(self.resp, '<table id="lista-agendas"')