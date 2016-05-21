""" Assignment 2
"""
import abc
from collections import defaultdict
import math

import index


def idf(term, index):
    """ Compute the inverse document frequency of a term according to the
    index. IDF(T) = log10(N / df_t), where N is the total number of documents
    in the index and df_t is the total number of documents that contain term
    t.

    Params:
      terms....A string representing a term.
      index....A Index object.
    Returns:
      The idf value.
      
    >>> idx = index.Index(['a b c a', 'c d e', 'c e f'])
    >>> idf('a', idx) # doctest:+ELLIPSIS
    0.477...
    >>> idf('d', idx) # doctest:+ELLIPSIS
    0.477...
    >>> idf('e', idx) # doctest:+ELLIPSIS
    0.176...
    """
    ###TODO
    count = 0
    if term not in index.doc_freqs.keys():
        return 0
    else:
        return math.log(len(index.documents)/index.doc_freqs[term],10)
    pass


class ScoringFunction:
    """ An Abstract Base Class for ranking documents by relevance to a
    query. """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def score(self, query_vector, index):
        """
        Do not modify.

        Params:
          query_vector...dict mapping query term to weight.
          index..........Index object.
        """
        return


class RSV(ScoringFunction):
    """
    See lecture notes for definition of RSV.

    idf(a) = log10(3/1)
    idf(d) = log10(3/1)
    idf(e) = log10(3/2)
    >>> idx = index.Index(['a b c', 'c d e', 'c e f'])
    >>> rsv = RSV()
    >>> rsv.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.4771...
    """

    def score(self, query_vector, index):
        ###TODO
        rsv_dict = {}
        for i in range(len(index.documents)):
            sum = 0
            for term in query_vector:
                if term in index.documents[i]:
                    sum = sum + idf(term,index)
                
            rsv_dict[i+1] = sum
        
        return rsv_dict
        pass

    def __repr__(self):
        return 'RSV'


class BM25(ScoringFunction):
    """
    See lecture notes for definition of BM25.

    log10(3) * (2*2) / (1(.5 + .5(4/3.333)) + 2) = log10(3) * 4 / 3.1 = .6156...
    >>> idx = index.Index(['a a b c', 'c d e', 'c e f'])
    >>> bm = BM25(k=1, b=.5)
    >>> bm.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.61564032...
    """
    def __init__(self, k=1, b=.5):
        self.k = k
        self.b = b

    def score(self, query_vector, index):
        ###TODO
        bm25_score = defaultdict(lambda:0)
        sum = 0
        idf_value = index.query_to_vector(query_vector.keys())
        
        for j in range(len(index.documents)):
            sum = 0
            for term in query_vector:
                if term in index.documents[j]:
                    if idf_value[term] > 0:
                        tf_value = index.documents[j].count(term)
                        sum += idf_value[term] * (self.k+1) *(tf_value)/(self.k * ((1 - self.b) + self.b * len(index.documents[j]) / index.mean_doc_length) + tf_value)#(k + 1) * tf / (k * ((1 - b) + b * length / m_length) + tf)
                    
            bm25_score[j+1] = sum
            
        return dict(bm25_score)
        pass

    def __repr__(self):
        return 'BM25 k=%d b=%.2f' % (self.k, self.b)


class Cosine(ScoringFunction):
    """
    See lecture notes for definition of Cosine similarity.  Be sure to use the
    precomputed document norms (in index), rather than recomputing them for
    each query.

    >>> idx = index.Index(['a a b c', 'c d e', 'c e f'])
    >>> cos = Cosine()
    >>> cos.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.792857...
    """
    def score(self, query_vector, index):
        ###TODO
        query_vector_dict = defaultdict(lambda:0)
        score_list = defaultdict(lambda:0)
        for term,tf in query_vector.items():
            query_vector_dict[term] = tf
        val =0    
        for k in range(len(index.documents)):
            val = 0
            for term in query_vector.keys():
                if term in index.documents[k]:
                    tf_value = index.documents[k].count(term)
                    idf_value = len(index.documents)/index.doc_freqs[term]
                    val += ((1 + math.log(tf_value,10)) * math.log(idf_value,10) * query_vector[term])
            val = val/index.doc_norms[k+1]
            score_list[k+1] = val
        
        return score_list
        pass
    
    def __repr__(self):
        return 'Cosine'
