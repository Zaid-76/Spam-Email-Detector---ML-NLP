Gmail Spam Email Classifier
Hey there, Zaid here and this is 
A Python-based project that uses Machine Learning and the Gmail API to classify recent emails as SPAM or NOT SPAM.

It consists of two parts:
> Training the model with your own dataset.
> Classifying your Gmail inbox emails using the trained model.

Features:
> Train a spam email classification model using Gaussian Naive Bayes model.
> Bag-of-Words text vectorization using CountVectorizer.
> Fetch and classify your 15 most recent Gmail emails.
> Works directly with your Gmail account via the Gmail API.
> Saves and reuses authentication tokens to avoid repeated logins.

Setup & Installation:
1. Clone the repository
2. Install dependencies
3. Enable Gmail API & Get Credentials: 
      Go to Google Cloud Console.
      Enable the Gmail API.
      Create OAuth 2.0 Client Credentials.
      Download the credentials file and rename it to credentials.json.
      Place it in the project directory.
4.Training the Model:

      python model_training.py
   
      Enter the CSV file name (without .csv extension) when prompted.
      The dataset must contain:
        text column → Email content.
        spam column → 1 for SPAM, 0 for NOT SPAM.
      Saves:
        classifier.joblib → Trained ML model.
        vectorizer.joblib → CountVectorizer object.
5. Classifying Emails:
      
      python spam_email_classifier.py

      The script will:
        Authenticate your Gmail account (only the first time).
        Fetch your 15 most recent emails.
        Display Subject → Classification (SPAM/NOT SPAM).

IMPORTANT NOTES:
1. If you want to custom train your classification model then please execute the model_training.py file with the respective dataset and classifier model first and then the spam_email_classifier.py file.
2. You can alter the model parameters(fine tuning) for better results.
3. All the files of .joblib extensions are created in the project directory, so need to worry about the path.
4. Take care about the google cloud console and gmail API settings.

THANK YOU! 
FOLLOW UP FOR MORE AND MORE EXCITING UPDATES AND PROJECTS! BOOYAH!!!!!!!!
