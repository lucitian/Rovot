import re, string, pickle
import numpy as np
np.set_printoptions(suppress=True)
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn import linear_model

#TODO: Make the labels static
#('fear', 'sadness', 'anger', 'love', 'joy', 'surprise')
class TextProcessingModel:
    def __init__(self, text_data_train, text_data_test):
        """
        Text Data format should be {label_0: [text_data_list],...,label_h: [text_data_list]}
        """
        self.text_data_train = text_data_train
        self.text_data_test = text_data_test

        self.train_fear = text_data_train['fear']
        self.train_sadness = text_data_train['sadness']
        self.train_anger = text_data_train['anger']
        self.train_love = text_data_train['love']
        self.train_joy = text_data_train['joy']
        self.train_surprise = text_data_train['surprise']

        self.test_fear = text_data_test['fear']
        self.test_sadness = text_data_test['sadness']
        self.test_anger = text_data_test['anger']
        self.test_love = text_data_test['love']
        self.test_joy = text_data_test['joy']
        self.test_surprise = text_data_test['surprise']

        self.train_y = np.append(
            np.zeros((len(self.train_fear), 1)), 
            np.ones((len(self.train_sadness), 1)),
            axis=0)

        self.train_y = np.append(self.train_y, np.full((len(self.train_anger), 1), 2,), axis=0)
        self.train_y = np.append(self.train_y, np.full((len(self.train_love), 1), 3,), axis=0)
        self.train_y = np.append(self.train_y, np.full((len(self.train_joy), 1), 4,), axis=0)
        self.train_y = np.append(self.train_y, np.full((len(self.train_surprise), 1), 5,), axis=0)

        self.test_y = np.append(
            np.zeros((len(self.test_fear), 1)), 
            np.ones((len(self.test_sadness), 1)),
            axis=0)

        self.test_y = np.append(self.test_y, np.full((len(self.test_anger), 1), 2,), axis=0)
        self.test_y = np.append(self.test_y, np.full((len(self.test_love), 1), 3,), axis=0)
        self.test_y = np.append(self.test_y, np.full((len(self.test_joy), 1), 4,), axis=0)
        self.test_y = np.append(self.test_y, np.full((len(self.test_surprise), 1), 5,), axis=0)

        self.labels = ('fear', 'sadness', 'anger', 'love', 'joy', 'surprise')

        self.word_frequencies = {}
        self.predictive_model = None

        for label in self.labels:
            self.word_frequencies[label] = {}
        
        self.accuracy = 0

    def _process_text(self, text) -> list:
        # Tokenize the sentence or split it into words.
        tokenized = word_tokenize(text)

        stopwords_eng = stopwords.words("english")

        # Remove texts that are stopwords and punctuation.
        processed_text = []

        for word in tokenized:
            if word not in stopwords_eng and word not in string.punctuation:
                processed_text.append(word)
        
        # Stemming 
        """
        stemmer = PorterStemmer()

        stemmed = []

        for word in processed_text:
            stemmed.append(stemmer.stem(word))
        """

        lemmatizer = WordNetLemmatizer()

        lemmatized = []

        for word in processed_text:
            lemmatized.append(lemmatizer.lemmatize(word))
        
        return lemmatized
    
    def _generate_word_frequencies(self):
        for label in self.labels:
            texts = self.text_data_train[label] + self.text_data_test[label]

            temp_words = []

            for text in texts:
                processed = self._process_text(text)

                for word in processed:
                    temp_words.append(word)
            
            for word in temp_words:
                if word not in self.word_frequencies[label]:
                    self.word_frequencies[label][word] = 1
                else:
                    self.word_frequencies[label][word] += 1
    
    def _engineer_features(self, text):
        processed = self._process_text(text)

        x = np.zeros((1, 7))

        x[0,0] = 1 # Bias term

        for word in processed:
            try:
                x[0,1] += self.word_frequencies['fear'][word]
            except:
                x[0,1] += 0

            try:
                x[0,2] += self.word_frequencies['sadness'][word]
            except:
                x[0,2] += 0

            try:
                x[0,3] += self.word_frequencies['anger'][word]
            except:
                x[0,3] += 0

            try:
                x[0,4] += self.word_frequencies['love'][word]
            except:
                x[0,4] += 0

            try:
                x[0,5] += self.word_frequencies['joy'][word]
            except:
                x[0,5] += 0

            try:
                x[0,6] += self.word_frequencies['surprise'][word]
            except:
                x[0,6] += 0
        
        assert(x.shape == (1, 7))

        return x

    def _prepare_train_features(self):
        train_data = self.train_fear + self.train_sadness + self.train_anger + self.train_love + self.train_joy + self.train_surprise

        X = np.zeros((len(train_data), len(self.labels) + 1))

        for i in range(len(train_data)):
            X[i, :] = self._engineer_features(train_data[i])

        return X
    
    def _prepare_test_features(self):
        test_data = self.test_fear + self.test_sadness + self.test_anger + self.test_love + self.test_joy + self.test_surprise

        X_test = np.zeros((len(test_data), len(self.labels) + 1))

        for i in range(len(test_data)):
            X_test[i, :] = self._engineer_features(test_data[i])
        
        return X_test
    
    def train_model(self):
        print("Training Model... Please wait.")
        self._generate_word_frequencies()

        X_train = self._prepare_train_features()
        X_test = self._prepare_test_features()

        
        lm = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=100)

        lm.fit(X_train, self.train_y.flatten())

        y_pred = lm.predict(X_test)

        from sklearn.metrics import accuracy_score

        #self.accuracy = lm.score(X_test, self.test_y.flatten())

        self.accuracy = accuracy_score(self.test_y, y_pred)

        print(f"Accuracy: {self.accuracy * 100: .0f}%")

        self.predictive_model = lm
        
        """
        from sklearn.linear_model import SGDClassifier
        from sklearn.pipeline import Pipeline
        from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
        from sklearn.metrics import accuracy_score

        sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
               ])
        
        sgd.fit(X_train, self.train_y)

        y_pred = sgd.predict(X_test)

        print(f"Accuracy: {accuracy_score(y_pred, self.test_y)}")
        """

    
    def predict(self, text):
        X = self._engineer_features(text)

        return self.predictive_model.predict(X), self.predictive_model.predict_proba(X)
    
    def save_model(self, filename):
        pickle.dump(self, open(filename, 'wb'))
        print(f"Model saved at {filename}.")