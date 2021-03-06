import unittest


class Yummy:
    """
    This is the Yummiest class of all hypothetical foods in the space
    of all the vectors imagination can come up with
    """

    def __init__(self):
        self.__all_words = ['hot', 'chocolate', 'milk']
        self.__food_documents = [[0, 1, 0],  # 'chocolate'
                                 [1, 0, 1]]  # 'hot milk'

    @property
    def food_documents(self):
        return self.__food_documents[::]  # return a copy of the list

    @property
    def all_words(self):
        return self.__all_words[::]  # return a copy of the list

    def create_new_food_document(self, document):
        """
        Adds vectorized food document to self.__food_documents.
        :param document: str of 1 or more words
        :return: list  # added for unit test
        # >>> y = Yummy()
        # >>> y.create_new_food_document('pumpkin')
        # ['pumpkin']
        """
        if not self._beautiful_string(document):
            return False
        if self.query(document) == document:
            # Document already exists
            return False
        document = self._document_string_to_list(document)
        new_words = self._is_in_all_words(document)
        self.add_to_all_words(new_words)
        self.__food_documents.append(self._vectorize(document))
        return self.food_documents[-1]  # only added this line for unit tests

    @staticmethod
    def _beautiful_string(ugly):
        """
        Checks if parameter is a string and if it contains only alphabetic characters,
        otherwise returns False
        :param ugly: str
        :return: bool
        >>> y = Yummy()
        >>> y._beautiful_string('pumpkin')
        True

        >>> y = Yummy()
        >>> y._beautiful_string('pumpkin4L!FE')
        False

        >>> y = Yummy()
        >>> y._beautiful_string(['pumpkin4L!FE'])
        False
        """
        if not isinstance(ugly, str) or not ugly:
            return False
        return all(i.isalpha() or i.isspace() for i in ugly)

    def add_to_all_words(self, word):
        """
        Adds word to self.__all_words
        :param word: list of strings
        :return: None

        """
        self.__all_words += word

    @staticmethod
    def _document_string_to_list(string_document):
        """
        Split string document into list of strings.
        :param string_document: str of 1 or more words
        :return: list
        >>> y = Yummy()
        >>> y._document_string_to_list('strawberry milkshake')
        ['strawberry', 'milkshake']

        """
        string_document = ' '.join(string_document.split())
        return string_document.lower().split(' ')

    def _is_in_all_words(self, word):
        """
        Checks if word is in the list of all words. Returns words from the list
        that are not yet in self._all_words
        :param word: list of 1 or more words
        :return: list
        """
        temp_words = []
        for i in word:
            if i not in self.__all_words:
                temp_words.append(i)
        return temp_words

    def _vectorize(self, document):
        """
        Transform list into binary vector,
        E.x. ['hot', 'chocolate'] -> [1, 1, 0]
        :param document: list
        :return: list
        >>> y = Yummy()
        >>> y._vectorize(['hot', 'chocolate'])
        [1, 1, 0]
        """
        document_vector = [0] * len(self.__all_words)
        for i in document:
            try:
                index = self.__all_words.index(i)
                document_vector[index] = 1
            except ValueError as e:
                return e
        return document_vector

    def query(self, Q):
        """
        Compute the scalar product between the query vector and all the document vectors.
        Find and return highest matching result
        :param Q: str
        :return: str
        """
        d = {}
        if not self._beautiful_string(Q):
            # Your query looks ugly
            return False
        Q = self._document_string_to_list(Q)

        # ignore words that are not available in self.__all_words
        Q = [item for item in Q if item in self.__all_words]
        Q = self._vectorize(Q)
        for i in self.__food_documents:
            vector_sum = sum((k * j for k, j in zip(Q, i)))
            d[self.__food_documents.index(i)] = vector_sum

        # return N best matches
        indices = [k for k, v in d.items() if ((v >= 1) and (max(d.values()) == v))]
        if not indices:
            # No matches found
            return None
        return self._prettify(self._match(indices))

    def _prettify(self, almost_pretty):
        """
        Turn beauty out of generator beast...hopefully
        :param almost_pretty: generator
        :return: str
        """
        s = ''
        for i in almost_pretty:
            if s:
                s += ', '
            s += ' '.join(i)
        return s

    def _match(self, indices):
        """
        Match and retrieve indices from food document
        :param indices: list
        :return: None
        """
        for i in indices:
            yield [self.__all_words[k] for k in range(len(self.__food_documents[i])) if
                   self.__food_documents[i][k] == 1]


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
        self.assertFalse(self.yum.create_new_food_document('hot milk'), msg='List already exists')

    def test_vectorize(self):
        self.assertListEqual(self.yum._vectorize(['hot']), [1, 0, 0])

    def test_query(self):
        self.assertMultiLineEqual(self.yum.query('hot chocolate'), 'chocolate, hot milk', )
        self.assertMultiLineEqual(self.yum.query('milk'), 'hot milk')
        self.assertIsNone(self.yum.query('banana'))
        self.assertRaises(TypeError, self.yum.query(['poisoned apple']))

    def test_beautiful_string(self):
        self.assertTrue(self.yum._beautiful_string('hot      cheesecake'), 'hot cheesecake')
        self.assertTrue(self.yum._beautiful_string('hot cake'), 'hot cheesecake')
        self.assertFalse(self.yum._beautiful_string('cr@zY b@nanas'))
        self.assertFalse(self.yum._beautiful_string(''))
        self.assertFalse(self.yum._beautiful_string(['shaved pineapple']))


unittest.main()
