import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from autobet.constants import PLACE_BET_SCREEN_ODDS_WIDTH, PLACE_BET_SCREEN_ODDS_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT

SAVED_MODEL_PATH = 'trained_model/saved_ocr_model'
MAX_ODDS = 30
INPUT_SHAPE = (int(PLACE_BET_SCREEN_ODDS_WIDTH * SCREEN_WIDTH), int(PLACE_BET_SCREEN_ODDS_HEIGHT * SCREEN_HEIGHT), 3)

def model():
	# ~1 million parameters
	model = Sequential()
	model.add(Conv2D(32, kernel_size=(3, 3),
	                 activation='relu',
	                 input_shape=INPUT_SHAPE))
	model.add(Conv2D(64, kernel_size=(2, 2),
	                 activation='relu'))
	model.add(Flatten())
	model.add(Dense(16, activation='relu'))
	model.add(Dense(32, activation='relu'))
	model.add(Dense(64, activation='relu'))
	model.add(Dense(MAX_ODDS, activation='softmax'))

	model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
	return model
