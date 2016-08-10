from .solution import *
class YummyTests(unittest.TestCase):
    def setUp(self):
        self.yum = Yummy()

    def test_document_string_to_list(self):
        self.assertTrue(self.yum._document_string_to_list('hot nickles'), ['hot', 'nickles'])
        self.assertTrue(self.yum._document_string_to_list('slartibartfast'), ['slartibartfast'])

    def test_is_in_all_words(self):
        self.assertListEqual(self.yum._is_in_all_words(['hot', 'chocolate', 'milk']), [])
        self.assertListEqual(self.yum._is_in_all_words(['hot', 'chocolate']), [])
        self.assertListEqual(self.yum._is_in_all_words(['hot']), [])
        self.assertListEqual(self.yum._is_in_all_words([]), [])
        self.assertListEqual(self.yum._is_in_all_words(['rotten', 'pumpkin']), ['rotten', 'pumpkin'])

    def test_create_new_food_document(self):
        self.assertFalse(self.yum.create_new_food_document(''))
        self.assertListEqual(self.yum.create_new_food_document('chocolate milk'), [0, 1, 1])
        self.assertListEqual(self.yum.create_new_food_document('hot milk'), [1, 0, 1])

    def test_vectorize(self):
        self.assertListEqual(self.yum._vectorize(['hot']), [1, 0, 0])

    def test_query(self):
        self.assertMultiLineEqual(self.yum.query('hot chocolate'), 'chocolate, hot milk, ', )
        self.assertMultiLineEqual(self.yum.query('milk'), 'hot milk, ')
        self.assertIsNone(self.yum.query('banana'))
        self.assertRaises(TypeError, self.yum.query(['poisoned apple']))

    def test_beautiful_string(self):
        self.assertTrue(self.yum._beautiful_string('hot      cheesecake'), 'hot cheesecake')
        self.assertTrue(self.yum._beautiful_string('hot cake'), 'hot cheesecake')
        self.assertFalse(self.yum._beautiful_string('cr@zY b@nanas'))
        self.assertFalse(self.yum._beautiful_string(''))
        self.assertFalse(self.yum._beautiful_string(['shaved pineapple']))


unittest.main()
