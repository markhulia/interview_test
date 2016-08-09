

class Yummy:
    def __init__(self):
        # self._all_words = ['milk', 'hot', 'chocolate', 'banana', 'tea', 'cheese', 'pizza',
        #                  'tuna', 'fish', 'pork', 'chicken', 'apple', 'orange', 'egg',
        #                  'steak', 'beef']

        self.__all_words = ['hot', 'chocolate', 'milk']
        self.__food_documents = [[0, 1, 0],  # 'chocolate'
                                [1, 0, 1]]  # 'hot milk'

    @property
    def food_documents(self):
        return self.__food_documents[::]  # return a copy of the list

    @property
    def all_words(self):
        return self.__all_words[::]  # return a copy of the list

    def add_word_to_all_words(self, food):
        """
        add new food to the list of all foods
        :param food: str
        :return: void
        """
        self.__all_words.append(food)

    @staticmethod
    def _document_string_to_list(string_document):
        # remove any redundant white spaces from the string
        # otherwise they will end up in the list
        string_document = ' '.join(string_document.split())
        return string_document.lower().split(' ')

    def create_new_food_document(self, _doc):
        """
        add vectorized food document to self._food_documents
        :param _doc: str
        :return: None
        """
        # split string into list of strings
        _doc = self._document_string_to_list(_doc)

        # check if words are already in the list of all words, if not,
        # add them
        self.add_to_all_words(_doc)

        # append vectors only after _doc is appended to all words
        self.__food_documents.append(self._vectorize(_doc))

    def add_to_all_words(self, word):
        temp_words = []
        for i in word:
            if not self.is_in_all_words(i):
                temp_words.append(i)

        # concatenate self._all_words and temp_words
        if temp_words:
            # noinspection PyShadowingNames
            inp = input('add {} to all words? [Y/N]\n'.format(temp_words))
            if inp in 'yY':
                self.__all_words += temp_words
            else:
                raise Exception('{} not in the list of all words'.format(temp_words))

    def is_in_all_words(self, word):
        """
        return True if every element of new document is already in the list of all words
        :param word: string
        :return: boolean
        """
        return word in self.__all_words

    def _vectorize(self, document):
        """
        Transform string into binary vector.
        For example: 'hot chocolate' == [1 1 0]
        :param document: str
        :return: list
        """
        document_vector = [0] * len(self.__all_words)
        for i in document:
            try:
                index = self.__all_words.index(i)
                document_vector[index] = 1
            except ValueError:
                return False
        return document_vector

    def query(self, Q):
        """
        Compute the scalar product between the query vector and all the document vectors
        :param Q: str
        :return: int
        """
        # dictionary holds the index of the food document and its score
        d = {}
        Q = self._document_string_to_list(Q)
        for i in Q:
            if not self.is_in_all_words(i):
                return '{} is not in word list'.format(i)

        Q = self._vectorize(Q)
        for i in self.__food_documents:
            s = sum((k * j for k, j in zip(Q, i)))
            d[self.__food_documents.index(i)] = s

        # returns N best matches
        indices = [k for k, v in d.items() if max(d.values()) == v]
        self.match(indices)

    def match(self, indices):
        for i in indices:
            m = [self.__all_words[k] for k in range(len(self.__food_documents[i])) if
                 self.__food_documents[i][k] == 1]
            print(' '.join(m), end=', ')


# self._all_words = ['hot', 'chocolate', 'milk']
# self._food_documents = [[0, 1, 0],  # 'chocolate'
#                         [1, 0, 1]]  # 'hot milk'
# y = Yummy()
# print('query: "chocolate  hot"')
# print('response:', end=' ')
# y.query('chocolate hot')
# print()

def _help():
    print('words - print list of all words\n'
          'docs - print list vectorized documents\n'
          'new - creates ne food document. Accepts string as an argument. e.x. "banana shake"\n'
          'help - print list of all commands\n'
          'hit Enter to exit')


if __name__ == '__main__':
    y = Yummy()
    print(y.query(' banana'))
    print()
    print('all words: ', y.all_words)

y = Yummy()
commands = {
    'words': y.all_words,
    'docs': y.food_documents,
    'new': y.create_new_food_document,
    'help': _help,
}

while False:
    inp = input('Enter command. Type "help" to list all commands\n')
    if inp == '':
        break
    elif inp == 'new':
        inp = input('Add document: (e.x. "banana milkshake")')
    print(commands[inp])
