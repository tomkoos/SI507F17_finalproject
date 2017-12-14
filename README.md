# SI 507 F17 - Final Project
## World Heavyweight Boxing Champions
The purpose of this project is to create database for heavyweight boxing champions of the worlds since the introduction of the Marquess of Queensberry rules in about 1884. In brief, I will utilize __BeautifulSoup__ to gather the data, and then store them into Postgres databases using SQL with Python. The visualization will be presented using html pages created by __Flask__ and __Plotly__.

The expected output is the Postgres database that consists of:
* 1 table for a list of world heavyweight boxing champions 
* 1 table for a list of countries
* 83 tables for boxing records for each of the world heavyweight boxing champion (However, some of them will be blank because of lack of data)


## How to run
The project expect Python 3 to run. Make sure Python 3 is installed in the system.  
0. Open Terminal (OSX or Unix) or Command Prompt (Windows). Change directory to the directory of the project.
1. Install all the required packages by running ```pip install -r requirements.txt```
2. Create a Postgres database
3. Edit __config.py__ by including the database name and user/password required to connect to the database. There's also an option whether you want to retrieve fresh data from the internet or retrieve stored data from the cache file. For example:
```
db_name = 'databasename_for_this_project'
db_user = 'myusername'
db_password = 'mypassword'
retrieve_from_cache = True
```
4. Run ```python SI507F17_finalproject.py``` to get all the data and to create database tables (it will take few minutes)
5. Run ```python app.py``` to start an internal web server
6. Go to __localhost:5000__ on web browser to access the Home page

## Additional details on the code
### SI507F17_finalproject.py
* When __SI507F17_finalproject.py__ runs, __get_all_info()__ will be called first and
1. Get countries' code (will be used in creating an interactive world map)
2. Connects to wikipedia server (or read cache_contents.json) and parsed the html response into beautifulsoup object. Then, iterate through the table of list of all boxers one by one to get the name of the boxer. While doing that, the program also visit and retrieve profile data from wiki profile page for each boxer. The obtained profile data will be used to create Boxer class objects and those objects will be stored temporarily in a list. During the retrieving process, the program will also create a json file call name_to_id to stored a mapping between boxer name and his boxer id.
3. If the process complete succesfully, the program will print out a message, either "Success retrieveing data from cache" or "Success retrieveing data from internet".
* __get_connection_and_cursor()__ will be called next to get the database connector and cursor to the database with a name specified in __config.py__. If the process complete successfully, the program will print out "Success connecting to database"
* Next, connect to the database and setup ChampionList and Country tables. __setup_database()__ is responsible for this task. If the process complete successfully, the program will print out "Setup database complete"
* __create_table_country(countries)__ : inserting data into country table. If the process complete successfully, the program will print out "Success inserting data into Country table"
* __create_table_list_of_champs__ : inserting data into ChampionList table. If the process complete successfully, the program will print out "Success inserting data into ChampionList table"
* Finally, __create_table_boxing_records__ will be called to setup boxing records tables for each boxer and inserting data into them. If the process complete successfully, the program will print out "Success creating table of boxing records for every boxers"