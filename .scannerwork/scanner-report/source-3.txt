from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/samples', methods=['GET'])
def get_samples():
    return jsonify({"message": "Hello from SampleProject!", "status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)