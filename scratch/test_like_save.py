import unittest
import json
import sqlite3
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app as flask_app
import mock_data

class TestLikeSaveFeature(unittest.TestCase):
    def setUp(self):
        flask_app.app.config['TESTING'] = True
        flask_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = flask_app.app.test_client()

    def test_mock_data_likes_zero(self):
        """Ensure all mock data entries start with exactly 0 likes."""
        for item in mock_data._all_landing_stories():
            self.assertEqual(item.get("likes", 0), 0, f"Item {item.get('id')} has non-zero likes")
        for domain in mock_data._DOMAIN_MAP.keys():
            items = mock_data.get_mock_data(domain)
            for item in items:
                self.assertEqual(item.get("likes", 0), 0, f"Item {item.get('title')} has non-zero likes")

    def test_landing_page_surfable_and_no_demo_button(self):
        """Check landing page renders dummy stories and has no 'demo' button."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        # Check dummy data is present
        self.assertIn("Blackwell", html)
        self.assertIn("ISRO", html)
        # Check no demo button / demo label
        self.assertNotIn("demo button", html.lower())
        self.assertNotIn("demo mode", html.lower())
        self.assertNotIn(">demo<", html.lower())
        # Check buttons do not show "0" next to Like or Save
        self.assertNotIn("Like 0", html)
        self.assertNotIn("Liked 0", html)
        self.assertNotIn("Save 0", html)
        self.assertNotIn("Saved 0", html)
        self.assertNotIn("<span class=\"action-count\">0</span>", html)

    def test_unauthenticated_like_save_blocked(self):
        """Unauthenticated requests to /like, /unlike, /save, /unsave should return 401 JSON."""
        res = self.client.post('/like', data=json.dumps({'link': 'https://example.com/test'}), content_type='application/json')
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'), 'login_required')

        res = self.client.post('/save', data=json.dumps({'link': 'https://example.com/test', 'title': 'Test'}), content_type='application/json')
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'), 'login_required')

    def test_authenticated_like_flow_counts(self):
        """Test liking and unliking as authenticated users and count transitions (0 -> 1 -> 2 -> 1 -> 0)."""
        test_link = "https://example.com/smartsearch-test-article"

        # Clean up any existing records for test_link in DB
        with sqlite3.connect('smartsearch.db') as conn:
            conn.execute("DELETE FROM liked_results WHERE link = ?", (test_link,))
            conn.execute("DELETE FROM saved_results WHERE link = ?", (test_link,))
            conn.commit()

        # Simulate User 1 login via session
        with self.client.session_transaction() as sess:
            sess['user_id'] = 99901
            sess['email'] = 'testuser1@example.com'

        # Initial like from user 1: count becomes 1
        res = self.client.post('/like', data=json.dumps({'link': test_link}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

        # Switch to User 2
        with self.client.session_transaction() as sess:
            sess['user_id'] = 99902
            sess['email'] = 'testuser2@example.com'

        # Like from user 2: count becomes 2
        res = self.client.post('/like', data=json.dumps({'link': test_link}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)

        # Unlike from user 2: count becomes 1
        res = self.client.post('/unlike', data=json.dumps({'link': test_link}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

        # Switch back to User 1 and unlike: count becomes 0
        with self.client.session_transaction() as sess:
            sess['user_id'] = 99901
            sess['email'] = 'testuser1@example.com'

        res = self.client.post('/unlike', data=json.dumps({'link': test_link}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 0)

        # Cleanup
        with sqlite3.connect('smartsearch.db') as conn:
            conn.execute("DELETE FROM liked_results WHERE link = ?", (test_link,))
            conn.commit()

    def test_authenticated_save_flow_counts(self):
        """Test saving and unsaving as authenticated users and count transitions."""
        test_link = "https://example.com/smartsearch-save-test"

        # Clean up
        with sqlite3.connect('smartsearch.db') as conn:
            conn.execute("DELETE FROM saved_results WHERE link = ?", (test_link,))
            conn.commit()

        # Simulate User 1 login
        with self.client.session_transaction() as sess:
            sess['user_id'] = 99901
            sess['email'] = 'testuser1@example.com'

        res = self.client.post('/save', data=json.dumps({
            'link': test_link,
            'title': 'Test Save Story',
            'snippet': 'A snippet',
            'source': 'Test Source'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

        # Switch to User 2
        with self.client.session_transaction() as sess:
            sess['user_id'] = 99902
            sess['email'] = 'testuser2@example.com'

        res = self.client.post('/save', data=json.dumps({
            'link': test_link,
            'title': 'Test Save Story',
            'snippet': 'A snippet',
            'source': 'Test Source'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)

        # User 2 unsaves
        res = self.client.post('/unsave', data=json.dumps({'link': test_link}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

        # Cleanup
        with sqlite3.connect('smartsearch.db') as conn:
            conn.execute("DELETE FROM saved_results WHERE link = ?", (test_link,))
            conn.commit()

if __name__ == '__main__':
    unittest.main()
