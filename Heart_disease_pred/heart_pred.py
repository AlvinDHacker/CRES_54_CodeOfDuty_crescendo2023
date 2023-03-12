import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

heart_dataset=pd.read_csv('heart_disease_training_data.csv')
x=heart_dataset.iloc[:,0:-1].values
y=heart_dataset.iloc[:,-1].values

scaler=StandardScaler()
scaler.fit(x)
standardized_data=scaler.transform(x)
standardized_data

X=standardized_data
Y=y

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=2)

cls=LogisticRegression(random_state=0)
cls.fit(x_train,y_train)

y_pred=cls.predict(x_test)


#accuracy_score(y_test,y_pred)

"""
here the sex is in 1 for male and 0 for female please check it 
"""

""""
INFORMTION OF WHAT NEEDS TO BE ASKED
1. age
2. sex
3. chest pain type (4 values)
4. resting blood pressure
5. serum cholestoral in mg/dI
6. fasting blood sugar > 120 mg/di
7. resting electrocardiographic results (values 0,1,2)
8. maximum heart rate achieved
9. exercise induced angina
10. oldpeak = ST depression induced by exercise relative to rest
11. the slope of the peak exercise ST segment
12. number of major vessels (0-3) colored by flourosopy
13. thal: 3 = normal; 6 = fixed defect; 7 = reversable defect
"""

age=float(input('Enter age '))
sex=float(input('Enter sex '))
cp=float(input('Enter cp '))
trestbps=float(input('Enter trestbps '))
chol=float(input('Enter chol '))
fbs=float(input('Enter fbs '))
restecg=float(input('Enter restecg '))
thalach=float(input('Enter thelach '))
exang=float(input('Enter exang '))
oldpeak=float(input('Enter oldpeak '))
slope=float(input('Enter slope '))
ca=float(input('Enter ca '))
thal=float(input('Enter thal '))
print(cls.predict(scaler.transform([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])))

67,
1,
0,
160,
286,
0,
0,
108,
1,
1.5,
1,
3,
2