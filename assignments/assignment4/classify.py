"""
Assignment 4. Implement a Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

import glob


class Document(object):
    """ A Document. DO NOT MODIFY.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename):
        self.filename = filename
        self.label = 'spam' if 'spmsg' in filename else 'ham'
        self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):

    def train(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your book.
        """
        pass

    def classify(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Return a list of strings, either 'spam' or 'ham', for each document.
        documents....A list of Document objects to be classified.
        """
        pass


def evaluate(predictions, documents):
    """
    TODO: COMPLETE THIS METHOD.

    Evaluate the accuracy of a set of predictions.
    Print the following:
    accuracy=xxx, yyy false spam, zzz missed spam
    where
    xxx = percent of documents classified correctly
    yyy = number of ham documents incorrectly classified as spam
    zzz = number of spam documents incorrectly classified as ham

    See the provided log file for the expected output.

    predictions....list of document labels predicted by a classifier.
    documents......list of Document objects, with known labels.
    """


def main():
    """ DO NOT MODIFY. """
    train_docs = [Document(f) for f in glob.glob("train/*.txt")]
    print 'read', len(train_docs), 'training documents.'
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(f) for f in glob.glob("test/*.txt")]
    print 'read', len(test_docs), 'testing documents.'
    predictions = nb.classify(test_docs)
    evaluate(predictions, test_docs)

if __name__ == '__main__':
    main()
