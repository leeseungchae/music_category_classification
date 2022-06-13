import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.utils import plot_model

X_train , X_test , Y_train , Y_test = np.load('./output/music_data_max_942_wordsize_33105.npy', allow_pickle=True)
print(X_train.shape , Y_train.shape)
print(X_test.shape , Y_test.shape)

model = Sequential()
model.add(Embedding(33105, 150, input_length=942))
model.add(Conv1D(32, kernel_size=5, padding = 'same', activation = 'relu')) # 빠르고 정확함 하지만 앞뒤 데이터가  정확해야함
model.add(MaxPooling1D(pool_size=1)) # Conv쓸때 들어간다고 함
model.add(LSTM(128, activation = 'tanh', return_sequences= True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation = 'tanh', return_sequences= True))
model.add(Dropout(0.3))
model.add(LSTM(164, activation = 'tanh', return_sequences= True))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dense(8, activation = 'softmax'))
model.summary()

model.compile(loss = 'categorical_crossentropy',
              optimizer = 'adam', metrics = ['accuracy'])

fit_hist = model.fit(X_train, Y_train, batch_size=30, epochs = 8 , validation_data=(X_test, Y_test))
model.save('news_category_classfication_model_{}.h5'.format(
    fit_hist.history['val_accuracy'][-1]))
plt.plot(fit_hist.history['accuracy'], label = 'accuracy')
plt.plot(fit_hist.history['val_accuracy'], label = 'val_accuracy')