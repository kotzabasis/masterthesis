import pandas as pd

"""Importing the Train dataset"""
dataset = pd.read_csv('DataSK.csv')
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

"""Transform the categorical data into numerical data"""
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0,1])], remainder='passthrough')
X = ct.fit_transform(X)

"""Training the Random Forest Regression model on the whole dataset"""
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 280, random_state = 0)
regressor.fit(X, y)

"""Importing the Test dataset"""
test_dataset = pd.read_csv('TestData.csv')
tasks=[];
resources=[];
estimated_time=[];
for index,row in test_dataset.iterrows():
    """Making time predictions and storing into list"""
    tasks.append(row['TaskID']);
    resources.append(row['ResourceID']);
    estimated_time.append(regressor.predict(ct.transform([[row['TaskID'], row['Res_Tag'], row['SkillLevel'], row['YOE'], row['ResourceCost']]]))[0]);

"""Creating the dataframe to return to .csv file"""
data={'TaskID':tasks,'ResourceID':resources,'EstimatedTime':estimated_time}
df = pd.DataFrame(data=data)
df.to_csv('EstimatedTimes.csv', index=False)