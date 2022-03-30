
from wtforms import Form, StringField, SubmitField, validators, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields import TextAreaField, HiddenField

class UpdateForm(Form):
    tittel = StringField('Tittel', validators=[DataRequired()])
    ingress = StringField('Ingress', validators=[DataRequired()])
    oppslagstekst = TextAreaField('Oppslagstekst', validators=[DataRequired()])
    kategori = SelectField("Kategori", choices=[("bil", "Bil"), ("motorsykkel", "Motorsykkel"), ("båt", "Båt"), ("fly", "Fly"), ("diverse", "Diverse")])
    id = HiddenField(validators=[DataRequired()])
    bruker = HiddenField()
    submit = SubmitField('Update')
