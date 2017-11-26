# SI 507 F17 - Final Project
## World Heavyweight Boxing Champions
The purpose of this project is to create database for heavyweight boxing champions of the worlds since the introduction of the Marquess of Queensberry rules in about 1884. In brief, I will utilize BeautifulSoup to gather the data, and then store them into Postgres databases using SQL with Python.

The expected output is the Postgres database that consists of:
* 1 table for a list of world heavyweight boxing champions 
* 1 table for a timeline of world heavyweight boxing champions (reign began and reign ended)
* 1 table for a list of countries
* tables for boxing records for each of the world heavyweight boxing champion

## Milestones
### Part 1: Setup the caching system
file: caching_system.py
- [ ] Try-except for opening the cache file
- [ ] Function to store new data in the cache file
- [ ] Function to get data from the cache file

### Part 2: Boxer class
file: BoxerClass.py
- [ ] __init__ : setup all attributes
- [ ] __repr__
- [ ] __contains__

### Part 3: Retrieve the data
file: SI507F17_finalproject.py  
url: https://en.wikipedia.org/wiki/List_of_heavyweight_boxing_champions
- [ ] Function to get HTML, and parse it to BeautifulSoup object
- [ ] Get the list of world heavyweight boxing champions from the internet
- [ ] Create Boxer object for each boxer from his wiki page

### Part 4: Storing data into Postgres database
files: database.py, config.py
- [ ] Create a database table for a list of world heavyweight boxing champions
- [ ] Create a database table for a timeline of world heavyweight boxing champions
- [ ] For each boxer, create a table that store the boxing records

### Part 5: Visualizations
file: SI507F17_finalproject.py
- [ ] Graph: Orthodox vs Southpaw (which stance is better for Heavyweight class)
- [ ] Graph: Stats for height, reach, and weight
- [ ] Graph: Nationalities

### Part 6: Test suite
file: SI507F17_finalproject_test.py
- [ ] Test Boxer Class
- [ ] Test database table for a list of world heavyweight boxing champions
- [ ] Test database table for a timeline of world heavyweight boxing champions
- [ ] Test database table for a list of countries
- [ ] Test database tables for boxing records

### Part 7: Miscellaneous
file: SI507F17_finalproject.py
- [ ] Create a virtual environment
- [ ] requirements.txt