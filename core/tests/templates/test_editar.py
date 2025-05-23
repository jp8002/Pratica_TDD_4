from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from core.models import Agenda


class Editar_Redirect_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.get(reverse('editar'))

    def test_editar_redirect(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.FOUND)

class Editar_Get_Sem_Contatos_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.client = Client()
        new_user = User.objects.create(username='admin', email='aluno@fatec.sp.gov.br')
        new_user.set_password('123mudar')
        new_user.save()
        self.client.login(username="admin", password="123mudar")
        self.resp = self.client.get(reverse('editar'))

    def test_status_ok(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'editar.html')

    def test_sem_contatos(self):
        self.assertContains(self.resp, '<option selected hidden>Não há contatos</option>')

class Editar_Get_Com_Contatos_Test(TestCase):
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

        self.resp = self.client.get(reverse('editar'))
        self.respJsonOK = self.client.get(reverse('editar') + "?id=1")
        self.respJsonBad = self.client.get(reverse('editar') + "?id=10")

    def test_status_ok(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'editar.html')

    def test_json_status_ok(self):
        self.assertEqual(self.respJsonOK.status_code, HTTPStatus.OK)

    def test_json_status_bad(self):
        self.assertEqual(self.respJsonBad.status_code, HTTPStatus.BAD_REQUEST)

    def test_com_contatos(self):
        self.assertContains(self.resp, '<option value="1">1 - João da Silva</option>')

class Editar_Post_Sucess_Test(TestCase):
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

        post_data = {
            "id":a.id,
            "nome_completo": "Goku da Silva",
            "telefone": "(19) 99999-8888",
            "email": "joao.silva@example.com",
            "observacao": "Cliente importante, prefere contato por e-mail."}

        self.resp = self.client.post(reverse("editar"), post_data)

    def test_status_ok(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'editar.html')

    def test_sem_contatos(self):
        self.assertContains(self.resp, '<option value="1">1 - Goku da Silva</option>')

class Editar_Post_Failure_Test(TestCase):
    def setUp(self):
        self.client = Client()
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

        post_data = {
            "nome_completo": "Goku da Silva",
            "telefone": "(19) 99999-8888",
            "email": "joao.silva@example.com",
            "observacao": "Cliente importante, prefere contato por e-mail."}

        self.resp = self.client.post(reverse("editar"), post_data)

    def test_status_ok(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'editar.html')

    def test_sem_contatos(self):
        self.assertContains(self.resp, '<option value="1">1 - João da Silva</option>')
        self.assertContains(self.resp, 'Não foi possível salver o contato')