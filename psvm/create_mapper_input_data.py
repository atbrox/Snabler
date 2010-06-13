import cPickle as pickle

def numerifyFeature(feature):
    if feature == "?":
        feature = 0.0
    return float(feature)

def extractFeatures(example):
    # remove running id and category
    features = example.split(",")[1:-1]
    return [numerifyFeature(f) for f in features]

def extractCategory(example, negCategory, posCategory):
    category = example.split(",")[-1].strip()
    if category == negCategory:
        return -1.0
    return 1.0

def maprunner(incsize=1):
    # read incsize number of examples from iris
    breastcancerfile = file('testdata/breastcancerwisconsin.data')
    # just some mapping to -1 and +1
    negative = [4]
    positive = [2]

    reduceinput = {}
    
    for example in breastcancerfile:
        # skip first and last feature (id + class)
        features = extractFeatures(example)
        category = extractCategory(example, negCategory="4", posCategory="2")
        print "%s\t%s" % (str(category),",".join([str(f) for f in features]))

if __name__ == "__main__":
    maprunner()
