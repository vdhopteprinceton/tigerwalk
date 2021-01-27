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
class Users(db.Model):
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
        user = Users.query.filter_by(username=username).one()
    except:
        user = Users(username=username)
        db.session.add(user)
        db.session.commit()

    html = render_template('home.html')
    response = make_response(html)
    return response

@app.route('/seewalkers')
def activeWalkers():
    username = CASClient().authenticate()
    username = username.strip()

    addUser = request.args.get("name")

    if addUser is not None:
        user = Users.query.filter_by(username=username).one()
        oldName = user.name
        
        if oldName != addUser:
            user.name = addUser
            db.session.commit()

            walkers.append(addUser)
            if oldName is not None:
                if oldName in walkers:
                    walkers.remove(oldName)
        else:
            if oldName not in walkers:
                walkers.append(oldName)

    deleteUser = request.args.get("deleteUser")
    if deleteUser is not None:
        user = Users.query.filter_by(username=deleteUser).one()
        name = user.name

        if name is not None:
            if name in walkers:
                walkers.remove(name)

    html = render_template('activeWalkers.html', walkers=walkers, username=username)
    response = make_response(html)
    return response

@app.route('/myprofile', methods=['GET', 'POST'])
def profile():
    username = CASClient().authenticate()
    username = username.strip()

    newprofilepic = request.files.get('newprofilepic')

    if newprofilepic is not None:
        newprofilepic = imageToURL(newprofilepic)
        user = Users.query.filter_by(username=username).one()
        user.profilepic = newprofilepic
        db.session.commit()

    user = Users.query.filter_by(username=username).one()
    profilepic = user.profilepic

    print(profilepic)

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
