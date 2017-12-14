import unittest
import json
from BoxerClass import *
from BoxingRecordsClass import *

class Test_Caching(unittest.TestCase):
  def setUp(self):
    self.cache_file = open("cache_contents.json", encoding='utf-8-sig')

  def test_cache_file(self):
    read = self.cache_file.read()
    self.assertTrue(read)
    self.assertIsInstance(read, str)
    cache_diction = json.loads(read)
    self.assertIsInstance(cache_diction, dict)

  def tearDown(self):
    self.cache_file.close()

class Test_BoxerClass(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    pass

  def tearDown(self):
    pass

class Test_BoxerRecordsClass(unittest.TestCase):
  def setUp(self):
    pass
  def test_csv_files(self):
    pass
  def tearDown(self):
    pass

if __name__ == "__main__":
  unittest.main(verbosity=2)
