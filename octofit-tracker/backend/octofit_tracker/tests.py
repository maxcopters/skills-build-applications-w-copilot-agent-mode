from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class ModelSmokeTest(TestCase):
    def test_team_create(self):
        team = Team.objects.create(name='TestTeam')
        self.assertEqual(str(team), 'TestTeam')
    def test_user_create(self):
        team = Team.objects.create(name='TestTeam2')
        user = User.objects.create(name='TestUser', email='test@example.com', team=team)
        self.assertEqual(str(user), 'TestUser')
    def test_activity_create(self):
        team = Team.objects.create(name='TestTeam3')
        user = User.objects.create(name='TestUser2', email='test2@example.com', team=team)
        activity = Activity.objects.create(user=user, type='Run', duration=10)
        self.assertEqual(str(activity), 'Run - TestUser2')
    def test_workout_create(self):
        team = Team.objects.create(name='TestTeam4')
        user = User.objects.create(name='TestUser3', email='test3@example.com', team=team)
        workout = Workout.objects.create(user=user, description='Desc', duration=20)
        self.assertEqual(str(workout), 'Desc - TestUser3')
    def test_leaderboard_create(self):
        team = Team.objects.create(name='TestTeam5')
        leaderboard = Leaderboard.objects.create(team=team, points=42)
        self.assertEqual(str(leaderboard), 'TestTeam5: 42 pts')
