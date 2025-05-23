from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus


class CadastrarGetRedirectTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.get(reverse("cadastrar"))

    def test_template_cadastrar_redirect(self):
        self.assertRedirects(self.resp, reverse('login')+"?next=/cadastrar/", status_code=HTTPStatus.FOUND, target_status_code=HTTPStatus.OK,fetch_redirect_response=True)

class CadastrarGetTest(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")
        self.resp = self.client.get(reverse("cadastrar"))

    def test_response(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_template_cadastrar(self):
        self.assertTemplateUsed(self.resp, 'cadastrar.html')

class CadastrarPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")

        post_data = {
            "nome_completo" : "João da Silva",
            "telefone" : "(19) 99999-8888",
            "email" : "joao.silva@example.com",
            "observacao" : "Cliente importante, prefere contato por e-mail."}

        self.resp = self.client.post(reverse("cadastrar"), post_data)
        self.resp_error = self.client.post(reverse("cadastrar"))

    def test_template_cadastrar(self):
        self.assertTemplateUsed(self.resp, 'cadastrar.html')

    def test_response(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_post_sucess(self):
        self.assertNotContains(self.resp, '<div class="alert alert-primary"')

    def test_post_error(self):
        self.assertContains(self.resp_error, '<div class="alert alert-primary"')
