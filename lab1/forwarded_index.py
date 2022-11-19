import re
import os


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


def get_files_list():
    files_array = []

    for file in os.listdir('data/'):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, 'data/{file}'.format(file=file))
        files_array.append(file_name)

    return files_array


class ForwardIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

    def index_document(self, document):
        clean_text = re.sub(r'[^\w\s]', '', document['text']).lower()
        terms = clean_text.replace('\n', ' ').split(' ')
        appearances_dict = dict()

        docs = []
        for term in terms:
            if term not in docs:
                docs.append(term)
        appearances_dict[get_files_list()[int(document['id']) - 1]] = docs

        update_dict = {
            key: appearance
            if key not in self.index
            else self.index[key] + appearance
            for (key, appearance) in appearances_dict.items()
        }

        self.index.update(update_dict)
        # print(update_dict)  # TODO (todo for highlight msg) index words
        self.db.add(document)
        return document

    def lookup_query(self, query):
        clean_text = re.sub(r'[^\w\s]', '', query).lower().strip()
        res = []
        for term in self.index:
            for words in self.index[term]:
                if clean_text in words:
                    if term not in res:
                        res.append(term)

        if len(res) >= 1:
            return {clean_text: res}
        else:
            return "\033[1;32;40m {term} not found \033[0;0m".format(term=query)


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
    index = ForwardIndex(db)
    index_file(index)

    search_term = input("Enter term(s) to search: ")
    print(index.lookup_query(search_term.strip()))


# main()
