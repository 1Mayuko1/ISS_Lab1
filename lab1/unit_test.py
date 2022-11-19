import unittest

import forwarded_index
import inverted_index

valid_data = {'the': ['/Users/vladkondrackiy/UNIVER/ISS/ISS_Labs/lab1/data/doc1.txt',
                      '/Users/vladkondrackiy/UNIVER/ISS/ISS_Labs/lab1/data/doc3.txt',
                      '/Users/vladkondrackiy/UNIVER/ISS/ISS_Labs/lab1/data/doc2.txt']}


class TestToolset(unittest.TestCase):

    def test_forwarded_index(self):
        db = forwarded_index.Storage()
        index = forwarded_index.ForwardIndex(db)
        forwarded_index.index_file(index)

        search_term = 'the'
        expected = valid_data

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_cap_text_forward(self):
        db = forwarded_index.Storage()
        index = forwarded_index.ForwardIndex(db)
        forwarded_index.index_file(index)

        search_term = 'THE'
        expected = valid_data

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_spaced_text_forward(self):
        db = forwarded_index.Storage()
        index = forwarded_index.ForwardIndex(db)
        forwarded_index.index_file(index)

        search_term = ' the . '
        expected = valid_data

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_unfounded_text_forward(self):
        db = forwarded_index.Storage()
        index = forwarded_index.ForwardIndex(db)
        forwarded_index.index_file(index)

        search_term = 'text'
        expected = "\033[1;32;40m text not found \033[0;0m"

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_unfounded_cap_text_forward(self):
        db = forwarded_index.Storage()
        index = forwarded_index.ForwardIndex(db)
        forwarded_index.index_file(index)

        search_term = 'TEXT'
        expected = "\033[1;32;40m TEXT not found \033[0;0m"

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_unfounded_spaced_text_forward(self):
        db = forwarded_index.Storage()
        index = forwarded_index.ForwardIndex(db)
        forwarded_index.index_file(index)

        search_term = ' text . '
        expected = "\033[1;32;40m  text .  not found \033[0;0m"

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_inverted_index(self):
        db = inverted_index.Storage()
        index = inverted_index.InvertedIndex(db)
        forwarded_index.index_file(index)

        search_term = 'the'
        expected = valid_data

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_cap_text_invert(self):
        db = inverted_index.Storage()
        index = inverted_index.InvertedIndex(db)
        inverted_index.index_file(index)

        search_term = 'THE'
        expected = valid_data

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_spaced_text_invert(self):
        db = inverted_index.Storage()
        index = inverted_index.InvertedIndex(db)
        inverted_index.index_file(index)

        search_term = ' The . '
        expected = valid_data

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_unfounded_inverted_index(self):
        db = inverted_index.Storage()
        index = inverted_index.InvertedIndex(db)
        forwarded_index.index_file(index)

        search_term = 'text'
        expected = "\033[1;32;40m text not found \033[0;0m"

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_unfounded_cap_text_invert(self):
        db = inverted_index.Storage()
        index = inverted_index.InvertedIndex(db)
        forwarded_index.index_file(index)

        search_term = 'TEXT'
        expected = "\033[1;32;40m TEXT not found \033[0;0m"

        self.assertEqual(index.lookup_query(search_term), expected)

    def test_unfounded_spaced_text_invert(self):
        db = inverted_index.Storage()
        index = inverted_index.InvertedIndex(db)
        forwarded_index.index_file(index)

        search_term = ' text . '
        expected = "\033[1;32;40m  text .  not found \033[0;0m"

        self.assertEqual(index.lookup_query(search_term), expected)


if __name__ == '__main__':
    unittest.main()
