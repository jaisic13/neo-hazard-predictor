import streamlit as st
import joblib
import os
import requests
from datetime import date
import random 
import urllib.request

MODEL_URL = "https://drive.google.com/file/d/1ettapiX2lYJloEbA_j7Nv95_GX3i318j/view?usp=sharing"

# Download model if not present
if not os.path.exists("model.pkl"):
    try:
        st.info("⬇️ Downloading model from Google Drive...")
        urllib.request.urlretrieve(MODEL_URL, "model.pkl")
        st.success("✅ Model downloaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to download model: {e}")

# Load the model
if os.path.exists("model.pkl"):
    with open("model.pkl", "rb") as f:
        model = joblib.load(f)
else:
    st.error("❌ model.pkl not available.")

# Move this out of the 'else' block
st.markdown(
    """
    <style>
    /* Sidebar container */
    section[data-testid="stSidebar"] {
        width: 450px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        width: 450px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.sidebar.title("📘 About")

st.sidebar.markdown("""
### 🛰️ What is a Near-Earth Object (NEO)?

A **NEO** is an asteroid or comet whose orbit brings it into proximity with Earth. These celestial bodies, if large and fast enough, have the potential to cause significant damage upon impact , making early detection and risk analysis crucial for planetary defense.

### 🤖 What Does This Model Do?

This model leverages machine learning to predict whether an NEO is *potentially hazardous* based on real data from NASA.

The prediction is made using the following features:

- **Estimated Diameter (Min & Max)** – Size of the asteroid
- **Relative Velocity** – Speed at which it approaches Earth
- **Miss Distance** – Distance between the asteroid and Earth at its closest approach
- **Absolute Magnitude** – Measure of brightness
- **Estimated Diameter Difference** – Difference between max and min size

These inputs are passed into a trained **Random Forest Classifier**, which outputs whether the asteroid is likely to pose a threat.

---

### 🧪 Goal

To build a simple, efficient, and interpretable system that contributes to understanding and mitigating asteroid risks — one prediction at a time.
""")


st.title("NEO Hazard Prediction")

st.markdown("---")
st.subheader("🔭 Enter Near Earth Object Details Below")


col1, col2 = st.columns(2)

with col1:
    est_diameter_min = st.number_input('Estimated Diameter Min', format="%.6f")
    est_diameter_max = st.number_input('Estimated Diameter Max', format="%.6f")
    est_diameter_diff = est_diameter_max - est_diameter_min
    st.metric(label="Diameter Diff", value=f"{est_diameter_diff:.6f}")


with col2:
    relative_velocity = st.number_input('Relative Velocity (km/h)')
    miss_distance = st.number_input('Miss Distance (km)')
    absolute_magnitude = st.number_input('Absolute Magnitude')


if st.button("Predict Hazard"):
    # Prepare input as list of lists
    input_features = [[
        est_diameter_min,
        est_diameter_max,
        relative_velocity,
        est_diameter_diff,
        miss_distance,
        absolute_magnitude
    ]]
    
    prediction = model.predict(input_features)
    
    if prediction[0] == 1:
     st.error("⚠️ Potentially Hazardous Asteroid Detected!")
     st.markdown("Based on the provided data, this asteroid poses a potential threat.")
    else:
     st.success("✅ No Hazard Detected")
     st.markdown("This asteroid is not considered hazardous according to the current parameters.")

st.markdown("---")
st.subheader("🪐 Predict using Real NEO Data (NASA)")

nasa_api_key = "gzaN6rCs6wJyKhrYpjPnOu82JCgSr9BYetX5o7tW"  
selected_date = st.date_input("📅 Select a date", date.today())

if st.button("🚀 Fetch NEO from NASA"):
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={selected_date}&end_date={selected_date}&api_key={nasa_api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        neos = data['near_earth_objects'].get(str(selected_date), [])
         
        if not neos:
            st.warning("No NEOs found for this date.")
        else:
            asteroid = random.choice(neos)  # Using the first asteroid for prediction
            st.write("☄️ NASA Actual Hazard Flag:", asteroid['is_potentially_hazardous_asteroid'])
            name = asteroid['name']
            est_diameter_min = asteroid['estimated_diameter']['kilometers']['estimated_diameter_min']
            est_diameter_max = asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']
            rel_velocity = float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_second']) * 3600
            miss_distance = float(asteroid['close_approach_data'][0]['miss_distance']['kilometers'])
            abs_magnitude = asteroid['absolute_magnitude_h']
            diameter_diff = est_diameter_max - est_diameter_min

            st.success(f"Fetched asteroid: {name}")
            st.write(f"🪐 Estimated Diameter Min: {est_diameter_min:.4f} km")
            st.write(f"🪐 Estimated Diameter Max: {est_diameter_max:.4f} km")
            st.write(f"🚀 Relative Velocity: {rel_velocity:.2f} km/s")
            st.write(f"📏 Miss Distance: {miss_distance:.2f} km")
            st.write(f"💡 Absolute Magnitude: {abs_magnitude}")
            st.write(f"📐 Diameter Difference: {diameter_diff:.4f} km")

            # Run your model prediction
            model_input = [[est_diameter_min, est_diameter_max, rel_velocity, diameter_diff, miss_distance, abs_magnitude]]
            prediction = model.predict(model_input)

            st.subheader("⚠️ NASA-based Prediction Result")
            if prediction[0] == 0:  # Instead of == 1
              st.error("⚠️ Potentially Hazardous Asteroid Detected!")
            else:
             st.success("✅ No Hazard Detected")

