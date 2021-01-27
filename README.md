# TigerWalk

Web application that helps create Princeton friendships in the COVID era through shared walks.



### Program Structure

The structure below highlights the purpose of the files used within the dash app. 

    └── tigerwalk
        ├── static
        │   ├── logo.jpg
        ├── templates
        │   ├── css                          # Contains stylesheet.css
        │   ├── images                        # Instantiates app
        │   ├── activeWalkers.css                # Speaks to Model regarding input about the cell data
        │   ├── contactInfo.html             # Based on user input recieve from callback, sets up a certain map
        │   └── wireless_handler.py             # Speaks to Model regarding input about the wireless data
        │   
        ├── Model
        │   ├── init.py                         # Creates the engine to connect to the database
        │   ├── generate_cell_queries.py        # Generates cell queries for database and creates Pandas DataFrames of the queries
        │   └── generate_wireless_queries.py    # Generates wireless queries for database and creates Pandas DataFrames of the queries
        │ 
        ├── Views
        │   ├── display.py                      # Holds callback input and output, returns are displayed to user.
        │   ├── layout.py                       # Responsible for the layout 
        │   └── map.py                          # Creates a figure to display to user
        │ 
        └── tigerwalk.py                        # Runs the application

### Prerequisites

* Docker must be installed on the device in order to use this program. 

### Running the program:

After cloning the repository, use the terminal to run the web application.
You can view the application from your browser at localhost:5000.

### Using the program:
Follow these tips to get the most out of the program. 

 * To improve render performance, select parameters through the GUI to filter out unnecessary data.
 * When Scatterplot is selected:  
    1. Clicking an element in the legend will hide points matching that element. Click again to undo.
    2. Double clicking an element will hide all points that don't match the element. Double click again to undo.
    3. Use box or lasso select to dim all elements outside of selection area. Double click anywhere on map to undo (Note, a selection tool must be selected to undo).

## PostgreSQL Container
Hosts the database. 

### Volumes
 * mydata - Used to persist data across sessions.
 * sql/schema.sql - If mydata includes no data (typically only occurs when building the image), this volume populates the database using the schema.sql 

### Bring Your Own Data
There are two ways to use this program with a different database.
NOTE: The table you bring to the database needs to have the same columns as the initial table. It is suggested 
that you use the Column Adder project prior to importing new data to use with the Dash Plotter.
1. Connect to a database on your own device / local network.
    * NOTE, only works on Docker-for-Mac or Docker-for-Windows, see [here](https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach) for more info.
    * In dash/Model/init.py, change the database location to the desired location.
    ```
    db_location = 'postgres://postgres:postgres@172.17.0.1:5432/WigleDatabase' 
    --> 
    db_location = 'postgres://username:password@host.docker.internal:5432/database_name
    ```
    * To use maps other than Wireless Network Data, ensure a table exists in your database called cell_data.
    See "Cell Scraper" section of Data Scraper project to make and populate this table. 
    * Run the program from the terminal.
    ```
    docker-compose up
    ```

    
2. Create a CSV file of your data
    * Using psql, create a csv file from your table of wigle data. 
    ```
    \copy [Table/Query] to [Relative Path] csv header
    ```
    * In the mydata directory, replace wigleData167k.csv with your csv file. 
    * In the mydata directory, if "data" directory exists, delete it. 
    * To use maps other than Wireless Network Data, ensure a table exists in your database called cell_data.
    See "Cell Scraper" section of Data Scraper project to make and populate this table.
    * Run the program from the terminal.
    ```
    docker-compose up
    ```

## Built With
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - WSGI web application framework, used as foundation for Dash application.
* [Dash](https://plotly.com/dash/) - Runs on top of Flask to host application.
* [Plotly](https://plotly.com/python/) - Graphing library, used to create heatmaps.
* [SQLAlchemy](https://www.sqlalchemy.org/) - Python toolkit to make connection to PostgreSQL database.
* [Psycopg2](https://www.psycopg.org/) - Used to interact with the PostgreSQL database.
* [PostgreSQL](https://www.postgresql.org/) - Database used to store the wigle data.
* [Docker](https://www.docker.com/) - Used to containerize the Dash app and database.

## Authors

* **Theo Knoll** 

## Acknowledgments

* David Velez - Mentor on project
* Eric Hsiung - Manager on project
* CACI - Employer