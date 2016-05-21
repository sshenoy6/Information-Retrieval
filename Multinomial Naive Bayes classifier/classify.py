"""
Assignment 3. Implement a Multinomial Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

from collections import defaultdict
from collections import Counter
import glob
import math
import os



class Document(object):
    """ A Document. Do not modify.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename=None, label=None, tokens=None):
        """ Initialize a document either from a file, in which case the label
        comes from the file name, or from specified label and tokens, but not
        both.
        """
        if label: # specify from label/tokens, for testing.
            self.label = label
            self.tokens = tokens
        else: # specify from file.
            self.filename = filename
            self.label = 'spam' if 'spmsg' in filename else 'ham'
            self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):
    
    def __init__(self, counters={}, prior=defaultdict(float), condprob_spam=defaultdict(lambda:0),condprob_ham=defaultdict(lambda:0), V=[],classWiseTxt=defaultdict(lambda:[])):
        self.counters = counters
        self.prior = prior
        self.condprob_spam = condprob_spam
        self.condprob_ham = condprob_ham
        self.V = V
        self.classWiseTxt = classWiseTxt
        
    def get_word_probability(self, label, term):
        """
        Return Pr(term|label). This is only valid after .train has been called.

        Params:
          label: class label.
          term: the term
        Returns:
          A float representing the probability of this term for the specified class.

        >>> docs = [Document(label='spam', tokens=['a', 'b']), Document(label='spam', tokens=['b', 'c']), Document(label='ham', tokens=['c', 'd'])]
        >>> nb = NaiveBayes()
        >>> nb.train(docs)
        >>> nb.get_word_probability('spam', 'a')
        0.25
        >>> nb.get_word_probability('spam', 'b')
        0.375
        """
        ###TODO
        if self.docs is None: # if train function is not called exit the function
            return
        
        term_freq = defaultdict(lambda:0)
        counter = defaultdict(lambda:{})
        term_list = []
        for i,x in enumerate(self.docs): 
            if x.label == self.docs[i-1].label:
                term_list = x.tokens + self.docs[i-1].tokens
                term_freq[x.label] = term_list
            else:
                if x.label not in term_freq.keys():
                    term_freq[x.label] = x.tokens
                    
        total = 0;
        for labels in term_freq.keys():
            counter[labels] = Counter(term_freq[labels])
        
        self.counters = counter
        
        counter_label= counter[label]
        
        for i in counter_label.keys():
            total = total + counter_label[i]
        
        return ((counter_label[term]+1)/(len(term_freq[label]) + total)) 
        pass

    def get_top_words(self, label, n):
        """ Return the top n words for the specified class, using the odds ratio.
        The score for term t in class c is: p(t|c) / p(t|c'), where c'!=c.

        Params:
          labels...Class label.
          n........Number of values to return.
        Returns:
          A list of (float, string) tuples, where each float is the odds ratio
          defined above, and the string is the corresponding term.  This list
          should be sorted in descending order of odds ratio.

        >>> docs = [Document(label='spam', tokens=['a', 'b']), Document(label='spam', tokens=['b', 'c']), Document(label='ham', tokens=['c', 'd'])]
        >>> nb = NaiveBayes()
        >>> nb.train(docs)
        >>> nb.get_top_words('spam', 2)
        [(2.25, 'b'), (1.5, 'a')]
        """
        ###TODO
        odds_ratio = []
        condprobprime = defaultdict(lambda:1)
        odds_ratio_denominator = 1
        for labels in self.classWiseTxt.keys():
            if labels != label:
                label_prime = labels
        
        if label_prime == "ham":
            condprobprime = self.condprob_ham
            condprob = self.condprob_spam
        else:
            condprobprime = self.condprob_spam
            condprob = self.condprob_ham
        
        for t in self.classWiseTxt[label]:
            odds_ratio.append((float(condprob[t]/condprobprime[t]),t))
        
        odds_ratio = list(set(odds_ratio))
        
        odds_ratio = sorted(odds_ratio,key=lambda x: x[0],reverse=True) 
        return odds_ratio[:n]
        pass

    def train(self, documents):
        """
        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your
        book. Store these as instance variables, to be used by the classify
        method subsequently.
        Params:
          documents...A list of training Documents.
        Returns:
          Nothing.
        """
        ###TODO
        self.docs = documents
        V = []
        counter = defaultdict(lambda:{})
        N = defaultdict(lambda:0)
        sum_to_terms = defaultdict(lambda:0)
        textc_spam = []
        textc_ham = []
        condprob_spam = defaultdict(lambda:0)
        condprob_ham = defaultdict(lambda:0)
        smoothing_factor = 1
        for x in documents:
            if x.label == 'spam':
                N["spam"] += 1
                textc_spam += x.tokens
            elif x.label == "ham":
                N["ham"] += 1
                textc_ham += x.tokens
            for token in x.tokens:
                self.V.append(token)
        
        C = ["spam","ham"]
        self.V = list(set(self.V)) # set the vocabulary
        
        total = 0;
        
        for label in C:
            
            self.Nc = N[label]
            self.prior[label] = self.Nc/len(documents) # set the prior
            if label == "spam":
                text_c = textc_spam
            else:
                text_c = textc_ham
                
            counter[label] = Counter(text_c)
            
            for token in set(text_c):
                sum_to_terms[label] += counter[label][token] # calculate the denominator of conditional probability calculation
            sum_to_terms[label]+= len(self.V)
          
        Tct_spam = Counter(textc_spam) # calculate the Tct value- term frequency
        Tct_ham = Counter(textc_ham)
        
        for t in self.V: #set the conditional probability
            self.condprob_spam[t] = float (Tct_spam[t] + smoothing_factor) / float (sum_to_terms["spam"])
            self.condprob_ham[t] = float (Tct_ham[t] + smoothing_factor) / float (sum_to_terms["ham"])
        
        self.counters = counter
        
        #set the instance variables for further use -classWiseTxt is used in get_top_words to find top k words
        classwiseTxt = defaultdict(lambda:[])
        classwiseTxt["spam"] = textc_spam
        classwiseTxt["ham"] = textc_ham
        self.classWiseTxt = classwiseTxt
        pass

    def classify(self, documents):
        """ Return a list of strings, either 'spam' or 'ham', for each document.
        Params:
          documents....A list of Document objects to be classified.
        Returns:
          A list of label strings corresponding to the predictions for each document.
        """
        ###TODO
        result = []
        score = defaultdict(float)
        #score is product of prior and each term's conditional probability- multiply as many times as occurence in the document
        for x in documents:
            for label in ["spam","ham"]:
                score[label] = math.log(self.prior[label],10)
            for t in list(set(x.tokens)):
                number_of_occurences =  x.tokens.count(t)
                if(self.condprob_spam[t] > 0 and self.condprob_ham[t] > 0):
                    score["spam"] += math.log(self.condprob_spam[t],10) * number_of_occurences
                    score["ham"] += math.log(self.condprob_ham[t],10) * number_of_occurences 
            value =  max(score.keys(), key=(lambda key:score[key])) #take the value of label based on maximum score i.e. the label will be the one for which score is higher.
            result.append(value) # append into the list the valid label
        
        return result
        pass

