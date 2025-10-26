
import pandas as pd
import numpy
import random

# list of crop values that mostly grown in haryana
crops = [
    "Cereals", "Wheat", "Rice (Paddy)", "Maize", "Bajra (Pearl Millet)", 
    "Barley", "Jowar (Sorghum)", "Gram (Chickpea)", "Moong (Green Gram)", 
    "Masoor (Lentil)", "Urad (Black Gram)", "Arhar (Pigeon Pea)", 
    "Mustard (Rapeseed & Mustard)", "Sunflower", "Groundnut", "Sesamum (Til)", 
    "Cotton", "Sugarcane", "Potato", "Onion", "Tomato", "Cauliflower", 
    "Cabbage", "Garlic"
]

# 3960 crop data
# data = {"previous crop": [random.choice(crops) for _ in range(3960)]}

# df = pd.DataFrame(data)

# Save to CSV
# df.to_csv("previous_crop_dataset.csv", index=False)

print("Dataset with 3960 rows has been created and saved as 'previous_crop_dataset.csv'.")
print("\nFirst 5 rows of the dataset for preview:")
# print(df.head())



data_main = pd.read_csv(r"D:\#PROJECTS\Crop Recommendation System for Indian Farmerss\previous_crop_dataset.csv")
print(data_main.head(5))

unique = numpy.unique_counts(data_main["previous crop"])

print(unique)