import pandas as pd
import numpy as np

data = pd.read_csv(r"D:\#PROJECTS\Crop Recommendation System for Indian Farmerss(c)\SoilMoisture_haryana_original.csv")
df = pd.DataFrame(data)

df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)

print(df.head(5))


print("""
The problem:

Months go in a circle: after December comes January. But if you just write them as numbers 1, 2, ..., 12, a computer thinks December (12) is far from January (1). That’s wrong!

The solution:

We use sine and cosine to put months on a circle:

df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)


This turns each month into two numbers.

These numbers tell the computer where the month is on a circle.

Now December and January are next to each other, just like in real life.

Example:

January → (sin ≈ 0.5, cos ≈ 0.87)

December → (sin ≈ -0.5, cos ≈ 0.87)

Even though the numbers 1 and 12 are far apart, on the circle they are close
""")