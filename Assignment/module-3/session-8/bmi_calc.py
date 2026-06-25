'''Use the math module to build a BMI calculator in bmi_calc.py.
 Take weight (kg) and height (meters) as input, use math.pow() for squaring,
 and print the calculated BMI rounded to 2 decimals.'''

'''BMI ka full form Body Mass Index hai.

Ye ek measure hai jo weight aur height ke basis par batata hai ki kisi vyakti ka weight uski height ke hisab se normal hai ya nahi.

Formula
BMI = Weight (kg) / Height² (m²)'''

'''round() ka use decimal values ko limit karne ke liye kiya jata hai.

BMI calculate karne par result aksar bahut saare decimal points me aata hai.'''

import math

weight=float(input("enter weight in kg:"))
height=float(input("enter height in meters:"))

bmi=weight/math.pow(height,2)

print("BMI",round(bmi,2))

if bmi<18.5:
    print("Category:Unserweight")

elif bmi<25:
    print("Category:Normal Wright")

elif bmi<30:
    print("Category: Overweight")
else:
    print("Category: Obese")