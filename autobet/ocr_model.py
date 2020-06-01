import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from autobet.constants import PLACE_BET_SCREEN_ODDS_WIDTH, PLACE_BET_SCREEN_ODDS_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT

SAVED_MODEL_PATH = 'trained_model/saved_ocr_model'
MAX_ODDS = 30
INPUT_SHAPE = (int(PLACE_BET_SCREEN_ODDS_HEIGHT * SCREEN_HEIGHT), int(PLACE_BET_SCREEN_ODDS_WIDTH * SCREEN_WIDTH), 1)

def new_model():
        # ~1.5 million parameters
        model = tf.keras.applications.MobileNetV2(
            include_top=True,
            weights=None,
            input_shape=INPUT_SHAPE,
            pooling=None,
            classes=MAX_ODDS,
        )

        model.compile(optimizer='adam',
                  loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
        return model

def load_model():
	m = new_model()
	m.load_weights(SAVED_MODEL_PATH)
	return m

def img_to_arr(img):
    return np.array(img) / 255

def parse(model, img):
	img_arr = np.expand_dims(img_to_arr(img), 0)
	pred = model.predict(img_arr)
	return np.argmax(pred) + 1

def parse_multiple(model, imgs):
    img_arrs = np.asarray([img_to_arr(img) for img in imgs])
    classes = model.predict_classes(img_arrs)
    return [i+1 for i in classes]
