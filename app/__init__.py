from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


from app import routes, models


def create_rooms(count: int):
    from random import randint
    from app.models import Room
    sess = db.session

    for i in range(count):
        busy = False
        cost = randint(2000, 14001) + randint(0, 101) / 100
        double_beds = randint(0, 3)
        single_beds = randint(0, 5)
        if double_beds == single_beds == 0:
            single_beds = 1

        showers = randint(0, 3)
        toilets = randint(1, 3)

        sess.add(Room(
            busy=busy, cost=cost,
            double_beds=double_beds,
            single_beds=single_beds,
            showers=showers,
            toilets=toilets
        ))
        sess.commit()


def create_tenants(count: int):
    from random import randint, choice
    from app.models import Tenant, User
    from sqlalchemy import select
    from sqlalchemy.exc import SQLAlchemyError

    sess = db.session
    stmt = select(User).where(User.id == 1)
    user = sess.execute(stmt).scalars().first()

    doc_nations = {
        'ru': 'Паспорт Росиийской федерации',
        'ua': 'Пасспорт України',
        'us': 'United States Passport'
    }
    pers_names = {
        'ru' or 0: {
            'firstname': [
                'Александр', 'Андрей', 'Егор', 'Максим', 'Максимилиан', 'Абрам',
                'Артём', 'Дмитрий', 'Ибрагим', 'Иосиф', 'Павел', 'Иван', 'Никита'
            ],
            'secondname': [
                'Александрович', 'Андреевич', 'Егорович', 'Максимович', 'Максимилианович', 'Абрамович',
                'Артёмович', 'Дмитриевич', 'Ибрагимович', 'Иосифич', 'Павлович', 'Иванович', 'Никитович'
            ],
            'lastname': [
                'Петров', 'Чацкий', 'Павлов', 'Егоров', 'Пиров', 'Нагой', 'Лабуда', 'Лавров',
                'Шароваров', 'Волков', 'Зуев', 'Калашматов', 'Романов', 'Марцинкевич', 'Шарашев', 'Васнецов'
            ]
        },
        'ua' or 1: {
            'firstname': [
                'Александр', 'Андрей', 'Егор', 'Максим', 'Максимилиан', 'Абрам',
                'Артём', 'Дмитрий', 'Ибрагим', 'Иосиф', 'Павел', 'Иван', 'Никита'
            ],
            'secondname': [
                'Александрович', 'Андреевич', 'Егорович', 'Максимович', 'Максимилианович', 'Абрамович',
                'Артёмович', 'Дмитриевич', 'Ибрагимович', 'Иосифич', 'Павлович', 'Иванович', 'Никитович'
            ],
            'lastname': [
                'Булько', 'Росавский', 'Парнюк', 'Шумейко', 'Андрусейко', 'Цушко', 'Марочко', 'Сирко',
                'Парипенко', 'Варенщук', 'Низушко', 'Хитрук', 'Намойко', 'Залейко', 'Таранец', 'Коломоец'
            ]
        },
        'us' or 2: {
            'firstname': [
                'Anthony', 'Daniel', 'Michael', 'Marshall', 'Theodore', 'Barth', 'Alexander', 'Liam',
                'Noah', 'Oliver', 'Elijah', 'James', 'Jonathan', 'Robert', 'Joshua', 'Elon'
            ],
            'lastname': [
                'Twist', 'James', 'Sheldon', 'Adams', 'Williams', 'Brown', 'Smith', 'Garcia',
                'Musk', 'Miller', 'Davis', 'Martin', 'Taylor', 'Harris', 'Thomas', 'Wilson'
            ]
        }
    }
    pers_tels = {
        'ru': '7',
        'ua': '380',
        'us': '1'
    }

    for i in range(count):
        nation      = choice(list(doc_nations.keys()))
        print(nation)
        nat_name    = pers_names.get(nation)
        firstname   = choice(nat_name.get('firstname'))
        secondname  = choice(nat_name.get('secondname')) + ' ' if not nation == 'us' else ''
        lastname    = choice(nat_name.get('lastname'))

        full_name       = f'{firstname} {secondname}{lastname}'
        doc_type        = doc_nations.get(nation)
        doc_number      = str(randint(100000, 1000000))
        date_of_birth   = f'{randint(1950, 2010)}-{randint(1, 12)}-{randint(1, 28)}'
        phone           = (pers_tels.get(nation) + str(randint(1000000000, 10000000000)))[:11:]
        email           = None

        try:
            if randint(1, 101) == 1 or not user:
                user = User(username='user'+doc_number[:2:], pass_hash=doc_number)
                sess.add(user)

            tenant = Tenant(
                user=user,
                full_name=full_name,
                doc_type=doc_type,
                doc_number=doc_number,
                date_of_birth=date_of_birth,
                phone=phone,
                email=email
            )

            sess.add(tenant)
            sess.commit()
        except SQLAlchemyError as e:
            print(e)
            sess.rollback()

