import unittest

# ./manage.py test calc
# Create your tests here.
from django.test import Client

from calc.views import generate_result, adding_result, generate_tempo, adding_tempos


class GenerateResultTest(unittest.TestCase):
    """
    TestCase for GenerateResultTest
    """

    def test_correct_3(self):
        """
        test correct output for 3-5km run and 30 efficiency
        """
        self.assertEqual(generate_result(30, 1), '17min 56sec ')

    def test_correct_5(self):
        """
        test correct output for 5-10km run and 30 efficiency
        """
        self.assertEqual(generate_result(30, 2), '30min 40sec ')

    def test_correct_10(self):
        """
        test correct output for 10-21.095km run and 30 efficiency
        """
        self.assertEqual(generate_result(30, 3), '1h 3min 46sec ')

    def test_correct_half(self):
        """
        test correct output for 20.095-42.195 km run and 30 efficiency
        """
        self.assertEqual(generate_result(30, 4), '2h 21min 4sec ')

    def test_correct_marathon(self):
        """
        test correct output for 42.195 km+ run and 30 efficiency
        """
        self.assertEqual(generate_result(30, 5), '4h 49min 17sec ')

    def test_max_marathon(self):
        """
        test correct output for 42.195 km+ run and 60 (max) efficiency
        """
        self.assertEqual(generate_result(60, 5), '2h 43min 25sec ')

    def test_incorrect_efficiency(self):
        """
        test incorrect efficiency (61)
        """
        self.assertEqual(generate_result(61, 3), 'Incorrect efficiency')

    def test_incorrect_distance(self):
        """
        test incorrect distance (no index 6 in TABLE)
        """
        self.assertEqual(generate_result(60, 6), 'Incorrect distance')

    def test_distance_str(self):
        """
        test incorrect distance (string)
        """
        self.assertEqual(generate_result(60, '5'), 'Incorrect distance')

    def test_efficiency_str(self):
        """
        test incorrect efficiency (string)
        """
        self.assertEqual(generate_result('60', 5), 'Incorrect efficiency')

    def test_distance_float(self):
        """
        test incorrect distance (float)
        """
        self.assertEqual(generate_result(60, 5.0), 'Incorrect distance')

    def test_efficiency_float(self):
        """
        test incorrect efficiency (float)
        """
        self.assertEqual(generate_result(60.0, 5), 'Incorrect efficiency')


class AddingResultTest(unittest.TestCase):
    """
    TestCase for AddingResultTest
    """

    def test_correct(self):
        """
        test correct output for efficiency = 30
        """
        self.assertEqual(adding_result(30),
                         {'marathon': '4h 49min 17sec ', 'half': '2h 21min 4sec ', '10k': '1h 3min 46sec ',
                          '5k': '30min 40sec ', '3k': '17min 56sec '})

    def test_incorrect(self):
        """
        test incorrect efficiency = 29 and efficiency = 61
        """
        self.assertEqual(adding_result(61), 'Incorrect efficiency')
        self.assertEqual(adding_result(29), 'Incorrect efficiency')

    def test_str(self):
        """
        test incorrect efficiency (string)
        """
        self.assertEqual(adding_result('61'), 'Incorrect efficiency')
        self.assertEqual(adding_result('29'), 'Incorrect efficiency')
        self.assertEqual(adding_result('35'), 'Incorrect efficiency')

    def test_float(self):
        """
        test incorrect efficiency (float)
        """
        self.assertEqual(adding_result(61.0), 'Incorrect efficiency')
        self.assertEqual(adding_result(29.0), 'Incorrect efficiency')
        self.assertEqual(adding_result(35.0), 'Incorrect efficiency')


