# 🚀 NEO Hazard Predictor

A machine learning web app that predicts whether a Near-Earth Object (NEO) — like an asteroid — is potentially hazardous to Earth 🌍☄️

Built using:
- Python
- Scikit-learn
- Streamlit
- NASA NEO API

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app/)

Features

-  Enter custom asteroid parameters and get predictions
-  Use real-time data from NASA’s Near Earth Object API
-  Visual feedback for parameters like diameter & velocity
-  Model is hosted externally (Google Drive) and fetched at runtime
-  Fully deployed on Streamlit Cloud — no setup needed

---

Tech Stack
-Python 3.12
-scikit-learn — Random Forest Classifier
-joblib— Model serialization
- Streamlit— For interactive UI and deployment
- Google Drive — Hosting the ML model externally
- NASA Open API — For fetching live NEO data

---

 How It Works

The model is trained to classify NEOs based on:
- Estimated Diameter (min & max)
- Relative Velocity
- Miss Distance from Earth
- Absolute Magnitude
- Diameter Difference

A Random Forest Classifier was tuned using randomized search and evaluated on real NASA data.
