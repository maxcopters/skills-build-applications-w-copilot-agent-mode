from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from djongo import models

from octofit_tracker import models as octo_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Suppression des anciennes données...'))
        # Suppression dans l'ordre des dépendances (enfants avant parents)
        for model in [octo_models.Activity, octo_models.Workout, octo_models.Leaderboard, octo_models.User, octo_models.Team]:
            try:
                model.objects.all().delete()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Suppression ignorée pour {model.__name__}: {e}"))

        self.stdout.write(self.style.SUCCESS('Création des équipes...'))
        marvel = octo_models.Team.objects.create(name='Marvel')
        dc = octo_models.Team.objects.create(name='DC')

        self.stdout.write(self.style.SUCCESS('Création des utilisateurs...'))
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': marvel},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': marvel},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': dc},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': dc},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user_objs.append(octo_models.User.objects.create(name=u['name'], email=u['email'], team=u['team']))

        self.stdout.write(self.style.SUCCESS('Création des activités...'))
        for user in user_objs:
            octo_models.Activity.objects.create(user=user, type='Running', duration=30)
            octo_models.Activity.objects.create(user=user, type='Cycling', duration=45)

        self.stdout.write(self.style.SUCCESS('Création des workouts...'))
        for user in user_objs:
            octo_models.Workout.objects.create(user=user, description='Full body workout', duration=60)

        self.stdout.write(self.style.SUCCESS('Création du leaderboard...'))
        for team in [marvel, dc]:
            octo_models.Leaderboard.objects.create(team=team, points=100)

        self.stdout.write(self.style.SUCCESS('Création d\'un index unique sur le champ email des utilisateurs...'))
        try:
            with connection.cursor() as cursor:
                cursor.execute('db.users.createIndex({ "email": 1 }, { unique: true })')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Index non créé ou déjà existant: {e}"))

        self.stdout.write(self.style.SUCCESS('Base de données octofit_db peuplée avec succès !'))