class GenerateTemposTest(unittest.TestCase):
    """
    TestCase for GenerateTemposTest
    """

    def test_correct_easy(self):
        """
        test correct output for efficiency = 30 and trening type = easy
        """
        self.assertEqual(generate_tempo(30, 8), '7.74km/h')

    def test_correct_marathon(self):
        """
        test correct output for efficiency = 30 and trening type = marathon
        """
        self.assertEqual(generate_tempo(30, 9), '8.51km/h')

    def test_correct_threshold(self):
        """
        test correct output for efficiency = 30 and trening type = threshold
        """
        self.assertEqual(generate_tempo(30, 10), '9.38km/h')

    def test_correct_interval(self):
        """
        test correct output for efficiency = 30 and trening type = interval
        """
        self.assertEqual(generate_tempo(30, 11), '10.14km/h')

    def test_correct_repetition(self):
        """
        test correct output for efficiency = 30 and trening type = repetition
        """
        self.assertEqual(generate_tempo(30, 12), '10.75km/h')

    def test_incorrect_type(self):
        """
        test incorrect type((no index 13 in TABLE)
        """
        self.assertEqual(generate_tempo(30, 13), 'Incorrect type')

    def test_incorrect_efficiency(self):
        """
        test incorrect efficiency (61)
        """
        self.assertEqual(generate_tempo(61, 12), 'Incorrect efficiency')

    def test_efficiency_str(self):
        """
        test incorrect efficiency (string)
        """
        self.assertEqual(generate_tempo('30', 12), 'Incorrect efficiency')

    def test_type_str(self):
        """
        test incorrect type (string)
        """
        self.assertEqual(generate_tempo(30, '12'), 'Incorrect type')

    def test_efficiency_float(self):
        """
        test incorrect efficiency (float)
        """
        self.assertEqual(generate_tempo(30.0, 12), 'Incorrect efficiency')

    def test_type_float(self):
        """
        test incorrect type (float)
        """
        self.assertEqual(generate_tempo(30, 12.0), 'Incorrect type')


class AddingTemposTest(unittest.TestCase):
    """
    TestCase for AddingTemposTest
    """

    def test_correct(self):
        """
        test correct output efficiency = 30
        """
        self.assertEqual(adding_tempos(30),
                         {'easy': '7.74km/h', 'interval': '10.14km/h', 'marathon': '8.51km/h',
                          'repetition': '10.75km/h', 'threshold': '9.38km/h'})

    def test_incorrect(self):
        """
        test incorrect efficiency (29, 61)
        """
        self.assertEqual(adding_tempos(61), 'Incorrect efficiency')
        self.assertEqual(adding_tempos(29), 'Incorrect efficiency')

    def test_str(self):
        """
        test incorrect efficiency (string)
        """
        self.assertEqual(adding_tempos('61'), 'Incorrect efficiency')
        self.assertEqual(adding_tempos('29'), 'Incorrect efficiency')
        self.assertEqual(adding_tempos('35'), 'Incorrect efficiency')

    def test_float(self):
        """
        test incorrect efficiency (float)
        """
        self.assertEqual(adding_tempos(61.0), 'Incorrect efficiency')
        self.assertEqual(adding_tempos(29.0), 'Incorrect efficiency')
        self.assertEqual(adding_tempos(35.0), 'Incorrect efficiency')


