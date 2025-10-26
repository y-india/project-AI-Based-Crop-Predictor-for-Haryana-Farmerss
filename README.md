# 🌾 AI-Based Crop Predictor for Haryana Farmers

## 📘 Overview
The **AI-Based Crop Predictor for Haryana Farmers** is a Machine Learning project designed to help Indian farmers — especially from **Haryana** — make data-driven decisions about which crop to grow next.  

Many farmers struggle to identify soil moisture and other scientific factors.  
This project uses **AI + simple farmer inputs** to predict **best-suited crops** for given conditions — without requiring any complex knowledge like NPK values or soil pH.

---

## 🧑‍💻 Author
**Developed by Yuvraj**  
17-year-old Indian developer skilled in **Python, Machine Learning, and Data Science**.  
Focused on building real-world AI projects that create meaningful social impact.

---

## 🎯 Project Objective
- Predict **soil moisture** using historical weather and satellite data.
- Use this predicted moisture with **farmer-friendly inputs** (district, date, temperature, rainfall, previous crop, soil type) to predict the **best crop to grow**.
- Simplify agricultural data science for real-world rural use cases.

---

## 🧠 Workflow (Step-by-Step)

### 🩵 Step 1: Moisture Prediction (`#1moisture_finder.ipynb`)
- Cleaned and explored the Haryana dataset with columns like:  
  `State, District, Date, Year, Month, Moisture, Source`
- Performed:
  - Null handling, dropping unnecessary columns, type conversions  
  - EDA: graphs, distributions, relationships
- Model Used: **LightGBM Regressor (lgb.LGBMRegressor)**  
  - Hyperparameter tuning via **GridSearchCV**
  - ✅ **Training Accuracy:** 99.75%  
  - ✅ **Testing Accuracy:** 96.28%
- Defined a reusable **moisture prediction function** for new farmer inputs.

---

### 🩶 Step 2: Month Feature Engineering (`#2what_is_this_(month_sin).py`)
- Explained and implemented **sin/cos transformations** on month features.  
- Reason: To capture **cyclical nature of months** (Jan & Dec are close in time).

---

### 💚 Step 3: Generating 3960-Row Moisture Data (`#3making_3960rows_moisture.py`)
- Used the trained moisture prediction model to generate a **large synthetic dataset (3960 rows)**.
- This extended dataset later helps in merging multiple input features to build a final, comprehensive dataset for crop prediction.

---

### 💛 Step 4: Feature Engineering for Crop Prediction (`#4important_works.ipynb`)
- Started with dataset having:  
  `N, P, K, Temperature, Humidity, pH, Rainfall, Label`
- Removed **N, P, K, Humidity, pH** (since farmers can’t easily measure these).  
- Focused on **inputs that farmers can provide** like:
  - Temperature  
  - Rainfall  
  - Date (Month/Day)  
  - District  
  - Previous Crop  
- Created `final_dataset.xlsx` with clean, practical inputs.

---

### 🧡 Step 5: Building Previous Crop Dataset (`#5previous_crop_dataset.py`)
- Created a dataset of **~4000 rows** showing commonly grown crops in Haryana.
- Integrated this dataset with the main one to improve crop recommendation accuracy.

---

### ❤️ Step 6: Best Crop Prediction Model (`#6BEST_CROP_PREDICTOR.ipynb`)
- Combined all previous outputs into a **final AI model**.
- Inputs used:
  - District  
  - Year, Month, Day  
  - Temperature  
  - Rainfall  
  - Predicted Moisture (15cm)  
  - Previous Crop  
  - Soil Type  
- Output: **Recommended Best Crop to Grow**

---

## 🧩 Skills & Technologies Used

| Category | Tools / Techniques |
|-----------|--------------------|
| **Programming** | Python |
| **Data Handling** | pandas, numpy |
| **Visualization** | matplotlib, seaborn |
| **Machine Learning** | scikit-learn, lightgbm |
| **Model Optimization** | RandomizedSearchCV, GridSearchCV |
| **Feature Engineering** | cyclical encoding (sin/cos), data scaling |
| **Data Cleaning & EDA** | Handling nulls, describe(), unique(), dtype(), graphs |
| **File Handling** | Excel, CSV |
| **Version Control** | Git & GitHub |

---

## ⚙️ How to Run
```bash
# Clone the repository
git clone https://github.com/y-india/AI-Based-Crop-Predictor-Haryana.git

# Navigate to project folder
cd AI-Based-Crop-Predictor-Haryana

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install required libraries
pip install -r requirements.txt

# Open the main notebook
jupyter notebook "#6BEST_CROP_PREDICTOR.ipynb"
```
## 🪄 Example Output

“For Ambala district on 5th January with given conditions, the most suitable crop to grow is Cabbage 🌱."



```


email -> y.india.main@gmail.com


```

