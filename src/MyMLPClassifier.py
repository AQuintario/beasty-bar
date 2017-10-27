import time
import pickle
from sklearn.neural_network import MLPClassifier


class MyMLPClassifier(MLPClassifier):
    def __init__(self, filename, *args, **kwargs):
        super(MyMLPClassifier, self).__init__(*args, **kwargs)
        self.filename = filename
        try:
            self.load()
        except FileNotFoundError:
            self.nn_exists = False
            print('Creating new Neural Network')

    def load(self):
        with open(self.filename, 'rb') as f:
            tmp_dict = pickle.load(f)
        self.__dict__.update(tmp_dict)
        self.nn_exists = True
        print('Loading trained model from ' + self.filename)

    def save(self):
        if self.filename == '':
            current_time = time.strftime('%Y%m%d_%H%M')
            hls = self.hidden_layer_sizes
            hls = str(hls[0]) if len(hls) == 1 else str(hls[0]) + 'x' + str(hls[1])
            self.filename = 'log/trained_nn_' + current_time + '_' + hls + '_hls.pkl'
        with open(self.filename, 'wb') as f:
            pickle.dump(self.__dict__, f, 2)
        print('Log saved to', self.filename)

   