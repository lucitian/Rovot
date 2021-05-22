import os, pickle, random
from text_processing import TextProcessingModel

def get_labels() -> set:
    for file in os.listdir('dataset'):
        with open(f"dataset/{file}", 'r', encoding="utf-8") as f:
            labels = []

            for line in f.readlines():
                labels.append(line.split(';')[1].strip())
            
            return tuple(set(labels))

def filter_data_label(dataset, label) -> tuple:
    with open(f"dataset/{dataset}", 'r', encoding="utf-8") as f:
            texts = []

            for line in f.readlines():
                if line.split(';')[1].strip() == label:
                    texts.append(line.split(';')[0].strip())
            
            return tuple(texts)

def get_text_data(dataset) -> tuple:
    with open(f"dataset/{dataset}", 'r', encoding="utf-8") as f:
            texts = []

            for line in f.readlines():
                texts.append(line.split(';')[0].strip())
            
            return tuple(texts)


if __name__ == "__main__":
    choice = int(input("1 = Retrain, 2 = Predict: "))
    
    lbl = ('fear', 'sadness', 'anger', 'love', 'joy', 'surprise')

    if choice == 1:
        data_train = {}
        data_test = {}

        for label in get_labels():
            train = filter_data_label('train.txt', label)
            test = filter_data_label('train.txt', label)
            val = filter_data_label('val.txt', label)

            random.shuffle(list(val))

            data_train[label] = train + val[0:len(val)//2]
            data_test[label] = test + val[len(val)//2:len(val)]
        
        model = TextProcessingModel(data_train, data_test)

        model._generate_word_frequencies()

        model.train_model()

        model.save_model('model.sav')
    else:
        model = pickle.load(open('models/model.sav', 'rb'))
        
        print(f"Accuracy: {model.accuracy * 100: .0f}%")

        while True:
            sentence = input(">> ")
            
            prediction = model.predict(sentence)

            confidence = prediction[1]

            print(f"Prediction: {lbl[int(prediction[0][0])]} | Confidence: {confidence[0][int(prediction[0][0])] * 100:.2f}%\n")