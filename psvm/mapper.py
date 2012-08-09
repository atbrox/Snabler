import base64
import cPickle as pickle
from mrjob.job import MRJob
import numpy as np

def numerify_feature(feature):
    if feature == '?':
        feature = 0.0
    return float(feature)

def extract_features(array):
    features = array[1:-1]
    return [numerify_feature(f) for f in features]

def extract_category(array, neg_category, pos_category):
    category = array[-1].strip()
    return -1.0 if category == neg_category else 1.0

class MRsvm(MRJob):
    def __init__(self, *args, **kwargs):
        super(MRsvm, self).__init__(*args, **kwargs)

    def transform_input(self, _, value):
        array = value.split(',')
        features = extract_features(array)
        category = extract_category(array, neg_category = '4', pos_category = '2')
        yield(category, features)

    def mapper(self, key, value):
        num_training_features = len(value)

        A = np.matrix(
            np.reshape(np.array(value),
                       (1, num_training_features)))
        D = np.diag([key])
        e = np.matrix(np.ones(len(A)).reshape(len(A), 1))
        E = np.matrix(np.append(A, -e, axis = 1))

        value = base64.b64encode(pickle.dumps((E.T*E, E.T*D*e)))
        yield("outputkey", value)

    def reducer(self, key, values):
        mu = 0.1

        sum_ETE = None
        sum_ETDe = None

        for value in values:
            ETE, ETDe = pickle.loads(base64.b64decode(value))

            if sum_ETE == None:
                sum_ETE = np.matrix(np.eye(ETE.shape[1])/mu)
            sum_ETE += ETE
            
            if sum_ETDe == None:
                sum_ETDe = ETDe
            else:
                sum_ETDe += ETDe


        result = sum_ETE.I * sum_ETDe
        yield(key, str(result.tolist()))

    def steps(self):
        return [self.mr(mapper = self.transform_input),
                self.mr(mapper = self.mapper,
                        reducer = self.reducer)]


if __name__ == '__main__':
    MRsvm.run()