def evaluate(predictions, documents):
    """ Evaluate the accuracy of a set of predictions.
    Return a tuple of three values (X, Y, Z) where
    X = percent of documents classified correctly
    Y = number of ham documents incorrectly classified as spam
    X = number of spam documents incorrectly classified as ham

    Params:
      predictions....list of document labels predicted by a classifier.
      documents......list of Document objects, with known labels.
    Returns:
      Tuple of three floats, defined above.
    """
    ###TODO
    incorrect_spam = 0
    incorrect_ham = 0
    accurate_classification = 0
    for i in range(0,len(documents)):
        if documents[i].label == predictions[i]:
            accurate_classification += 1
        elif predictions[i] == "spam":
            incorrect_spam += 1
        elif predictions[i] == "ham":
            incorrect_ham += 1
    return ((accurate_classification/len(documents)),incorrect_spam,incorrect_ham)#return tuple of accuracy,incorrect spam count,incorrect ham count
    pass

def main():
    """ Do not modify. """
    if not os.path.exists('train'):  # download data
       from urllib.request import urlretrieve
       import tarfile
       urlretrieve('http://cs.iit.edu/~culotta/cs429/lingspam.tgz', 'lingspam.tgz')
       tar = tarfile.open('lingspam.tgz')
       tar.extractall()
       tar.close()
    train_docs = [Document(filename=f) for f in glob.glob("train/*.txt")]
    print('read', len(train_docs), 'training documents.')
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(filename=f) for f in glob.glob("test/*.txt")]
    print('read', len(test_docs), 'testing documents.')
    predictions = nb.classify(test_docs)
    results = evaluate(predictions, test_docs)
    print('accuracy=%.3f, %d false spam, %d missed spam' % (results[0], results[1], results[2]))
    print('top ham terms: %s' % ' '.join('%.2f/%s' % (v,t) for v, t in nb.get_top_words('ham', 10)))
    print('top spam terms: %s' % ' '.join('%.2f/%s' % (v,t) for v, t in nb.get_top_words('spam', 10)))

if __name__ == '__main__':
    main()
 