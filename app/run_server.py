# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pickle
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		print('Ok')
		model = dill.load(f)
	print(model)

#modelpath = "/home/artcom5/GeekBrains/ml_business/9_lesson/course_project/logreg_cardio.dill"
modelpath = "/app/app/models/logreg_cardio.dill"
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		age, height, weight, cholesterol, smoke, alco, active = int(), int(), int(), int(), int(), int(), int()
		request_json = flask.request.get_json()
		print(request_json)
		if request_json['age']:
			age = request_json['age']

		if request_json['height']:
			height = request_json['height']

		if request_json['weight']:
			weight = request_json['weight']

		if request_json['cholesterol']:
			cholesterol = request_json['cholesterol']

		if request_json['smoke']:
			smoke = request_json['smoke']

		if request_json['alco']:
			alco = request_json['alco']

		if request_json['active']:
			active = request_json['active']

		logger.info(f'{dt} Data: age={age}, height={height}, weight={weight}, '
					f'cholesterol={cholesterol}, smoke={smoke}, alco={alco}, active={active}')
		try:
			df = pd.DataFrame({'age': age, 'height': height, 'weight': weight,
							   'cholesterol': cholesterol, 'smoke': smoke, 'alco': alco,
							   'active': active}, index=[0])
			print(df)
			preds = model.predict_proba(df)

		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds[:, 1][0]
		# indicate that the request was a success
		data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)