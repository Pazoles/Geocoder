from flask import Flask, make_response, request, render_template, redirect, url_for, send_file
from census_geo import chunketize, geocode

app = Flask(__name__)
#app.config.from_object('config')

@app.route('/geo', methods=["POST"])
def geo_post():
    file = request.files['data_file']
    filename = request.files['data_file'].name

    if not file:
        return "No file attached"

    file_contents = open(filename, 'r')

    result = geocode(file_contents)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response

@app.route('/')
def home():
    return render_template('geo.html')

#Error Handlers (404,403,500)
@app.errorhandler(404)
def erorr404(error):
	return render_template('404.html'), 404

@app.errorhandler(403)
def erorr403(error):
	return render_template('403.html'), 403

@app.errorhandler(500)
def erorr404(error):
	#May want to add in a db rollback in here too.
	return render_template('500.html'), 500

if __name__ == '__main__':
        app.debug = True
        app.run(debug=True)
