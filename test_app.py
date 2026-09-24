import unittest
from app import app


class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):

        response = self.app.get("/")

        self.assertEqual(
            response.status_code,
            200
        )

    def test_health_endpoint(self):

        response = self.app.get("/health")

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["status"],
            "healthy"
        )


if __name__ == "__main__":
    unittest.main()
