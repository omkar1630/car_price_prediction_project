from flask import Flask, request, render_template_string
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
with open("decision_tree_rp.pkl", "rb") as file:
    model = pickle.load(file)

# Sample encoding dictionaries
# Update these according to your dataset if needed
make_map = {
    "Toyota": 0,
    "Honda": 1,
    "Ford": 2,
    "BMW": 3,
    "Hyundai": 4
}

model_map = {
    "Corolla": 0,
    "Civic": 1,
    "Focus": 2,
    "X5": 3,
    "i20": 4
}

fuel_map = {
    "Petrol": 0,
    "Diesel": 1,
    "CNG": 2,
    "Electric": 3
}

transmission_map = {
    "Manual": 0,
    "Automatic": 1
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Car Price Prediction System</title>

    <style>
        body{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg,#1e3c72,#2a5298);
            margin:0;
            padding:0;
        }

        .container{
            width:550px;
            margin:40px auto;
            background:white;
            padding:30px;
            border-radius:20px;
            box-shadow:0px 8px 25px rgba(0,0,0,0.2);
        }

        h1{
            text-align:center;
            color:#1e3c72;
        }

        label{
            font-weight:bold;
        }

        input,select{
            width:100%;
            padding:10px;
            margin-top:5px;
            margin-bottom:15px;
            border-radius:8px;
            border:1px solid #ccc;
        }

        button{
            width:100%;
            padding:12px;
            background:#1e3c72;
            color:white;
            border:none;
            border-radius:10px;
            cursor:pointer;
            font-size:16px;
        }

        button:hover{
            background:#16315f;
        }

        .result{
            margin-top:20px;
            text-align:center;
            font-size:22px;
            color:green;
            font-weight:bold;
        }
    </style>
</head>
<body>

<div class="container">

<h1>🚗 Car Price Prediction System</h1>

<form method="POST">

<label>Make</label>
<select name="make">
{% for item in makes %}
<option value="{{item}}">{{item}}</option>
{% endfor %}
</select>

<label>Model</label>
<select name="model">
{% for item in models %}
<option value="{{item}}">{{item}}</option>
{% endfor %}
</select>

<label>Year</label>
<input type="number" name="year" required>

<label>Engine Size</label>
<input type="number" step="0.1" name="engine_size" required>

<label>Mileage</label>
<input type="number" name="mileage" required>

<label>Fuel Type</label>
<select name="fuel">
{% for item in fuels %}
<option value="{{item}}">{{item}}</option>
{% endfor %}
</select>

<label>Transmission</label>
<select name="transmission">
{% for item in transmissions %}
<option value="{{item}}">{{item}}</option>
{% endfor %}
</select>

<button type="submit">Predict Price</button>

</form>

{% if prediction %}
<div class="result">
💰 Estimated Price: ₹ {{prediction}}
</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":

        make = make_map[request.form["make"]]
        model_name = model_map[request.form["model"]]
        year = int(request.form["year"])
        engine_size = float(request.form["engine_size"])
        mileage = float(request.form["mileage"])
        fuel = fuel_map[request.form["fuel"]]
        transmission = transmission_map[request.form["transmission"]]

        input_data = pd.DataFrame(
            [[
                make,
                model_name,
                year,
                engine_size,
                mileage,
                fuel,
                transmission
            ]],
            columns=[
                "Make",
                "Model",
                "Year",
                "Engine Size",
                "Mileage",
                "Fuel Type",
                "Transmission"
            ]
        )

        result = model.predict(input_data)[0]
        prediction = f"{result:,.2f}"

    return render_template_string(
        HTML,
        prediction=prediction,
        makes=make_map.keys(),
        models=model_map.keys(),
        fuels=fuel_map.keys(),
        transmissions=transmission_map.keys()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
