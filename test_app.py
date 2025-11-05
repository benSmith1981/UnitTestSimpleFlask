import unittest
import os
import sqlite3
from app import app, init_db
class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test"
        self.client = app.test_client()
        # Temporary DB setup
        if os.path.exists("test.db"):
            os.remove("test.db")
        conn = sqlite3.connect("test.db")
        conn.execute("CREATE TABLE submissions (id INTEGER PRIMARY KEY, name TEXT, message TEXT)")
        conn.commit()
        conn.close()
        #tell the app config to setup a value for the key DATABASE to point to test DB
        app.config["DATABASE"] = "test.db"

    def test_home_page_loads(self):
        response = self.client.get("/chin")
        self.assertEqual(response.status_code, 200)
        #this tests if the text exists in your page so we know it loaded
        self.assertIn(b"Submit Your Message", response.data)


    def test_user_saved_in_database(self):
        self.client.post("/", data={"name": "Bob", "message": "Hello!"}, follow_redirects=True)
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        c.execute("SELECT name FROM submissions WHERE name = 'Bob'")
        result = c.fetchone()
        print(result)
        conn.close()
        self.assertIsNotNone(result)

    def tearDown(self):
        if os.path.exists("test.db"):
            os.remove("test.db")
if __name__ == "__main__":
    unittest.main()