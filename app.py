import json
import sys
sys.getdefaultencoding()
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Email

# Функция для записи данных в файл
def write_to_file(data):
    print("Writing data to file:", data)  # Добавляем отладочный вывод
    with open('user_data.json', 'a', encoding='utf-8') as file:  # Указываем кодировку UTF-8
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')  # Добавляем символ новой строки

def read_from_file():
    try:
        with open('user_data.json', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        last_line = lines[-1]  # Берем только последнюю строку из файла
        data = json.loads(last_line)
        return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
        return {}


# Создание экземпляра приложения Flask
app = Flask(__name__)
app.secret_key = 'any secret string'

# Класс формы для анкеты пользователя
class UserForm(FlaskForm):
    name = StringField('Имя', validators=[InputRequired()])
    age = IntegerField('Возраст', validators=[InputRequired(), NumberRange(1)])
    email = StringField('Почта', validators=[InputRequired(), Email()])
    submit = SubmitField('Отправить')

# Маршрут для отображения и обработки формы
@app.route('/', methods=['GET', 'POST'])
def user_form():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        email = form.email.data

        user_data = {
            'name': name,
            'age': age,
            'email': email
        }

        write_to_file(user_data)  # Запись информации о пользователе в файл

        return redirect(url_for('success', name=name))  # Перенаправление на страницу успеха с передачей имени пользователя
    return render_template('user_form.html', form=form)

@app.route('/success')
def success():
    name = request.args.get('name')  # Получаем имя из параметров URL
    return render_template('success.html', name=name)  # Отображаем страницу успеха с переданным именем

if __name__ == '__main__':
    app.run(debug=False, port=8000)