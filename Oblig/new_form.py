    
from wtforms import Form, StringField, SubmitField, validators, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields import TextAreaField, HiddenField

class NewForm(Form):
    tittel = StringField('Tittel', validators=[DataRequired()])
    ingress = StringField('Ingress', validators=[DataRequired()])
    oppslagstekst = TextAreaField('Oppslagstekst', validators=[DataRequired()])
    kategori = SelectField("Kategori", choices=[("bil", "Bil"), ("motorsykkel", "Motorsykkel"), ("båt", "Båt"), ("fly", "Fly"), ("diverse", "Diverse")])
    id = HiddenField()
    bruker = HiddenField()
    submit = SubmitField('Update')
    bruker = StringField('Bruker', validators=[DataRequired()])