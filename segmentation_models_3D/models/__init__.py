from tensorflow import keras


def get_submodules_from_kwargs():
    backend = keras.backend
    inp= keras
    layers = keras.layers
    models = keras
    utils = keras.utils
    return backend,inp, layers, models, utils