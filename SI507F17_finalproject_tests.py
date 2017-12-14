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
    params = {'name': 'Mike Tyson',
              'real_name': 'Mike Tyson',
              'nickname': 'Kid Dynamite\nThe Baddest Man on the Planet\nIron Mike',
              'weight': 'Heavyweight',
              'height': '5 ft 10 in (178 cm)',
              'reach': '71 in (180 cm)',
              'country': {'id': 1},
              'born': 'June 30, 1966 (age 51)',
              'stance': 'Orthodox',
              'total_fights': '58',
              'wins': '50',
              'wins_by_ko': '44',
              'losses': '6',
              'no_contests': '2'}
    self.mike_tyson = Boxer(params)
    self.second_boxer = Boxer({'real_name': 'test'})

  def test_init(self):
    self.assertEqual(self.mike_tyson.boxer_id, 1)
    self.assertEqual(self.mike_tyson.real_name, 'Mike Tyson')
    self.assertEqual(self.mike_tyson.nickname, 'Kid Dynamite, The Baddest Man on the Planet, Iron Mike')
    self.assertEqual(self.mike_tyson.weight, 'Heavyweight')
    self.assertEqual(self.mike_tyson.height, 178)
    self.assertEqual(self.mike_tyson.reach, 180)
    self.assertEqual(self.mike_tyson.country_id, 1)
    self.assertEqual(self.mike_tyson.born, 'June 30, 1966 (age 51)')
    self.assertEqual(self.mike_tyson.stance, 'Orthodox')
    self.assertEqual(self.mike_tyson.total_fights, 58)
    self.assertEqual(self.mike_tyson.wins, 50)
    self.assertEqual(self.mike_tyson.wins_by_ko, 44)
    self.assertEqual(self.mike_tyson.losses, 6)
    self.assertEqual(self.mike_tyson.draws, 0)
    self.assertEqual(self.mike_tyson.no_contests, 2)

    self.assertEqual(self.second_boxer.boxer_id, 2)

  def test_repr(self):
    self.assertEqual(repr(self.mike_tyson), 'Mike Tyson')

  def test_contains(self):
    self.assertTrue('Mike' in self.mike_tyson)
    self.assertTrue('Tyson' in self.mike_tyson) 

  def test_set_recognitions(self):
    self.mike_tyson.set_recognitions('IBF, WBA and WBC')
    self.assertEqual(self.mike_tyson.recognitions, 'IBF, WBA and WBC')

  def test_set_reign_days(self):
    self.mike_tyson.set_reign_days(1415)
    self.assertEqual(self.mike_tyson.reign_days, 1415)

  def tearDown(self):
    Boxer.totalBoxers = 0

class Test_BoxerRecordsClass(unittest.TestCase):
  def setUp(self):
    params = {'name': 'Mike Tyson',
              'real_name': 'Mike Tyson',
              'nickname': 'Kid Dynamite\nThe Baddest Man on the Planet\nIron Mike',
              'weight': 'Heavyweight',
              'height': '5 ft 10 in (178 cm)',
              'reach': '71 in (180 cm)',
              'country': {'id': 1},
              'born': 'June 30, 1966 (age 51)',
              'stance': 'Orthodox',
              'total_fights': '58',
              'wins': '50',
              'wins_by_ko': '44',
              'losses': '6',
              'no_contests': '2'}
    self.mike_tyson = Boxer(params)
    self.mike_tyson_records = BoxingRecords(self.mike_tyson.boxer_id)

  def test_init(self):
    self.assertEqual(self.mike_tyson_records.boxer_id, 1)
    self.assertTrue(self.mike_tyson_records.have_record)

  def test_repr(self):
    self.assertEqual(repr(self.mike_tyson_records), 'Boxing records for boxer ID: 1')

  def test_adding_records(self):
    self.mike_tyson_records.set_headers(['no.', 'result', 'record', 'opponent', 'type', 'round, time', 'date', 'location', 'notes'])
    self.assertEqual(len(self.mike_tyson_records.headers), 9)
    values = [1, 'Win', '1-0', 'Hector Mercedes', 'TKO', '1 (4), 1:47', 'Mar 6, 1985', 'Plaza Convention Center, Albany, New York, U.S.', 'Professional debut']
    temp = {}
    for i in range(len(values)):
      temp[self.mike_tyson_records.headers[i]] = values[i]
    self.mike_tyson_records.add_record(temp)    
    self.assertEqual(len(self.mike_tyson_records.records), 1)

    self.assertEqual(self.mike_tyson_records.records[0]['no.'], 1)
    self.assertEqual(self.mike_tyson_records.records[0]['result'], 'Win')
    self.assertEqual(self.mike_tyson_records.records[0]['record'], '1-0')
    self.assertEqual(self.mike_tyson_records.records[0]['opponent'], 'Hector Mercedes')
    self.assertEqual(self.mike_tyson_records.records[0]['type'], 'TKO')
    self.assertEqual(self.mike_tyson_records.records[0]['round, time'], '1 (4), 1:47')
    self.assertEqual(self.mike_tyson_records.records[0]['date'], 'Mar 6, 1985')
    self.assertEqual(self.mike_tyson_records.records[0]['location'], 'Plaza Convention Center, Albany, New York, U.S.')
    self.assertEqual(self.mike_tyson_records.records[0]['notes'], 'Professional debut')

  def test_no_record(self):
    self.mike_tyson_records.no_record()
    self.assertFalse(self.mike_tyson_records.have_record)

  def tearDown(self):
    Boxer.totalBoxers = 0

if __name__ == "__main__":
  unittest.main(verbosity=2)
