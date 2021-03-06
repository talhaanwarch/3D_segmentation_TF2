import tensorflow.keras.applications as ka
from ..__version__ import __version__


def get_submodules_from_kwargss(kwargs):
    backend = kwargs.get('backend', ka._KERAS_BACKEND)
    layers = kwargs.get('layers', ka._KERAS_LAYERS)
    models = kwargs.get('models', ka._KERAS_MODELS)
    utils = kwargs.get('utils', ka._KERAS_UTILS)
    return backend, layers, models, utils
def get_submodules_from_kwargs(kwargs):

    return None, None, None, None