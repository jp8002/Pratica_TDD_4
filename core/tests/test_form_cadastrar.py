from django.test import TestCase

from core.forms import AgendaForm


class TestFormCadastrar(TestCase):
    def setUp(self):
        form_data = {
            "nome_completo" : "João da Silva",
            "telefone" : "(19) 99999-8888",
            "email" : "joao.silva@example.com",
            "observacao" : "Cliente importante, prefere contato por e-mail."
        }
        self.valid_form = AgendaForm(form_data)

    def test_form_valid(self):
        self.assertTrue(self.valid_form.is_valid())