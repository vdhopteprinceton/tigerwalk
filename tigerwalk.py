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

#user database
class Users(db.Model):
    username = db.Column(db.String(150), nullable=False, primary_key=True)
    name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    groupme = db.Column(db.String(150), nullable=True)
    facebook = db.Column(db.String(150), nullable=True)
    profilepic = db.Column(db.Text(), nullable=True)
    active = db.Column(db.Boolean(), nullable=False)


    def __repr__(self):
        return f"user('{self.name}', '{self.phone}', '{self.groupme}', '{self.facebook}', '{self.profilepic}')"

@app.route('/')
def home():
    username = CASClient().authenticate()
    username = username.strip()

    try:
        user = Users.query.filter_by(username=username).one()
    except:
        user = Users(username=username, active=False)
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
        user.name = addUser
        user.active = True
        db.session.commit()

    deleteUser = request.args.get("deleteUser")
    if deleteUser is not None:
        user = Users.query.filter_by(username=deleteUser).one()
        user.active = False
        db.session.commit()

    walkers = []
    
    myname = ""
    for user in Users.query.filter_by(active=True).all():
        walkers.append(user.name)
        if user.username == username:
            myname = user.name

    html = render_template('activeWalkers.html', walkers=walkers, username=username, myname=myname)
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

    number = request.args.get('number')
    facebook = request.args.get('facebook')
    groupme = request.args.get('groupme')

    if number is not None:
        user.phone = number
        db.session.commit()
    if facebook is not None:
        user.facebook = facebook
        db.session.commit()
    if groupme is not None:
        user.groupme = groupme
        db.session.commit()

    number = user.phone
    facebook = user.facebook
    groupme = user.groupme

    html = render_template('profile.html', username=username, profilepic=profilepic, number=number, facebook=facebook, groupme=groupme)
    response = make_response(html)
    return response

@app.route('/map')
def map():
    username = CASClient().authenticate()
    username = username.strip()

    html = render_template('map.html')
    response = make_response(html)
    return response

@app.route('/contactInfo')
def contactInfo():
    username = CASClient().authenticate()
    username = username.strip()

    otherUsername = request.args.get("username");
    otherUser = Users.query.filter_by(name = otherUsername).one();

    number = otherUser.phone;
    facebook = otherUser.facebook;
    groupme = otherUser.groupme;
    profilepic = otherUser.profilepic;

    html = render_template('contactInfo.html', number=number, facebook = facebook,  groupme = groupme, profilepic = profilepic)
    response = make_response(html)
    return response

if __name__ == '__main__':
    app.run(debug=True)
