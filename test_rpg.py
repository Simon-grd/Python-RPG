import unittest

class TestSearchPlayerStats(unittest.TestCase):
    def test_search_player_stats_utf8(self):
        with open('test_utf8.txt', 'w', encoding='utf-8') as f:
            f.write('Player stats in UTF-8')
        result = search_player_stats('test_utf8.txt')
        self.assertEqual(result, 'Expected output for UTF-8')

    def test_search_player_stats_latin1(self):
        with open('test_latin1.txt', 'w', encoding='latin-1') as f:
            f.write('Player stats in Latin-1')
        result = search_player_stats('test_latin1.txt')
        self.assertEqual(result, 'Expected output for Latin-1')

if __name__ == '__main__':
    unittest.main()