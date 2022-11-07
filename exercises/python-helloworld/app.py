from flask import Flask
import logging


app = Flask(__name__)

@app.route("/")
def hello():
    app.logger.info('Main request successfull')
    return "Hello 2 World!"

@app.route('/status')
def status():
    app.logger.info('status request successfull')
    response = app.response_class(
          response=json.dumps({"result":"OK - healthy"}),
          status=200,
          mimetype='application/json'
          )
    return response

@app.route('/metrics')
def metrics():
    app.logger.info('Main request successfull')
    response = app.response_class(
          response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
          status=200,
          mimetype='application/json'
          )
    return response

if __name__ == "__main__":
    # Stream logs to a file, and set the default log level to DEBUG
  logging.basicConfig(filename='app.log',level=logging.DEBUG)
  app.run(host='0.0.0.0')
