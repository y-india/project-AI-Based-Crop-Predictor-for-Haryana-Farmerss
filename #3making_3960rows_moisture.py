import pandas as pd
import numpy as np




data = pd.read_csv(r"D:\#PROJECTS\Crop Recommendation System for Indian Farmerss(c)\SoilMoisture_haryana_original.csv")

df = pd.DataFrame(data)


df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df['Year'] = df['Date'].dt.year
df['DayOfYear'] = df['Date'].dt.dayofyear
df['Day'] = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.weekday
df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)


df = pd.get_dummies(df, columns=['District'], drop_first=False)

# print(df.head(5))


# Features and target
features = ['Year', 'Month', 'Month_sin', 'Month_cos', 'DayOfYear', 'Day', 
            'Weekday'] + [col for col in df.columns if 'District_' in col]
X = df[features]
y = df['Avg_smlvl_at15cm']


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score

model = lgb.LGBMRegressor(objective='regression', num_leaves=31, learning_rate=0.05, n_estimators=100)
model.fit(X_train, y_train)

# using
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

from sklearn.model_selection import GridSearchCV , RandomizedSearchCV

estimator_grid = {"num_leaves" : [31,40,50,60,70,100], "n_estimators" : [100,200,300,400] , "learning_rate" : [0.05,0.1,0.2,0.3]}



model_new = lgb.LGBMRegressor(objective='regression', 
                              learning_rate=0.2, n_estimators=400, num_leaves=100)
model_new.fit(X_train, y_train)

print(f"\n\n\n\n\n\n\n\nTRAINING SCORE OF NEW MODEL IS {model_new.score(X_train,y_train)*100}")
print(f"TESTING SCORE OF NEW MODEL IS {model_new.score(X_test,y_test)*100}")





def predict_moisture(district, year, month, day):
    # input for new data
    input_data = pd.DataFrame({
        'State': ['Haryana'],  
        'District': [district],
        'Month': [month],
        'Date': [f'{year}-{month:02d}-{day:02d}']
    })

    #finding features
    input_data['Date'] = pd.to_datetime(input_data['Date'])
    input_data['Year'] = input_data['Date'].dt.year
    input_data['DayOfYear'] = input_data['Date'].dt.dayofyear
    input_data['Day'] = input_data['Date'].dt.day
    input_data['Weekday'] = input_data['Date'].dt.weekday
    input_data['Month_sin'] = np.sin(2 * np.pi * input_data['Month'] / 12)
    input_data['Month_cos'] = np.cos(2 * np.pi * input_data['Month'] / 12)

    # One-hot encode District
    district_cols = [col for col in df.columns if 'District_' in col]
    input_data = pd.get_dummies(input_data, columns=['District'])
    for col in district_cols:
        if col not in input_data.columns:
            input_data[col] = 0

    # arranging
    features = ['Year', 'Month', 'Month_sin', 'Month_cos', 'DayOfYear', 'Day', 'Weekday'] + district_cols
    X_input = input_data[features]

    # Predict
    predicted = model_new.predict(X_input)
    return predicted[0]








'''
NOW I WANT TO MAKE NEW DATASET WITH THIS MODEL APPROX
                 3960 LINES !
'''


# Let's automatically generate around 3960 prediction tasks
districts = [
    "Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad",
    "Gurugram", "Hisar", "Jhajjar", "Jind", "Kaithal", "Karnal",
    "Kurukshetra", "Mahendragarh", "Nuh", "Palwal", "Panchkula",
    "Panipat", "Rewari", "Rohtak", "Sirsa", "Sonipat", "Yamunanagar"
]

# You can adjust these ranges as needed
year = 2023
months = [1,3,5, 7,9,11] 
days = range(1, 31)   

# Creating all (district, year, month, day) combinations
tasks = [
    {"district": d, "year": year, "month": m, "day": day}
    for d in districts
    for m in months
    for day in days
]

# ✅ Run predictions for all tasks
results = []

for i, task in enumerate(tasks, start=1):
    try:
        moisture_val = predict_moisture(task["district"], task["year"], task["month"], task["day"])
        results.append({
            "District": task["district"],
            "Year": task["year"],
            "Month": task["month"],
            "Day": task["day"],
            "Predicted_Moisture": moisture_val
        })
        print(f"[{i}/{len(tasks)}] ✅ {task['district']} ({task['month']}/{task['day']}) → {moisture_val:.2f}")
    except Exception as e:
        print(f"[{i}/{len(tasks)}] ⚠️ Error for {task['district']} ({task['month']}/{task['day']}): {e}")

results_df = pd.DataFrame(results)


# results_df.to_csv("moisture_predictions_merge.csv", index=False)
# print("\n✅ All predictions saved to 'moisture_predictions.csv'")
# print(f"Total predictions made: {len(results_df)}")