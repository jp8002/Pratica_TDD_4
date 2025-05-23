from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from core.models import Agenda


class Excluir_Get_Bad_Test(TestCase):
    def setUp(self):
        self.client = Client()

        self.resp = self.client.get(reverse("excluir"))

    def test_excluir_status(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.FOUND)

    def test_excluir_redirect(self):
        self.assertRedirects(self.resp, reverse('login') + "?next=/excluir/", status_code=HTTPStatus.FOUND, target_status_code=HTTPStatus.OK,fetch_redirect_response=True)

class Excluir_Get_OK_Empty_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")

        self.resp = self.client.get(reverse("excluir"))

    def test_excluir_status(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_excluir_template_used(self):
        self.assertTemplateUsed(self.resp, "excluir.html")

    def test_excluir_empty(self):
        self.assertContains(self.resp, "<option selected hidden>Não há contatos</option>")

class Excluir_Get_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")

        a = Agenda.objects.create(
            nome_completo="João da Silva",
            telefone="(19) 99999-8888",
            email="joao.silva@example.com",
            observacao="Cliente importante, prefere contato por e-mail."
        )

        self.resp = self.client.get(reverse("excluir"))

    def test_excluir_status(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_excluir_template_used(self):
        self.assertTemplateUsed(self.resp, "excluir.html")

    def test_excluir_Notempty(self):
        self.assertContains(self.resp, "<option selected hidden>Escolha um contato</option>")

class Excluir_Post_Failure_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")

        a = Agenda.objects.create(
            nome_completo="João da Silva",
            telefone="(19) 99999-8888",
            email="joao.silva@example.com",
            observacao="Cliente importante, prefere contato por e-mail."
        )

        self.resp = self.client.post(reverse("excluir"),{"id":999})

    def test_excluir_status(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_excluir_template_used(self):
        self.assertTemplateUsed(self.resp, "excluir.html")

    def test_excluir_fail(self):
        self.assertContains(self.resp," - João da Silva</option>")

class Excluir_Post_Sucess_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")

        a = Agenda.objects.create(
            nome_completo="João da Silva",
            telefone="(19) 99999-8888",
            email="joao.silva@example.com",
            observacao="Cliente importante, prefere contato por e-mail."
        )

        self.resp = self.client.post(reverse("excluir"),{"id":a.id})

    def test_excluir_status(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_excluir_template_used(self):
        self.assertTemplateUsed(self.resp, "excluir.html")

    def test_excluir_sucess(self):
        self.assertContains(self.resp,"<option selected hidden>Não há contatos</option>")

