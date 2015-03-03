from flask.ext.wtf import Form
from wtforms import SubmitField, TextField
 
class locationSelectionForm(Form):
  	current_location=TextField('My Current Location')
  	next_event=TextField('My Next Event')
  	submit = SubmitField("WHAT TO DO?")