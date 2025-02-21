import unittest
from src.main import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_samples(self):
        response = self.app.get('/api/samples')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"SampleProject", response.data)

if __name__ == "__main__":
    unittest.main()