""" Assignment 2
"""
import abc
from collections import defaultdict 
import numpy as np


class EvaluatorFunction:
    """
    An Abstract Base Class for evaluating search results.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, hits, relevant):
        """
        Do not modify.
        Params:
          hits...A list of document ids returned by the search engine, sorted
                 in descending order of relevance.
          relevant...A list of document ids that are known to be
                     relevant. Order is insignificant.
        Returns:
          A float indicating the quality of the search results, higher is better.
        """
        return


class Precision(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute precision.

        >>> Precision().evaluate([1, 2, 3, 4], [2, 4])
        0.5
        """
        ###TODO
        tp = 0
        fp = 0
        for doc in hits:
            if doc in relevant:
                tp+= 1
            else:
                fp+= 1
        
        return tp / (tp + fp)
        pass

    def __repr__(self):
        return 'Precision'


class Recall(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute recall.

        >>> Recall().evaluate([1, 2, 3, 4], [2, 5])
        0.5
        """
        ###TODO
        tp = 0
        fp = 0
        for doc in hits:
            if doc in relevant:
                tp+= 1
                
        fn = len(relevant) - tp # in top K -> assume k to be 10
        
        return tp / (tp +fn)
        pass

    def __repr__(self):
        return 'Recall'


class F1(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute F1.

        >>> F1().evaluate([1, 2, 3, 4], [2, 5])  # doctest:+ELLIPSIS
        0.333...
        """
        ###TODO
        precision = Precision().evaluate(hits,relevant)
        recall = Recall().evaluate(hits,relevant)
        
        if recall + precision == 0:
            return 0
        else:
            return 2 * recall * precision / (recall + precision)
        pass

    def __repr__(self):
        return 'F1'


class MAP(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute Mean Average Precision.

        >>> MAP().evaluate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 4, 6, 11, 12, 13, 14, 15, 16, 17])
        0.2
        """
        ###TODO
        precision_recall_dict = defaultdict(lambda: [0,0])
        tp = 0 #true positive
        fp = 0 # false positive
        fn = 0 # false negative
        for i in hits:
            if i in relevant:
                tp+= 1
                fn = len(relevant) - tp
            else:
                fp+= 1
            
            precision = tp/(tp + fp)
            if (tp + fn) == 0:
                recall = 0
            else:
                recall = tp/(tp + fn)   
            precision_recall_dict[i] = [precision,recall] 
        
        values_list = list(precision_recall_dict.values())
        sum = values_list[0][0] # numerator of MAP
        for i in range(len(values_list) - 1):
            if values_list[i][1] != values_list[i+1][1]:
                sum = sum + values_list[i+1][0]
        
        return sum/10  # assume k to be 10
        pass

    def __repr__(self):
        return 'MAP'

