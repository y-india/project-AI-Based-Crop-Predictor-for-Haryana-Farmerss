import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# =========================
# Load Moisture Model
# =========================
try:
    moisture_model = joblib.load("moisture_model.pkl")
except:
    moisture_model = None
    st.warning("⚠️ Moisture model missing. Moisture will be estimated.")

# District Encoding
district_map = {
    "ambala": 1, "yamunanagar": 2, "kurukshetra": 3, "karnal": 4,
    "panipat": 5, "rohtak": 6, "jind": 7, "kaithal": 8, "sonipat": 9,
    "hisar": 10, "sirsa": 11, "bhiwani": 12, "faridabad": 13,
    "gurugram": 14, "jhajjar": 15, "palwal": 16, "fatehabad": 17,
    "mahendragarh": 18, "rewari": 19,
}

# =========================
# Moisture Prediction
# =========================
def predict_moisture(district, year, month, day):
    if moisture_model is None:
        return 10

    district_code = district_map.get(district.lower(), 0)

    df = pd.DataFrame([{
        "District": district_code,
        "Year": int(year),
        "Month": int(month),
        "Day": int(day),
    }])

    try:
        moisture = float(moisture_model.predict(df)[0])
        return max(0, min(100, moisture))
    except:
        return 10

# =========================
# Full Crop Logic
# =========================
def recommend_crop(district, year, month, day, temp, rain, prev_crop, soil_type="loamy"):

    row = {
        "District": district,
        "Year": year,
        "Month": month,
        "Day": day,
        "temperature(°C)_full": temp,
        "rainfall(mm)_full": rain,
        "previous_crop": prev_crop,
        "soil_type": soil_type
    }

    # Predict moisture
    row["Predicted_Moisture_15cm"] = predict_moisture(
        district=row["District"],
        year=row["Year"],
        month=row["Month"],
        day=row["Day"]
    )

    # Extract values
    district = row["District"].lower().strip()
    month = int(row["Month"])
    temp = float(row["temperature(°C)_full"])
    rain = float(row["rainfall(mm)_full"])
    moist = float(row["Predicted_Moisture_15cm"])
    prev = row["previous_crop"].lower().strip()
    soil_type = soil_type.lower().strip()

    north = ["yamunanagar","ambala","kurukshetra","karnal"]
    central = ["panipat","rohtak","jind","kaithal","sonipat"]

    if district in north:
        zone = "north"
    elif district in central:
        zone = "central"
    else:
        zone = "south"

    crops = {
        "Wheat":0,"Mustard":0,"Barley":0,"Gram":0,"Rice":0,
        "Maize":0,"Cotton":0,"Bajra":0,"Sugarcane":0,
        "Moong (Green Gram)":0,"Sunflower":0,"Vegetables":0
    }

    # Rabi
    if month in [11,12,1,2,3]:
        if any(x in prev for x in ["rice","paddy","urad"]): crops["Wheat"]+=30
        if any(x in prev for x in ["cotton","maize"]):
            crops["Mustard"]+=20; crops["Gram"]+=15
        if moist<8 and rain<50: crops["Mustard"]+=25
        if 8<=moist<=12 and 18<=temp<=26: crops["Wheat"]+=25
        if temp<22 and rain<40: crops["Barley"]+=20
        if zone=="south": crops["Gram"]+=20
        if soil_type in ["loamy","sandy loam"]:
            crops["Wheat"]+=10; crops["Barley"]+=10
        if soil_type=="clayey": crops["Gram"]+=10

    # Kharif
    elif month in [6,7,8,9,10]:
        if any(x in prev for x in ["wheat","barley"]):
            if rain>120 and moist>10: crops["Rice"]+=30
            if zone=="south": crops["Cotton"]+=25
            else: crops["Maize"]+=20
        if any(x in prev for x in ["mustard","gram"]):
            if zone=="north": crops["Rice"]+=25
            elif zone=="south": crops["Bajra"]+=20
            else: crops["Maize"]+=20
        if rain<80 and temp>30: crops["Bajra"]+=20
        if rain>150 and zone=="north": crops["Sugarcane"]+=25
        if soil_type in ["loamy","clayey"]:
            crops["Rice"]+=15; crops["Sugarcane"]+=10
        if soil_type=="sandy":
            crops["Bajra"]+=15; crops["Cotton"]+=10

    # Zaid
    elif month in [4,5]:
        if temp>30 and rain<80: crops["Moong (Green Gram)"]+=25
        if rain>100: crops["Maize"]+=20
        if moist>12: crops["Vegetables"]+=25
        if soil_type in ["loamy","sandy loam"]:
            crops["Sunflower"]+=15; crops["Moong (Green Gram)"]+=10
        if soil_type=="clayey": crops["Vegetables"]+=10

    best = max(crops, key=crops.get)
    return best, moist

# =========================
# UI Theme
# =========================
st.set_page_config(page_title="Haryana AI Crop Advisor", layout="wide")

# Background
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #e9f5e1, #cfe8c3);
}
</style>
""", unsafe_allow_html=True)

# Header with logo
c1,c2 = st.columns([0.15,1])
with c1:
    st.image("farmer.png", width=80)
with c2:
    st.markdown("<h1 style='color:#1b5e20;'>Haryana AI Crop Advisor</h1>", unsafe_allow_html=True)
    st.caption("AI powered crop advice for Haryana farmers")

st.write("")

# =========================
# Input Form
# =========================
col1, col2 = st.columns(2)

district = col1.selectbox("District", list(district_map.keys()))
date = col2.date_input("Date", datetime.today())
prev_crop = col1.selectbox("Previous Crop", ["Wheat","Rice","Maize","Cotton","Bajra","Mustard","Gram"])
soil = col2.selectbox("Soil Type", ["Loamy","Sandy","Clayey","Sandy Loam"])
temp = col1.slider("Temperature (°C)", 5, 50, 30)
rain = col2.slider("Rainfall (mm)", 0, 300, 20)

# Predict Button
if st.button("Predict Crop"):
    y,m,d = date.year, date.month, date.day
    crop, moist = recommend_crop(district, y, m, d, temp, rain, prev_crop, soil)
    st.success(f"🌾 Recommended Crop: **{crop}**")
    st.info(f"Soil Moisture Estimate: **{moist:.2f}%**")
