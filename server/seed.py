#!/usr/bin/env python3

from random import randint
from faker import Faker

from app import app
from models import db, Article, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Article.query.delete()
    User.query.delete()

    print("Creating users...")
    users = []
    usernames = []
    for i in range(25):
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()

        usernames.append(username)
        user = User(username=username)
        users.append(user)

    # Add the specific user 'Tuei'
    tuei_user = User(username="Tuei")
    users.append(tuei_user)

    db.session.add_all(users)

    print("Usernames added:")
    for user in users:
        print(f"- {user.username}")

    print("Creating articles...")
    articles = []
    for i in range(100):
        content = fake.paragraph(nb_sentences=8)
        preview = content[:25] + '...'

        article = Article(
            author=fake.name(),
            title=fake.sentence(),
            content=content,
            preview=preview,
            minutes_to_read=randint(1, 20),
        )

        articles.append(article)

    db.session.add_all(articles)

    db.session.commit()
    print("Seeding complete.")
