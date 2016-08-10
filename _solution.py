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
        :return:
        # >>> y = Yummy()
        # >>> y.create_new_food_document('pumpkin')
        # ['pumpkin']
        """
        if not self._beautiful_string(document):
            return False
        document = self._document_string_to_list(document)
        are_words = self._is_in_all_words(document)
        if are_words:
            inp = input('you have to add {} to list of all words before \n'
                        'creating a food document. Add now? [Y/N] -> '.format(are_words))
            if inp in 'yY':
                self.add_to_all_words(are_words)
            else:
                return False
        # document_vector = self._vectorize(document)
        self.__food_documents.append(self._vectorize(document))

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
        :return:

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
            print('Your query looks ugly')
            return False
        Q = self._document_string_to_list(Q)

        # ignore words that are not available in self.__all_words
        # exclude_words = self._is_in_all_words(Q)
        Q = [item for item in Q if item in self.__all_words]
        Q = self._vectorize(Q)
        for i in self.__food_documents:
            vector_sum = sum((k * j for k, j in zip(Q, i)))
            d[self.__food_documents.index(i)] = vector_sum

        # return N best matches
        indices = [k for k, v in d.items() if ((v >= 1) and (max(d.values()) == v))]
        if not indices:
            print('No matches found')
            return None
        s = ''
        documents = self._match(indices)
        for document in documents:
            s += ' '.join(document) + ', '

        return s

    def _match(self, indices):
        """
        Match and retrieve indices from food document
        :param indices: list
        :return:
        """
        for i in indices:
            yield [self.__all_words[k] for k in range(len(self.__food_documents[i])) if
                   self.__food_documents[i][k] == 1]
            # print(' '.join(m), end=', ')


class YummyTests(unittest.TestCase):
    # def test_create_new_document(self):
    #     y = Yummy()
    #     self.assertEqual(y.create_new_food_document('pumpkin'), ['pumpkin'])

    def setUp(self):
        self.yum = Yummy()

    def test_vectorize(self):
        y = Yummy()
        self.assertListEqual(self.yum._vectorize(['hot']), [1, 0, 0])

    def test_match(self):
        # y = Yummy()
        self.assertLogs(self.yum._match([1]), 'hot milk')
        self.assertLogs(self.yum._match([0]), 'chocolate')

    def test_query(self):
        y = Yummy()
        self.assertMultiLineEqual(self.yum.query('hot chocolate'), 'chocolate, hot milk, ',)
        self.assertMultiLineEqual(self.yum.query('milk'), 'hot milk, ')
        self.assertIsNone(self.yum.query('banana'))


# unittest.main()

y = Yummy()
print(y.create_new_food_document(''))