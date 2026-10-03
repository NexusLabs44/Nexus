from django.test import SimpleTestCase, override_settings


@override_settings(ALLOWED_HOSTS=['testserver'])
class AccountViewTests(SimpleTestCase):
    def test_login_page_is_available(self):
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-mail')

    def test_register_page_is_available(self):
        response = self.client.get('/cadastro/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nome completo')

    def test_logout_redirects_to_login(self):
        response = self.client.get('/logout/')

        self.assertRedirects(response, '/login/')

    def test_protected_pages_redirect_anonymous_users_to_login(self):
        for path in ('/', '/calculadora/', '/perfil/', '/resultados/'):
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertRedirects(response, f'/login/?next={path}')