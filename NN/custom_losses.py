import tensorflow as tf


class kl_reg(tf.keras.regularizers.Regularizer):
    """ Kullback Leibler Divergenz

    Can be used as Regularizer. Similar to L2 norm.
    """
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

