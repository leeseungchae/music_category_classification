import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.keras.models import load_model

#designer

form_window = uic.loadUiType('./mainWidget.ui')[0]
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 20)
df = pd.read_csv('./output/music_data_coulmns.csv')
Y = df.genre

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.path = None
        self.setupUi(self)
        self.model = load_model('./output/music_category_classfication_model_0.4069400727748871.h5')

        self.btn_push.clicked.connect(self.predict_genre)

    def predict_genre(self):
        X = self.te_lylic.toPlainText()

        with open('./output/encoder.pickle', 'rb') as f:
            encoder = pickle.load(f)
        labeled_Y = encoder.transform(Y)


        with open('./output/music_token.pickle', 'rb') as f:
            token = pickle.load(f)
        tokened_X = token.texts_to_sequences([X])

        for i in range(len(tokened_X)):
            if len(tokened_X[i]) > 942:
                tokened_X[i] = tokened_X[i][:942]
        X_pad = pad_sequences(tokened_X, 942)


        label = encoder.classes_
        model = load_model('./output/music_category_classfication_model_0.4069400727748871.h5')

        preds = model.predict(X_pad)[0]
        preds = list(preds.round(2))
        label_temp = list(label)
        preds_temp = preds
        labels = []
        predicts = []
        total = 0

        while total < 0.7:
            labels.append(label_temp.pop(np.argmax(preds_temp)))
            predicts.append(preds_temp.pop(np.argmax(preds_temp)))
            total = total + predicts[-1]

        predicts = np.array(predicts)
        predicts = predicts.round(2)*100
        predicts = predicts.astype(np.int32)
        predicts = predicts.astype('str')

        if labels[0] == '포크 블루스':
            labels[0] = '발라드'
        print(labels)

        self.lbl_result.setText('/ '.join(labels))
        print(predicts)
        self.lbl_result_2.setText('/ '.join(predicts) + "%")

app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())