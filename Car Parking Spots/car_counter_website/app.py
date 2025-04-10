from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
car_count = 0

@app.route("/")
def index():
    return render_template("index.html", car_count=car_count)

@app.route("/update", methods=["POST"])
def update():
    global car_count
    action = request.json.get("action")
    if action == "increment":
        car_count += 1
    elif action == "decrement":
        car_count = max(0, car_count - 1)
    return jsonify({"car_count": car_count})

if __name__ == "__main__":
    app.run(debug=True)
