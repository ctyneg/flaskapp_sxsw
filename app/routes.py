from flask import Flask, render_template, request
from flask.ext.googlemaps import GoogleMaps
from forms import locationSelectionForm
from find_recommendations import show_recommendations
 
app = Flask(__name__)   
GoogleMaps(app)   

app.secret_key="development key"
 
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/gmap', methods=['GET','POST'])
def gmap():
	form=locationSelectionForm()
	if request.method=='POST':
		selected_location=request.form['current_location']
		selected_event=request.form['next_event']
		calculations=show_recommendations(selected_location,selected_event)
		calc_status=calculations['message']
		calc_events=calculations['next_events']
		if calc_status=='SUCCESS':
			return render_template(
				'gmap.html', 
				success=True, 
				form=form, 
				next_events=calc_events, 
				)
		else:
			return render_template('gmap.html', success=False, form=form)
	elif request.method=='GET':
		return render_template('gmap.html', form=form)
 
if __name__ == '__main__':
	app.run(debug=True)