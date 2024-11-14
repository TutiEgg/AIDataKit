from tensorflow import keras
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Model
import keras
#from keras.constraints import non_neg


# @tf.keras.utils.register_keras_serializable(package='Custom', name='kl')
class kl_reg(tf.keras.regularizers.Regularizer):
    def __init__(self, p=0., b=1):
        self.p = p
        self.b = b

    def __call__(self, x):
        x = tf.nn.relu(x)
        x = x + 1e-7
        return self.b * tf.math.reduce_sum(
            self.p * tf.math.log(self.p / x) + (1 - self.p) * tf.math.log((1 - self.p) / (1 - x)))

    def get_config(self):
        return {'p': float(self.p)}


class Dense_Encoder(Model):
    def __init__(self):
        super(Dense_Encoder, self).__init__()

        self.dense1 = keras.layers.Dense(156)
        self.dense2 = keras.layers.Dense(64)
        self.dense3 = keras.layers.Dense(25, activation='relu')
        self.dense4 = keras.layers.Dense(10, activity_regularizer=kl_reg(p=0.05))

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.dense4(x)
        return x

    def model(self):
        x = keras.layers.Input(shape=(156))
        return Model(inputs=[x], outputs=self.call(x))


class Dense_Decoder(Model):
    def __init__(self):
        super(Dense_Decoder, self).__init__()

        self.dense1 = keras.layers.Dense(156, activation='sigmoid')
        self.dense2 = keras.layers.Dense(64)
        self.dense3 = keras.layers.Dense(25)

    def call(self, inputs):
        x = self.dense3(inputs)
        x = self.dense2(x)
        x = self.dense1(x)
        return x

    def model(self):
        x = keras.layers.Input(shape=(10))
        return Model(inputs=[x], outputs=self.call(x))


class Conv_Encoder(Model):
    def __init__(self):
        super(Conv_Encoder, self).__init__()

        self.dense1 = keras.layers.Dense(156)
        self.reshape = keras.layers.Reshape((156, 1))
        self.conv1 = keras.layers.Conv1D(16, 3)
        self.conv2 = keras.layers.Conv1D(8, 6)
        self.conv3 = keras.layers.Conv1D(1, 9)
        self.flatten = keras.layers.Flatten()
        self.dropout = keras.layers.Dropout(0.2)
        self.dense2 = keras.layers.Dense(75)
        self.dense3 = keras.layers.Dense(20, activation='sigmoid', kernel_regularizer=kl_reg(
            p=0.005))  # keras.regularizers.l2(l2=1e-4)) # kl_reg(p=0.05)) kernel_constraint=non_neg(),

    def call(self, inputs):
        # x = self.dense1(inputs)
        x = self.reshape(inputs)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.flatten(x)
        # x = self.dropout(x)
        # x = self.dense2(x)
        x = self.dense3(x)
        return x

    def model(self):
        x = keras.layers.Input(shape=(156))
        return Model(inputs=[x], outputs=self.call(x))


class Conv_Decoder(Model):
    def __init__(self):
        super(Conv_Decoder, self).__init__()

        self.dense0 = keras.layers.Dense(75)
        self.dense1 = keras.layers.Dense(141)
        # self.dense2 = keras.layers.Dense(152, activation='relu')
        self.reshape = keras.layers.Reshape((141, 1))
        self.deconv0 = keras.layers.Conv1DTranspose(8, 9)
        self.deconv1 = keras.layers.Conv1DTranspose(16, 6)
        self.deconv2 = keras.layers.Conv1DTranspose(1, 3)
        self.flatten = keras.layers.Flatten()
        self.dense4 = keras.layers.Dense(156)

    def call(self, inputs):
        # x = self.dense0(inputs)
        x = self.dense1(inputs)
        x = self.reshape(x)
        x = self.deconv0(x)
        x = self.deconv1(x)
        x = self.deconv2(x)
        x = self.flatten(x)
        x = self.dense4(x)
        return x

    def model(self):
        x = keras.layers.Input(shape=(20))
        return Model(inputs=[x], outputs=self.call(x))


class AE(Model):
    def __init__(self):
        super(AE, self).__init__()
        self.encoder = Conv_Encoder()
        self.decoder = Conv_Decoder()

    def call(self, inputs):
        x = self.encoder(inputs)
        x = self.decoder(x)
        return x


def main():
    o = np.ones((200, 156))
    o[0:100] = np.zeros((100, 156))

    o = (o + 1) * 5


    model = AE()
    model.compile(loss=keras.losses.MeanSquaredError(),
                  optimizer=keras.optimizers.Adam())  # keras.losses.KLDivergence()

    history = model.fit(o, o, batch_size=16, verbose=1, epochs=15)
    model.encoder.model().summary()
    model.decoder.model().summary()
    o2 = o[98:104]

    # predictions = model.predict(o2, batch_size=4)
    # print(predictions)
    pred = model.encoder.predict(o2)
    print(pred)
"""
    o3 = np.array((1, 0, 0, 0))[None, :]
    print('decoder')
    a = model.decoder.predict(o3)
    print(a)

    o3 = np.array((0, 0, 0, 1))[None, :]
    print('decoder')
    a = model.decoder.predict(o3)
    print(a)
"""

if __name__ == '__main__':
    main()

