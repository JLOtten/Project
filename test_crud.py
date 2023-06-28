import unittest
import app
from crud import save_encouragement
from model import Encouragement
import pytest

class TestCrudFunctions(unittest.TestCase):

    def setUp(self):
        self.client = app.app.test_client()
        app.app.config['TESTING'] = True

    @pytest.mark.skip(reason="no way of creating duplicate encouragements yet")
    def test_save_encouragement_to_database(self):
        with app.app.app_context():
            text = "You're doing great!"
            language = "en"
            save_encouragement(text, language)
            encouragement = Encouragement.query.filter_by(text=text).first()
            self.assertIsNotNone(encouragement)
            self.assertEqual(encouragement.language, language)
            app.db.session.delete(encouragement)