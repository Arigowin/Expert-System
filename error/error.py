
def error(code, message):
    # [retun, message, exit]
    errors = {-1: [-1, "Modify value already set" + message, False],
              -2: [0, "Modify value with lower priority" + message, False],
              -3: [-1, "Modify value with highter priority" + message, False],
              -4: [-1, "Modify value with same priority" + message, False],
              -5: [-1, "Inconsistency rule" + message, False],
              -6: [-1, tf.usage(message), True]}
