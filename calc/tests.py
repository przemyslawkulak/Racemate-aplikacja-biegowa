import unittest

# ./manage.py test calc
# Create your tests here.
from calc.views import generate_result


class GenerateResultTest(unittest.TestCase):

    def test_correct_3(self):
        self.assertEqual(generate_result(30, 1), '17min 56sec ')

    def test_correct_5(self):
        self.assertEqual(generate_result(30, 2), '30min 40sec ')

    def test_correct_10(self):
        self.assertEqual(generate_result(30, 3), '1h 3min 46sec ')

    def test_correct_half(self):
        self.assertEqual(generate_result(30, 4), '2h 21min 4sec ')

    def test_correct_marathon(self):
        self.assertEqual(generate_result(30, 5), '4h 49min 17sec ')

    def test_max_marathon(self):
        self.assertEqual(generate_result(60, 5), '2h 43min 25sec ')

    def test_incorrect_efficiency(self):
        self.assertEqual(generate_result(61, 3), 'Incorrect efficiency')

    def test_incorrect_distance(self):
        self.assertEqual(generate_result(60, 6), 'Incorrect distance')

    def test_distance_str(self):
        self.assertEqual(generate_result(60, '5'), 'Incorrect distance')

    def test_efficiency_str(self):
        self.assertEqual(generate_result('60', 5), 'Incorrect efficiency')

    def test_distance_float(self):
        self.assertEqual(generate_result(60, 5.0), 'Incorrect distance')

    def test_efficiency_float(self):
        self.assertEqual(generate_result(60.0, 5), 'Incorrect efficiency')
