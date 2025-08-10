import numpy as np
# You need to run this file only once, just for training the classification model for spam email classification

#install the required libraries as mentioned below

import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.naive_bayes import GaussianNB


def mt(CSV):
    dataset = pd.read_csv(f'{CSV}.csv', encoding="ISO-8859-1")

    # Filter out rows where the 'label' column is not 1 or 0 (as integers) *OPTIONAL STEP*
    dataset = dataset[dataset['spam'].isin([1, 0])]
    # Removing unwanted repeating words in each text(row) based on dataset used, Basically small preprocessing step!
    dataset['text'] = dataset['text'].str.replace(r'\bSubject: \b', '', case=False, regex=True)
    dataset['text'] = dataset['text'].str.replace(r'[:]', '', case=False, regex=True)
    # Creating the Bag of Words model with a larger vocabulary
    cv = CountVectorizer(max_features=9500) # change the value of max_features for fine tuning based on your datset!
    # take care of the column names
    X = cv.fit_transform(dataset['text']).toarray()
    y = dataset["spam"]

    # Using label encoder (this is now redundant but kept for consistency) *OPTIONAL STEP*
    le = LabelEncoder()
    y = le.fit_transform(y)

    # Splitting the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Training the Gaussian Naive Bayes model
    # You can use any classification model that gives the best result
    classifier =  GaussianNB()
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix *OPTIONAL STEP*
    #cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)

    # Saving both the classifier and the CountVectorizer
    joblib.dump(classifier, 'classifier.joblib')
    joblib.dump(cv, 'vectorizer.joblib')

CSV=input("enter the name of csv file without extension: ") #You can input any training dataset that you want for
                                                            #maximum accuracy
mt(CSV)
print("Training process completed!!")
