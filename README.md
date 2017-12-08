# SI 507 F17 - Final Project
## World Heavyweight Boxing Champions
The purpose of this project is to create database for heavyweight boxing champions of the worlds since the introduction of the Marquess of Queensberry rules in about 1884. In brief, I will utilize __BeautifulSoup__ to gather the data, and then store them into Postgres databases using SQL with Python. The visualization will be presented using html pages created by __Flask__ and __Plotly__.

The expected output is the Postgres database that consists of:
* 1 table for a list of world heavyweight boxing champions 
* 1 table for a list of countries
* 83 tables for boxing records for each of the world heavyweight boxing champion (However, some of them will be blank because of lack of data)


# How to run
1.  Create a Postgres database
2.  Edit __config.py__ by including the database name and user/password to connect to the database. There's also an option whether you want to retrieve fresh data from the internet or retrieve stored data from the cache file. For example:
```
db_name = 'databasename_for_this_project'
db_user = 'myusername'
db_password = 'mypassword'
retrieve_from_cache = True
```
3.  Run ```python main.py``` to get all the data and to create database tables (it will take few minutes)
4.  Run ```python app.py``` to start an internal web server
5.  Go to __localhost:5000__ on web browser to access the Home page