import unittest
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_form_page(self):
        response = self.app.get('/')
        self.assertIn('Анкета пользователя', response.data.decode('utf-8'))

    def test_success_page(self):
        name = 'Test'
        age = 25
        email = 'test@example.com'

        # Отправляем POST запрос на главную страницу
        self.app.post('/', data=dict(name=name, age=age, email=email))

        # Затем отправляем GET запрос на страницу успеха
        response = self.app.get(f'/success?name={name}&age={age}&email={email}')

        # Проверяем, что имя пользователя отображается на странице успеха
        self.assertIn(f'Спасибо, {name}, ваша анкета успешно отправлена!', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()