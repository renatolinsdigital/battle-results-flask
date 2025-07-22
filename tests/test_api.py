from db_models.battle_entry import BattleEntry
from config.database import db
from app import app
import os
import sys
import unittest
from datetime import datetime

# Add parent directory to path to import from project
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class BattleResultsTestCase(unittest.TestCase):
    """Test case for the Battle Results Flask API"""

    def setUp(self):
        """Set up a test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

            # Add test data
            test_entry = BattleEntry(
                game_tag='test_game',
                player_1_name='Test Player 1',
                player_2_name='Test Player 2',
                winner_name='Test Player 2'
            )
            db.session.add(test_entry)
            db.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_entries(self):
        """Test getting all entries"""
        response = self.client.get('/entries')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('entries', data)
        self.assertEqual(len(data['entries']), 1)
        self.assertEqual(data['entries'][0]['gameTag'], 'test_game')

    def test_get_single_entry(self):
        """Test getting a single entry"""
        response = self.client.get('/entries/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('entry', data)
        self.assertEqual(data['entry']['gameTag'], 'test_game')

    def test_create_entry(self):
        """Test creating a new entry"""
        entry_data = {
            'gameTag': 'new_test_game',
            'player1Name': 'New Player 1',
            'player2Name': 'New Player 2',
            'winnerName': 'New Player 2'
        }
        response = self.client.post('/entries', json=entry_data)
        self.assertEqual(response.status_code, 201)

        # Check if entry was actually created
        response = self.client.get('/entries/2')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['entry']['gameTag'], 'new_test_game')

    def test_update_entry(self):
        """Test updating an entry"""
        update_data = {
            'winnerName': 'Test Player 1'
        }
        response = self.client.patch('/entries/1', json=update_data)
        self.assertEqual(response.status_code, 200)

        # Check if entry was updated
        response = self.client.get('/entries/1')
        data = response.get_json()
        self.assertEqual(data['entry']['winnerName'], 'Test Player 1')

    def test_delete_entry(self):
        """Test deleting an entry"""
        response = self.client.delete('/entries/1')
        self.assertEqual(response.status_code, 200)

        # Verify entry was deleted
        response = self.client.get('/entries/1')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
