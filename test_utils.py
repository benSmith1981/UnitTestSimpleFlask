import unittest
from utils import greet_user, double_number
class TestUtils(unittest.TestCase):
    def test_greet_user(self):
        self.assertEqual(greet_user("Garv"),"GarvGarvGarvGarvGarvGarvGarvGarvGarvGarv")    
        self.assertEqual(greet_user("Ben"),"BenBenBenBenBenBenBenBenBenBen")