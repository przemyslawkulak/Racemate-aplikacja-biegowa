import unittest

# ./manage.py test calc
# Create your tests here.
from calc.views import generate_result, adding_result, generate_tempo, adding_tempos


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


class AddingResultTest(unittest.TestCase):

    def test_correct(self):
        self.assertEqual(adding_result(30),
                         {'marathon': '4h 49min 17sec ', 'half': '2h 21min 4sec ', '10k': '1h 3min 46sec ',
                          '5k': '30min 40sec ', '3k': '17min 56sec '})

    def test_incorrect(self):
        self.assertEqual(adding_result(61), 'Incorrect efficiency')
        self.assertEqual(adding_result(29), 'Incorrect efficiency')

    def test_str(self):
        self.assertEqual(adding_result('61'), 'Incorrect efficiency')
        self.assertEqual(adding_result('29'), 'Incorrect efficiency')
        self.assertEqual(adding_result('35'), 'Incorrect efficiency')

    def test_float(self):
        self.assertEqual(adding_result(61.0), 'Incorrect efficiency')
        self.assertEqual(adding_result(29.0), 'Incorrect efficiency')
        self.assertEqual(adding_result(35.0), 'Incorrect efficiency')


class GenerateTemposTest(unittest.TestCase):

    def test_correct_easy(self):
        self.assertEqual(generate_tempo(30, 8), '7.74km/h')

    def test_correct_marathon(self):
        self.assertEqual(generate_tempo(30, 9), '8.51km/h')

    def test_correct_threshold(self):
        self.assertEqual(generate_tempo(30, 10), '9.38km/h')

    def test_correct_interval(self):
        self.assertEqual(generate_tempo(30, 11), '10.14km/h')

    def test_correct_repetition(self):
        self.assertEqual(generate_tempo(30, 12), '10.75km/h')

    def test_incorrect_type(self):
        self.assertEqual(generate_tempo(30, 13), 'Incorrect type')

    def test_incorrect_efficiency(self):
        self.assertEqual(generate_tempo(61, 12), 'Incorrect efficiency')

    def test_efficiency_str(self):
        self.assertEqual(generate_tempo('30', 12), 'Incorrect efficiency')

    def test_type_str(self):
        self.assertEqual(generate_tempo(30, '12'), 'Incorrect type')

    def test_efficiency_float(self):
        self.assertEqual(generate_tempo(30.0, 12), 'Incorrect efficiency')

    def test_type_float(self):
        self.assertEqual(generate_tempo(30, 12.0), 'Incorrect type')


class AddingTemposTest(unittest.TestCase):

    def test_correct(self):
        self.assertEqual(adding_tempos(30),
                         {'easy': '7.74km/h', 'interval': '10.14km/h', 'marathon': '8.51km/h',
                          'repetition': '10.75km/h', 'threshold': '9.38km/h'})

    def test_incorrect(self):
        self.assertEqual(adding_tempos(61), 'Incorrect efficiency')
        self.assertEqual(adding_tempos(29), 'Incorrect efficiency')

    def test_str(self):
        self.assertEqual(adding_tempos('61'), 'Incorrect efficiency')
        self.assertEqual(adding_tempos('29'), 'Incorrect efficiency')
        self.assertEqual(adding_tempos('35'), 'Incorrect efficiency')

    def test_float(self):
        self.assertEqual(adding_tempos(61.0), 'Incorrect efficiency')
        self.assertEqual(adding_tempos(29.0), 'Incorrect efficiency')
        self.assertEqual(adding_tempos(35.0), 'Incorrect efficiency')


class GeneratorViewTest:
    pass