class GeneratorViewTest(unittest.TestCase):
    """
    TestCase for GeneratorViewTest
    """

    def setUp(self):
        self.client = Client()

    def test_correct_get(self):
        """
        test correct status code for get method
        """
        response = self.client.get('/calculator/')
        self.assertEquals(response.status_code, 200)

    def test_correct_post(self):
        """
        test correct response context for post method and input 1 hour, 1 minute 1 second and 13 distance
        """
        response = self.client.post('/calculator/', {'hours': '1', 'minutes': '1', 'seconds': '1', 'distance': '13'})

        self.assertEqual(response.context['efficiency'], 43)
        self.assertEqual(response.context['form_value'],
                         {'hours': '1', 'minutes': '1', 'seconds': '1', 'distance_total': '13'})
        self.assertEqual(response.context['results'],
                         {'marathon': '3h 36min 28sec ', 'half': '1h 44min 20sec ', '10k': '47min 4sec ',
                          '5k': '22min 41sec ', '3k': '13min 11sec '})
        self.assertEqual(response.context['tempos'],
                         {'easy': '10.11km/h', 'interval': '13.53km/h', 'marathon': '11.65km/h',
                          'repetition': '14.69km/h', 'threshold': '12.46km/h'})

    def test_correct_empty_hours_post(self):
        """
        test correct response context for post method and input 0 hour, 61 minute 1 second and 13 distance
        """
        response = self.client.post('/calculator/', {'hours': '0', 'minutes': '61', 'seconds': '1', 'distance': '13'})

        self.assertEqual(response.context['efficiency'], 43)
        self.assertEqual(response.context['form_value'],
                         {'hours': '0', 'minutes': '61', 'seconds': '1', 'distance_total': '13'})
        self.assertEqual(response.context['results'],
                         {'marathon': '3h 36min 28sec ', 'half': '1h 44min 20sec ', '10k': '47min 4sec ',
                          '5k': '22min 41sec ', '3k': '13min 11sec '})
        self.assertEqual(response.context['tempos'],
                         {'easy': '10.11km/h', 'interval': '13.53km/h', 'marathon': '11.65km/h',
                          'repetition': '14.69km/h', 'threshold': '12.46km/h'})

    def test_correct_empty_minutes_post(self):
        """
        test correct response context for post method and input 1 hour, 0 minute 61 second and 13 distance
        """
        response = self.client.post('/calculator/', {'hours': '1', 'minutes': '0', 'seconds': '61', 'distance': '13'})

        self.assertEqual(response.context['efficiency'], 43)
        self.assertEqual(response.context['form_value'],
                         {'hours': '1', 'minutes': '0', 'seconds': '61', 'distance_total': '13'})
        self.assertEqual(response.context['results'],
                         {'marathon': '3h 36min 28sec ', 'half': '1h 44min 20sec ', '10k': '47min 4sec ',
                          '5k': '22min 41sec ', '3k': '13min 11sec '})
        self.assertEqual(response.context['tempos'],
                         {'easy': '10.11km/h', 'interval': '13.53km/h', 'marathon': '11.65km/h',
                          'repetition': '14.69km/h', 'threshold': '12.46km/h'})

    def test_correct_empty_seconds_post(self):
        """
        test correct response context for post method and input 1 hour, 1 minute 0 second and 13 distance
        """
        response = self.client.post('/calculator/', {'hours': '1', 'minutes': '1', 'seconds': '0', 'distance': '13'})

        self.assertEqual(response.context['efficiency'], 43)
        self.assertEqual(response.context['form_value'],
                         {'hours': '1', 'minutes': '1', 'seconds': '0', 'distance_total': '13'})
        self.assertEqual(response.context['results'],
                         {'marathon': '3h 36min 28sec ', 'half': '1h 44min 20sec ', '10k': '47min 4sec ',
                          '5k': '22min 41sec ', '3k': '13min 11sec '})
        self.assertEqual(response.context['tempos'],
                         {'easy': '10.11km/h', 'interval': '13.53km/h', 'marathon': '11.65km/h',
                          'repetition': '14.69km/h', 'threshold': '12.46km/h'})

    def test_negative_time_post(self):
        """
        test response context for negative number in time input
        """
        response = self.client.post('/calculator/', {'hours': '-1', 'minutes': '1', 'seconds': '1', 'distance': '13'})
        self.assertEqual(response.context['text'], 'No data can be a negative number')

        response = self.client.post('/calculator/', {'hours': '1', 'minutes': '-1', 'seconds': '1', 'distance': '13'})
        self.assertEqual(response.context['text'], 'No data can be a negative number')

        response = self.client.post('/calculator/', {'hours': '1', 'minutes': '1', 'seconds': '-1', 'distance': '13'})
        self.assertEqual(response.context['text'], 'No data can be a negative number')

    def test_negative_distance_post(self):
        """
        test response context for negative number in distance input
        """
        response = self.client.post('/calculator/', {'hours': '1', 'minutes': '1', 'seconds': '1', 'distance': '-13'})
        self.assertEqual(response.context['text'], 'No data can be a negative number')

    def test_empty_distance_post(self):
        """
        test response context for empty string in distance input
        """
        response = self.client.post('/calculator/', {'hours': '1', 'minutes': '1', 'seconds': '1', 'distance': ''})
        self.assertEqual(response.context['text'], 'Insert all data to the form')

    def test_distance_zero_post(self):
        """
        test response context for 0 in distance input
        """
        response = self.client.post('/calculator/', {'hours': '1', 'minutes': '0', 'seconds': '0', 'distance': '0'})
        self.assertEqual(response.context['text'], 'Insert all data to the form')

    def test_time_zero_post(self):
        """
        test response context for 0 in time input
        """
        response = self.client.post('/calculator/', {'hours': '0', 'minutes': '0', 'seconds': '0', 'distance': '13'})
        self.assertEqual(response.context['text'], 'Insert all data to the form')

    def test_empty_time_post(self):
        """
        test response context for empty string in time input
        """
        response = self.client.post('/calculator/', {'hours': '', 'minutes': '', 'seconds': '', 'distance': '13'})
        self.assertEqual(response.context['text'], 'Insert all data to the form')

    def test_str_time_post(self):
        """
        test response context for string in time input
        """
        response = self.client.post('/calculator/', {'hours': 'a', 'minutes': '1', 'seconds': '1', 'distance': '13'})
        self.assertEqual(response.context['text'], 'Insert all data to the form')

    def test_str_distance_post(self):
        """
        test response context for string in distance input
        """
        response = self.client.post('/calculator/', {'hours': 'a', 'minutes': '1', 'seconds': '1', 'distance': 'a'})
        self.assertEqual(response.context['text'], 'Insert all data to the form')
