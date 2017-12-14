from flask import Flask, request, render_template, url_for
import requests
from database import *
from choropleth import *
from stats import *

app = Flask(__name__)


@app.route('/')
def index():
  conn, cursor = get_connection_and_cursor()
  cursor.execute("""SELECT name, nickname, recognitions,
                           total_fights, wins, wins_by_ko, losses, draws, no_contests
                       FROM ChampionList""")
  rows = cursor.fetchall()    
  return render_template('index.html', rows=rows)

@app.route('/map')
def map():  
  return render_template('map.html', plot_div=plot_choropleth())

@app.route('/stats')
def stats():
  conn, cursor = get_connection_and_cursor()
  stances = {}
  cursor.execute("""SELECT stance, COUNT(boxer_id)
                       FROM ChampionList
                         WHERE stance IS NOT NULL
                           GROUP BY stance""" )
  for item in cursor.fetchall():
    stances[item['stance']] = item['count']

  cursor.execute("""SELECT height_cm
                       FROM ChampionList
                         WHERE height_cm IS NOT NULL""" )
  heights = [item['height_cm'] for item in cursor.fetchall()] 

  cursor.execute("""SELECT reach_cm
                       FROM ChampionList
                         WHERE reach_cm IS NOT NULL""" )
  reachs = [item['reach_cm'] for item in cursor.fetchall()] 

  return render_template('stats.html',
                          plot_stance = plot_stance(stances),
                          plot_height = plot_height(heights),
                          plot_reach = plot_reach(reachs))

@app.route('/topfives')
def topfives():
  conn, cursor = get_connection_and_cursor()
  cursor.execute("""SELECT name, reign_days
                       FROM ChampionList
                         ORDER BY reign_days DESC
                           LIMIT 5""" )
  longestReign = cursor.fetchall()   

  cursor.execute("""SELECT name, total_fights
                       FROM ChampionList
                         ORDER BY total_fights DESC
                           LIMIT 5""" )
  mostFight = cursor.fetchall()

  cursor.execute("""SELECT name, round(100*wins_by_ko/wins::float) AS ko_percent
                       FROM ChampionList
                         ORDER BY ko_percent DESC
                           LIMIT 5""" )
  KOpercent = cursor.fetchall()      

  return render_template('topfives.html',
                          longestReign = longestReign,
                          mostFight = mostFight,
                          KOpercent = KOpercent)

@app.route('/table/list')
def list():
  conn, cursor = get_connection_and_cursor()
  cursor.execute("""SELECT *
                       FROM ChampionList""")
  rows = cursor.fetchall()    
  return render_template('list.html', rows=rows)

@app.route('/table/country')
def country():
  conn, cursor = get_connection_and_cursor()
  cursor.execute("""SELECT *
                       FROM Country""")
  rows = cursor.fetchall()    
  return render_template('country.html', rows=rows)

@app.route('/table/records/<name>')
def records(name):
  no_data = False
  conn, cursor = get_connection_and_cursor()
  with open('name_to_id.json', 'r', encoding='utf-8-sig') as cache_file:
        cache_json = cache_file.read()
        name_to_id = json.loads(cache_json)
  boxer_id = name_to_id[name]
  cursor.execute("SELECT pic_url FROM ChampionList WHERE boxer_id = {}".format(boxer_id))
  pic_url = cursor.fetchone()['pic_url']
  cursor.execute("SELECT * FROM boxer{}".format(boxer_id))
  rows = cursor.fetchall()
  if not rows:
    no_data = True
  return render_template('records.html', table_name=name, rows=rows, no_data=no_data, pic_url=pic_url)

@app.route('/search')
def search():
  search_term = request.args.get('q').lower()
  conn, cursor = get_connection_and_cursor()
  cursor.execute("""SELECT name
                       FROM ChampionList
                         WHERE lower(name) like '%{}%' """.format(search_term))
  rows = cursor.fetchall()    
  return render_template('search.html', rows=rows, num=len(rows))

if __name__ == '__main__':
    # auto reloads (mostly) new code and shows exception traceback in the browser
    app.run(use_reloader=True, debug=True)

