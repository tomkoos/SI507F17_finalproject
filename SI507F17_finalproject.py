import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from caching_system import *
from BoxerClass import *
from BoxingRecordsClass import *
from database import *
from config import *

base_url = 'https://en.wikipedia.org'

def getSoup(url):
  global retrieve_from_cache

  if retrieve_from_cache:
    try:
      data = get_from_cache(url)
    except:
      print('Fail retrieveing data from cache')
      exit()
  else:    
    data = requests.get(url).text
    set_in_data_cache(url, data)
  return BeautifulSoup(data, 'html.parser')

attribute_to_class = {'Real name': 'real_name',
                      'Nickname(s)': 'nickname',
                      'Other names': 'nickname',
                      'Weight(s)': 'weight',
                      'Height': 'height',
                      'Reach': 'reach',
                      'Nationality': 'nationality',
                      'Born': 'born',
                      'Died': 'died',
                      'Stance': 'stance',
                      'Total fights': 'total_fights',
                      'Total': 'total_fights',
                      'Wins': 'wins',
                      'Wins by KO': 'wins_by_ko',
                      'Losses': 'losses',
                      'Draws': 'draws',
                      'No contests': 'no_contests'}

countries = {} 
list_boxers = [] #list of Boxer class objects
list_boxing_records = []

def get_country_codes(three_letters_country_codes):
  countrycode_url = 'https://countrycode.org'
  soup = getSoup(countrycode_url)
  countrycode_table = soup.find('tbody').find_all('tr')
  for tr in countrycode_table:
    data = tr.find_all('td')
    three_letters_country_codes[data[0].text.strip()] = re.search('/ ([A-Z]+)', data[2].text.strip()).group(1)

def get_all_info():
  global countries
  global list_boxers
  global list_boxing_records

  three_letters_country_codes = {}
  uniquenames = set()  
  country_index = 1   
  reign_days = {}
  title_recognition = {}
  name_to_id = {}

  # get countries' code first
  get_country_codes(three_letters_country_codes)

  list_url = 'https://en.wikipedia.org/wiki/List_of_heavyweight_boxing_champions'
  soup = getSoup(list_url)
  champions_table = soup.find('table', {"class":"wikitable"})
  rows = champions_table.find_all('tr')

  # iterate through each row of the table (skip the header)
  for row in rows[1:]:
    profile_data_dict = {}
    row_data = row.find_all('td')
    suffix = row_data[0].find('a')['href']
    name = re.sub(' \(boxer\)' , '', row_data[0].find('a')['title'])
    country = row_data[1].text.strip()
    recognition = re.findall(r"\bWBA\b|\bIBF\b|\bWBO\b|\bWBC\b|\bNBA\b|\bNYSAC\b|\bIBU\b|\bUniversal\b", row_data[2].text)
    title_recognition[name] = title_recognition.get(name, []) + recognition
    reign_began = datetime.strptime(row_data[3].text, '%B %d, %Y')
    if row_data[4].text == 'Present':
      reign_ended = datetime.now()
    else:
      reign_ended = datetime.strptime(row_data[4].text, '%B %d, %Y')
    reign_days[name] = reign_days.get(name, 0) + (reign_ended - reign_began).days
    
    # now get into each boxer's profile page
    if name in uniquenames:
      continue
    else:
      uniquenames.add(name)
    profile = getSoup(base_url + suffix)
    
    profile_data_dict['name'] = name    
    if not (country in countries):
      countries[country] = {'id': country_index, 'country_code': three_letters_country_codes[country]}
      country_index += 1
    profile_data_dict['country'] = countries[country]

    # get profile info for each boxer
    profile_card = profile.find('table', {'class': 'infobox vcard'})    
    # wiki page for Vitali Klitschko is a little bit different
    if row_data[0].text == 'Vitali Klitschko':
      profile_card = profile.find_all('table', {'class': 'infobox vcard'})[1]
    if not profile_card:
      profile_card = profile.find('table', {'class': 'infobox biography vcard'})
    profile_data = profile_card.find_all('tr')
    if profile_card.find('img'):
      profile_data_dict['pic_url'] = profile_card.find('img')['src']
    else:
      profile_data_dict['pic_url'] = None
    for item in profile_data:      
      th = item.find('th')
      td = item.find('td')
      if th:
        attribute = th.text
        if 'knockout' in attribute:
          attribute = 'Wins by KO'
        if attribute in attribute_to_class:
          attribute_name = attribute_to_class[attribute]
          if attribute_name in profile_data_dict:
            continue
          if attribute_name == 'born':
            profile_data_dict[attribute_name] = None
            bday = td.find('span', {'class': 'bday'})
            if bday:
               profile_data_dict[attribute_name] = bday.text
          elif attribute_name == 'died':
            profile_data_dict[attribute_name] = None
            dday = td.find('span', {'class': 'dday deathdate'})
            if dday:
              profile_data_dict[attribute_name] = dday.text
          else:
            profile_data_dict[attribute_name] = td.text.strip().replace(u'\xa0', u' ')
    list_boxers.append(Boxer(profile_data_dict))
    name_to_id[name] = Boxer.totalBoxers

    # get boxing records for each boxer    
    boxing_record = BoxingRecords(Boxer.totalBoxers)
    if name in ('Marvin Hart', 'Tommy Burns', 'Jess Willard'):
      boxing_record.no_record()
      list_boxing_records.append(boxing_record)
      continue

    boxing_records_data = profile.find('table', {'class': 'wikitable', 'style': 'text-align:center; font-size:95%'})
    if name in ('Ken Norton', 'Oliver McCall'):
      boxing_records_data = profile.find_all('table', {'class': 'wikitable'})[1]
    if not boxing_records_data:
      boxing_records_data = profile.find('table', {'class': 'wikitable'})
      if not boxing_records_data:
        boxing_records_data = profile.find('table', {'class': 'wikitable succession-box'})
    header_index = 0
    header_row = boxing_records_data.find('tr')
    if len(header_row.find_all('td')) == 1:
      header_index = 1
      header_row = boxing_records_data.find_all('tr')[1]
    headers = header_row.find_all('th')
    # print(header_row)
    if not headers:
      headers = header_row.find_all('td')
    list_headers = []
    for header in headers:
      list_headers.append(re.search('([A-Za-z]+)', header.text).group(1).lower())
    boxing_record.set_headers(list_headers)
    rows = boxing_records_data.find_all('tr')
    # print(rows)
    for row in rows[header_index+1:]:
      temp_record = {}
      values = row.find_all('td')
      for i in range(len(values)):
        temp_record[list_headers[i]] = values[i].text
      boxing_record.add_record(temp_record)
    list_boxing_records.append(boxing_record)

  # set title recognitions and reign days
  for k in title_recognition:
    title_recognition[k] = ', '.join(set(title_recognition[k]))
  for boxer in list_boxers:
    boxer.set_recognitions(title_recognition[boxer.get_name()])
    boxer.set_reign_days(reign_days[boxer.get_name()])

  create_cache_name_to_id(name_to_id)

  # success message
  if retrieve_from_cache:
    print('Success retrieveing data from cache')
  else:
    print('Success retrieveing data from internet')

if __name__ == '__main__':
  get_all_info()
  conn, cursor = get_connection_and_cursor()
  setup_database()
  create_table_country(countries)
  create_table_list_of_champs(list_boxers)
  create_table_boxing_records(list_boxing_records)
