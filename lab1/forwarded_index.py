import re
import os


class Output:
    def __init__(self, document, frequency):
        self.path = document
        self.frequency = frequency

    def __repr__(self):
        return str(self.__dict__)


class Storage:
    def __init__(self):
        self.db = dict()

    def __repr__(self):
        return str(self.__dict__)

    def get(self, self_id):
        return self.db.get(self_id, None)

    def add(self, document):
        return self.db.update({document['id']: document})

    def remove(self, document):
        return self.db.pop(document['id'], None)


class InvertedIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

    def index_document(self, document):
        clean_text = re.sub(r'[^\w\s]', '', document['text']).lower()
        terms = clean_text.replace('\n', ' ').split(' ')

        files_array = []
        for file in os.listdir('data/'):
            file_dir = os.path.dirname(os.path.realpath('__file__'))
            file_name = os.path.join(file_dir, 'data/{file}'.format(file=file))
            files_array.append(file_name)

        result_dict = {}

        for file in files_array:
            docs = []
            for term in terms:
                if term not in docs:
                    docs.append(term)
                result_dict[file] = docs

        self.index.update(result_dict)
        self.db.add(document)
        return document

    def return_data(self):
        return self.index


def main():
    db = Storage()
    index = InvertedIndex(db)
    inc = 1
    for x in os.listdir('data/'):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, 'data/{file}'.format(file=x))
        file_handle = open(file_name)
        tst = file_handle.read()
        file_handle.close()

        doc = {'id': str(inc), 'text': tst}
        index.index_document(doc)
        inc += 1

    print('')
    print('Indexed successful: ' + str(index.return_data()))


main()
