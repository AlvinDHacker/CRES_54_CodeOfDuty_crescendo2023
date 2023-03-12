""""
this model uses souns as a way to predict whether the person has parkinsonse disease or not 
the way they speak
"""




import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

park_dataset=pd.read_csv('parkinsons.csv')

x1=park_dataset.drop(columns=['status'])
x=x1.iloc[:,1:].values
y=park_dataset.iloc[:,17].values


scaler=StandardScaler()
scaler.fit(x)
standardized_data=scaler.transform(x)
standardized_data
X=standardized_data
Y=y

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=2)

classifier=svm.SVC(kernel='linear',probability=True)
classifier.fit(x_train,y_train)

x_train_pred=classifier.predict(x_train)
training_data_score=accuracy_score(x_train_pred,y_train)

x_test_pred=classifier.predict(x_test)
test_data_score=accuracy_score(x_test_pred,y_test)



"""
Matrix column entries (attributes):
name - ASCII subject name and recording number
MDVP:Fo(Hz) - Average vocal fundamental frequency
MDVP:Fhi(Hz) - Maximum vocal fundamental frequency
MDVP:Flo(Hz) - Minimum vocal fundamental frequency
MDVP:Jitter(%),MDVP:Jitter(Abs),MDVP:RAP,MDVP:PPQ,Jitter:DDP - Several 
measures of variation in fundamental frequency
MDVP:Shimmer,MDVP:Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,MDVP:APQ,Shimmer:DDA - Several measures of variation in amplitude
NHR,HNR - Two measures of ratio of noise to tonal components in the voice
status - Health status of the subject (one) - Parkinson's, (zero) - healthy
RPDE,D2 - Two nonlinear dynamical complexity measures
DFA - Signal fractal scaling exponent
spread1,spread2,PPE - Three nonlinear measures of fundamental frequency variation
"""
input_data=(119.99200,157.30200,74.99700,0.00784,0.00007,0.00370,0.00554,0.01109,0.04374,0.42600,0.02182,0.03130,0.02971,0.06545,0.02211,21.03300,0.414783,0.815285,-4.813031,0.266482,2.301442,0.284654)
input_data_array=np.asarray(input_data)
input_data_reshaped=input_data_array.reshape(1,-1)
std_data=scaler.transform(input_data_reshaped)
pred=classifier.predict(std_data)
pred_val=classifier.predict_proba(std_data)
print(pred)
print(pred_val)
