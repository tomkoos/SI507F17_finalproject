from plotly.offline import plot
from database import *

def plot_choropleth():
  conn, cursor = get_connection_and_cursor()
  cursor.execute("""select country.country_code, country.name, count(championlist.boxer_id) as number_of_champs
            from country inner join championlist on country.country_id = championlist.country_id
            group by country.country_id""")
  result = cursor.fetchall()

  data = [ dict(
      type = 'choropleth',
      locations = [item['country_code'] for item in result],
      z = [item['number_of_champs'] for item in result],
      text = [item['name'] for item in result],
      showscale = False,
      colorscale = [[0,"#e5f5ff"],[0.1,"#006dff"], [1,"#0061e0"]],
      autocolorscale = False,
      marker = dict(
        line = dict (
          color = 'rgb(178, 178, 178)',
          width = 0.5
        ) ),      
      colorbar = dict(        
        autotick = False,
        title = 'Number of Champs'),
      ) ]

  layout = dict(
    title = '<b>Map of 83 World Heavyweight Boxing Champions</b>',
    height = 500,
    width = 800,
    margin=dict( l=0, r=0, b=0 ),  
    geo = dict(
      landcolor='rgb(239, 239, 239)',
      countrywidth=1,
      showland = True,
      showframe = False,
      showcoastlines = False,
      projection = dict(
        type = 'Mercator'
      )    
    )
  )

  fig = dict(data=data, layout=layout)
  return plot(fig, validate=False, include_plotlyjs=False, output_type='div' )
