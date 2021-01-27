# TigerWalk

TigerWalk is a web application that helps create Princeton
friendships in the COVID era through shared walks. 


### Program Structure

The structure below highlights the purpose of the files used within TigerWalk. 

    └── tigerwalk
        ├── templates                       # Contains the css and html files for the program's pages
        │  
        ├── CASClient.py                    # Enables CAS authentication
        │  
        └── tigerwalk.py                    # Runs the application, built using flask

### Running the program on your own:

After cloning the repository, use the terminal to run the web application.
 ```
    python tigerwalk.py
 ```
You can view the application from your browser at localhost:5000.

## Database
The database is powered by flask-sqlalchemy, making for a lightweight way to store user information.

## Built With
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - WSGI web application framework, used as foundation for TigerWalk application.
* [SQLAlchemy](https://www.sqlalchemy.org/) - Python toolkit to make connection to database.
* [CASClient](https://www.psycopg.org/) - Used to login to Princeton CAS.
* [Cloudinary](https://cloudinary.com/) - Stores photos in online drive.
* [Open Layers](https://openlayers.org/) - Enables use of the dynamic map.

## Authors

* **Vedant Dhopte**
* **Theo Knoll**
* **Christine Sun**
* **Theresa Lim**
* **Justice Chukwuma**
 

## Acknowledgments

* Princeton COS Council - Hosted hackathon