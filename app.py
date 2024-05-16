from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm
from models import db, connect_db, Pet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'petadoption:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretsqlkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def list_pets():
    """List Pets"""
   pets = Pet.query.all()
   return render_template("pets_list.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Add Pet"""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data 
        species = form.species.data
        photo_url = form.photo.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        return redirect("/")
    else:    
        return render_template("add_pet.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"]) 
def edit_pet(pet_id):
    """Edit Pet""" 

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        return redirect("/") 

    else:
        return render_template("edit_pet.html", form=form, pet=pet)

@app.route("/api/pets/<int:pet_id", methods=["GET"])
def get_info(pet_id):
    """Gets info about pet from API"""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)
