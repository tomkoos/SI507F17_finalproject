from psycopg2 import sql
import psycopg2.extras
import sys
import json
from config import *

db_connection = None
db_cursor = None

def get_connection_and_cursor():
  global db_connection, db_cursor
  if not db_connection:
    try:
      db_connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
      print("Success connecting to database")
    except:
      print("Unable to connect to the database. Check server and credentials.")
      sys.exit(1)

  if not db_cursor:
    db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

  return db_connection, db_cursor

def setup_database():
  conn, cur = get_connection_and_cursor()

  cur.execute("DROP TABLE IF EXISTS ChampionList")
  cur.execute("DROP TABLE IF EXISTS Country")

  cur.execute("CREATE TABLE IF NOT EXISTS \
                 ChampionList(Boxer_id INT PRIMARY KEY, \
                              Name VARCHAR(128) UNIQUE, \
                              Real_Name VARCHAR(128), \
                              Nickname VARCHAR(128), \
                              Weight VARCHAR(128), \
                              Recognitions VARCHAR(32), \
                              Reign_days INT, \
                              Height_cm DECIMAL, \
                              Reach_cm INT, \
                              Country_ID INT, \
                              Born DATE, \
                              Died DATE, \
                              Stance VARCHAR(16), \
                              Total_fights INT, \
                              Wins INT, \
                              Wins_by_KO INT, \
                              Losses INT, \
                              Draws INT, \
                              No_contests INT, \
                              Pic_URL VARCHAR(256))")

  cur.execute("CREATE TABLE IF NOT EXISTS \
                 Country(Country_ID INT PRIMARY KEY, \
                         Name VARCHAR(32), \
                         Country_Code VARCHAR(3))")
  conn.commit()
  print('Setup database complete')

def insert(conn, cur, table, data_dict):  
  column_names = data_dict.keys()
  query = sql.SQL('INSERT INTO {0}({1}) VALUES({2}) ON CONFLICT DO NOTHING').format(
          sql.SQL(table),
          sql.SQL(', ').join(map(sql.Identifier, column_names)),
          sql.SQL(', ').join(map(sql.Placeholder, column_names))
      )
  query_string = query.as_string(conn)
  cur.execute(query_string, data_dict)

def create_table_country(diction):
  conn, cur = get_connection_and_cursor()
  for key in diction:
    insert(conn, cur, 'Country', {'country_id': diction[key]['id'],
                                  'name': key,
                                  'country_code': diction[key]['country_code']})
  conn.commit()
  print('Success inserting data into Country table')

def create_table_list_of_champs(list_boxers):
  conn, cur = get_connection_and_cursor()
  for boxer in list_boxers:
    insert(conn, cur, 'ChampionList',
           {'boxer_id': boxer.boxer_id,
            'name': boxer.name,
            'real_name': boxer.real_name,
            'nickname': boxer.nickname,
            'weight': boxer.weight,
            'recognitions': boxer.recognitions,
            'reign_days': boxer.reign_days,
            'height_cm': boxer.height,
            'reach_cm': boxer.reach,
            'country_id': boxer.country_id,
            'born': boxer.born,
            'died': boxer.died,
            'stance': boxer.stance,
            'total_fights': boxer.total_fights,
            'wins': boxer.wins,
            'wins_by_ko': boxer.wins_by_ko,
            'losses': boxer.losses,
            'draws': boxer.draws,
            'no_contests': boxer.no_contests,
            'pic_url': boxer.pic_url}
          )
  conn.commit()
  print('Success inserting data into ChampionList table')

def create_table_boxing_records(boxing_records):
  conn, cur = get_connection_and_cursor()
  for boxing_record in boxing_records:
    table_name = 'Boxer' + str(boxing_record.boxer_id)
    cur.execute("DROP TABLE IF EXISTS {}".format(table_name))
    setup = "CREATE TABLE IF NOT EXISTS {}".format(table_name)
    headers = ', '.join([header + " VARCHAR(512)" for header in boxing_record.headers])
    cur.execute("{} ({})".format(setup, headers))
    for record in boxing_record.records:
      insert(conn, cur, table_name, record)
  conn.commit()
  print('Success creating table of boxing records for every boxers')
