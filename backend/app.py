from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/register-experiment", methods=["POST"])
def register_experiment():
    data = request.json

    print("Received experiment data:")
    print(data)

    return jsonify({
        "status": "success",
        "message": "Experiment received by backend",
        "data": data,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
