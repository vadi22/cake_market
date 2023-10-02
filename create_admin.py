from getpass import getpass
import sys

from webapp import create_app
from webapp.models import User, db

app = create_app()
with app.app_context():
    email = input('Введите свою почту: ')

    if User.query.filter(User.email == email).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        sys.exit(0)

    email = 'admin'

    new_user = User(email=email, active =  True, role=1, telegram_id ='admin')
    new_user.set_password(password)
    email = 'admin'

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))