"""VGG19 model for Keras.

# Reference

- [Very Deep Convolutional Networks for Large-Scale Image Recognition](
    https://arxiv.org/abs/1409.1556) (ICLR 2015)

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from .. import get_submodules_from_kwargs
from tensorflow.keras.applications import imagenet_utils 
from ..weights import load_model_weights


preprocess_input = imagenet_utils.preprocess_input
global backend, layers, models, keras_utils
backend, inp,layers, models, keras_utils=get_submodules_from_kwargs()

def VGG19(include_top=True,
          weights='imagenet',
          input_tensor=None,
          input_shape=None,
          pooling=None,
          classes=1000,
          **kwargs):
    """Instantiates the VGG19 architecture.

    Optionally loads weights pre-trained on ImageNet.
    Note that the data format convention used by the model is
    the one specified in your Keras config at `~/.keras/keras.json`.

    # Arguments
        include_top: whether to include the 3 fully-connected
            layers at the top of the network.
        weights: one of `None` (random initialization),
              'imagenet' (pre-training on ImageNet),
              or the path to the weights file to be loaded.
        input_tensor: optional Keras tensor
            (i.e. output of `layers.Input()`)
            to use as image input for the model.
        input_shape: optional shape tuple, only to be specified
            if `include_top` is False (otherwise the input shape
            has to be `(224, 224, 3)`
            (with `channels_last` data format)
            or `(3, 224, 224)` (with `channels_first` data format).
            It should have exactly 3 inputs channels,
            and width and height should be no smaller than 32.
            E.g. `(200, 200, 3)` would be one valid value.
        pooling: Optional pooling mode for feature extraction
            when `include_top` is `False`.
            - `None` means that the output of the model will be
                the 4D tensor output of the
                last convolutional block.
            - `avg` means that global average pooling
                will be applied to the output of the
                last convolutional block, and thus
                the output of the model will be a 2D tensor.
            - `max` means that global max pooling will
                be applied.
        classes: optional number of classes to classify images
            into, only to be specified if `include_top` is True, and
            if no `weights` argument is specified.

    # Returns
        A Keras model instance.

    # Raises
        ValueError: in case of invalid argument for `weights`,
            or invalid input shape.
    """

    if not (weights in {'imagenet', None} or os.path.exists(weights)):
        raise ValueError('The `weights` argument should be either '
                         '`None` (random initialization), `imagenet` '
                         '(pre-training on ImageNet), '
                         'or the path to the weights file to be loaded.')

    if weights == 'imagenet' and include_top and classes != 1000:
        raise ValueError('If using `weights` as `"imagenet"` with `include_top`'
                         ' as true, `classes` should be 1000')

    if input_tensor is None:
        img_input = layers.Input(shape=input_shape)
    else:
        if not backend.is_keras_tensor(input_tensor):
            img_input = layers.Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor
    # Block 1
    x = layers.Conv3D(64, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block1_conv1')(img_input)
    x = layers.Conv3D(64, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block1_conv2')(x)
    x = layers.MaxPooling3D((2, 2, 2), strides=(2, 2, 2), name='block1_pool')(x)

    # Block 2
    x = layers.Conv3D(128, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block2_conv1')(x)
    x = layers.Conv3D(128, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block2_conv2')(x)
    x = layers.MaxPooling3D((2, 2, 2), strides=(2, 2, 2), name='block2_pool')(x)

    # Block 3
    x = layers.Conv3D(256, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv1')(x)
    x = layers.Conv3D(256, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv2')(x)
    x = layers.Conv3D(256, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv3')(x)
    x = layers.Conv3D(256, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv4')(x)
    x = layers.MaxPooling3D((2, 2, 2), strides=(2, 2, 2), name='block3_pool')(x)

    # Block 4
    x = layers.Conv3D(512, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv1')(x)
    x = layers.Conv3D(512, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv2')(x)
    x = layers.Conv3D(512, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv3')(x)
    x = layers.Conv3D(512, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv4')(x)
    x = layers.MaxPooling3D((2, 2, 2), strides=(2, 2, 2), name='block4_pool')(x)

    # Block 5
    x = layers.Conv3D(512, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv1')(x)
    x = layers.Conv3D(512, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv2')(x)
    x = layers.Conv3D(512, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv3')(x)
    x = layers.Conv3D(512, (3, 3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv4')(x)
    x = layers.MaxPooling3D((2, 2, 2), strides=(2, 2, 2), name='block5_pool')(x)

    if include_top:
        # Classification block
        x = layers.Flatten(name='flatten')(x)
        x = layers.Dense(4096, activation='relu', name='fc1')(x)
        x = layers.Dense(4096, activation='relu', name='fc2')(x)
        x = layers.Dense(classes, activation='softmax', name='predictions')(x)
    else:
        if pooling == 'avg':
            x = layers.GlobalAveragePooling3D()(x)
        elif pooling == 'max':
            x = layers.GlobalMaxPooling3D()(x)

    # Ensure that the model takes into account
    # any potential predecessors of `input_tensor`.
    if input_tensor is not None:
        inputs = keras_utils.get_source_inputs(input_tensor)
    else:
        inputs = img_input
    # Create model.
    model = models.Model(inputs, x, name='vgg19')

    # Load weights.
    if weights:
        if type(weights) == str and os.path.exists(weights):
            model.load_weights(weights)
        else:
            load_model_weights(model, 'vgg19', weights, classes, include_top, **kwargs)

    return model
