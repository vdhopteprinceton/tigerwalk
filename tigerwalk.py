from flask import Flask
from flask import render_template, make_response, request
from flask_sqlalchemy import SQLAlchemy
from CASClient import CASClient
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = "tigerwalk key"
db = SQLAlchemy(app)

# for profile pics
def imageToURL(image):
    print("KJHKHKKH")
    cloudinary.config(
        cloud_name="vdhopte",
        api_key="482853372222936",
        api_secret="kMjjC-ooctqWxG2oE1Ym7u2AU84"
    )

    DEFAULT_TAG = "python_sample_basic"

    response = upload(image, tags=DEFAULT_TAG)
    url, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
    )
    return url

#active walker list
walkers = ['Theresa', 'Christine', 'Theo']

#user database
class User(db.Model):
    username = db.Column(db.String(150), nullable=False, primary_key=True)
    name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    groupme = db.Column(db.String(150), nullable=True)
    facebook = db.Column(db.String(150), nullable=True)
    profilepic = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return f"user('{self.name}', '{self.phone}', '{self.groupme}', '{self.facebook}')"

@app.route('/')
def home():
    username = CASClient().authenticate()
    username = username.strip()

    try:
        user = User.query.filter_by(username=username).one()
    except:
        user = User(username=username)

    html = render_template('home.html')
    response = make_response(html)
    return response

@app.route('/seewalkers')
def activeWalkers():
    username = CASClient().authenticate()
    username = username.strip()
    addUser = request.args.get("addUser")
    if addUser is not None:
        if addUser not in walkers:
            walkers.append(addUser)

    deleteUser = request.args.get("deleteUser")
    if deleteUser in walkers:
        walkers.remove(deleteUser)



    html = render_template('activeWalkers.html', walkers=walkers, username=username)
    response = make_response(html)
    return response

@app.route('/myprofile', methods=['GET', 'POST'])
def profile():
    username = CASClient().authenticate()
    username = username.strip()

    profilepic = request.files.get('profilepic')

    if profilepic is not None:
        profilepic = imageToURL(profilepic)

    html = render_template('profile.html', username=username, profilepic=profilepic)
    response = make_response(html)
    return response

@app.route('/map')
def map():
    username = CASClient().authenticate()
    username = username.strip()

    html = render_template('map.html')
    response = make_response(html)
    return response

if __name__ == '__main__':
    app.run(debug=True)
