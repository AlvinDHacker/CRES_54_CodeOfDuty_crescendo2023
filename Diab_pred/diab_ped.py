import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

diab_dataset=pd.read_csv('diabetes_training_data.csv')
diab_dataset.describe()
diab_dataset.groupby('Outcome').mean()

x= diab_dataset.iloc[:,0:8].values
y=diab_dataset.iloc[:,-1].values

scaler=StandardScaler()
scaler.fit(x)
standardized_data=scaler.transform(x)
standardized_data

X=standardized_data
Y=y

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=2)

classifier=svm.SVC(kernel='linear')
classifier.fit(x_train,y_train)

x_train_pred=classifier.predict(x_train)
training_data_score=accuracy_score(x_train_pred,y_train)

x_test_pred=classifier.predict(x_test)
test_data_score=accuracy_score(x_test_pred,y_test)


"""
Here you need to change the input data and the the patients records
"""
Pregnancies=float(input('enter pregnancies'))
Glucose=float(input('enter glucose'))
BloodPressure=float(input('enter blood pressure'))
SkinThickness=float(input('enter SkinThickness'))
Insulin=float(input('enter INsulin'))
bmi=float(input('enter BMI'))
DiabetesPedigreeFunction=float(input('enter DiabetesPedigreeFunction'))
Age=float(input('enter age'))
input_data=(Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,bmi,DiabetesPedigreeFunction,Age)
input_data_array=np.asarray(input_data)
input_data_reshaped=input_data_array.reshape(1,-1)
std_data=scaler.transform(input_data_reshaped)
pred=classifier.predict(std_data)
print(pred)
