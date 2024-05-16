from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, URL, NumberRange, AnyOf, Optional

class AddPetForm(FlaskForm):
    """Form to add pet"""
    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField("Species", validators=[InputRequired(), AnyOf(values=["cat", "dog", "porcupine"])])
    photo = StringField("Photo URL", validators=[URL()])
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30)])
    notes = StringField("Notes")

class EditPetForm(FlaskForm):
    """Form to edit pet"""
    photo_url = StringField("Photo URL", validators=[Optional(), URL()],)
    notes = TextAreaField("Comments" validators=[Optional(), URL()],)
    available = BooleanField("Available?")

    