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
        appearances_dict = dict()

        files_array = []

        for file in os.listdir('data/'):
            file_dir = os.path.dirname(os.path.realpath('__file__'))
            file_name = os.path.join(file_dir, 'data/{file}'.format(file=file))
            files_array.append(file_name)

        for term in terms:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Output(files_array[int(document['id']) - 1], term_frequency + 1)

        # Update index
        update_dict = {
            key: [appearance]
            if key not in self.index
            else self.index[key] + [appearance]
            for (key, appearance) in appearances_dict.items()
        }

        self.index.update(update_dict)
        # print(update_dict)  # TODO (todo for highlight msg) index all words

        # Add into the database
        self.db.add(document)
        return document

    def lookup_query(self, query):
        return {term: self.index[term] for term in query.split(' ') if term in self.index}


def index_file(index):
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


def main():
    db = Storage()
    index = InvertedIndex(db)
    index_file(index)

    search_term = input("Enter term(s) to search: ")
    result = index.lookup_query(search_term)
    if not bool(result):
        return print("\033[1;32;40m No text found \033[0;0m")
    else:
        print(result)


main()
