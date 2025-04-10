#!/bin/bash
mkdir -p car_counter_website/templates

cat > car_counter_website/app.py << 'EOF'
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
EOF

cat > car_counter_website/templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Clovis Community College Parking Spots AC-3</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #ffffff;
            color: #333;
            margin: 0;
            padding: 0;
            text-align: center;
        }
        .header {
            padding: 50px 0;
            font-size: 2em;
            font-weight: 600;
        }
        .content {
            max-width: 600px;
            margin: auto;
            padding: 20px;
        }
        .counter {
            font-size: 4em;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="header">Clovis Community College Parking Spots AC-3</div>
    <div class="content">
        <div class="counter" id="counter">{{ car_count }}</div>
    </div>
    <script>
        function updateCount(action) {
            fetch("/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({action: action})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('counter').innerText = data.car_count;
            });
        }
        // Example auto-update every 5 seconds:
        // setInterval(() => updateCount("increment"), 5000);
    </script>
</body>
</html>
EOF

echo "Setup complete."

