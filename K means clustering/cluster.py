"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter
from collections import defaultdict
from collections import OrderedDict
import gzip
import math
import operator
import sys
import codecs
import numpy as np


class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector), rounded to 2 decimal places.
        See Log.txt for expected output.
        The order of operations is:
        1) initialize means
        2) Loop
          2a) compute_clusters
          2b) compute_means
          2c) print sizes and error
        """
        ###TODO
        self.mean_vectors = documents[0:self.k]
        
        self.mean_vector_product = []
        doc_id = 0
        self.vector_prod=defaultdict(lambda:0)
        self.documents=documents
        doc_id=0
        for doc in documents:
            sqr=0
            for term in doc:
                sqr += doc[term] ** 2
            self.vector_prod[doc_id]=sqr 
            doc_id+=1
        
        self.mean_vector_prod=[]
        for doc in self.mean_vectors:
            sqr=0
            for term in doc:
                sqr += doc[term]**2
            self.mean_vector_prod.append(sqr)    
               
        for i in range(iters):
            self.compute_clusters(documents)
            self.compute_means()
            print (self.cluster_length)
            print ("%.2f"%self.error(documents))
        pass

    def compute_means(self):
        """ Compute the mean vectors for each cluster (results stored in an
        instance variable of your choosing)."""
        ###TODO
        self.mean_vectors = []
        for key in range(self.k):
            counter_value = Counter()
            cluster_num = 0
            for document_id in self.clusters[key]:
                counter_value.update(self.documents[document_id])
                cluster_num += 1
            if cluster_num > 0:
                for doc in counter_value:
                    counter_value[doc] = float(counter_value[doc])/float(cluster_num)
            
            self.mean_vectors.append(counter_value)
            
            self.mean_vector_prod=[]
            for doc in self.mean_vectors:
                sqr=0
                for term in doc:
                    sqr += doc[term] ** 2
                self.mean_vector_prod.append(sqr)                                
        pass

    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable of your choosing). """
        ###TODO
        self.clusters=defaultdict(lambda:[])
        distance_dict = defaultdict(lambda:0)
        doc_id=0
        for doc in documents:
            for i in range(self.k):
                distance=self.distance(doc,self.mean_vectors[i],self.mean_vector_prod[i]+self.vector_prod[doc_id])
                if (i==0):
                    min_index=i
                    min_dist=distance
                else:
                    if (distance<min_dist):
                        min_index=i
                        min_dist=distance
            self.clusters[min_index].append(doc_id)
            doc_id+=1
        cluster_length = []
        
        for i in self.clusters:
                cluster_length.append(len(self.clusters[i]))
                for doc_id in self.clusters[i]:
                    doc=documents[doc_id]
                    distance=self.distance(doc,self.mean_vectors[i],self.mean_vector_prod[i]+self.vector_prod[doc_id])
                    distance_dict[doc_id] = distance
        self.cluster_length = cluster_length
        self.distance_dict = distance_dict
        pass

    def sqnorm(self, d):
        """ Return the vector length of a dictionary d, defined as the sum of
        the squared values in this dict. """
        ###TODO
        return float(sum([list(d.values())[i] ** 2 for i in range(0, len(list(d.values())))]))
        pass

    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
        ###TODO
        prod = 0
        for term in doc:
            prod += doc[term]*mean[term]
        return math.sqrt(mean_norm - 2.0 * prod)
        pass

    def error(self, documents):
        """ Return the error of the current clustering, defined as the total
        Euclidean distance between each document and its assigned mean vector."""
        ###TODO
        error=0
        self.cluster_doc_tuple=defaultdict(list)
        for cluster in self.clusters:
            for doc_id in self.clusters[cluster]:
                doc=documents[doc_id]
                distance=self.distance(doc,self.mean_vectors[cluster],self.mean_vector_prod[cluster]+self.vector_prod[doc_id])
                error+= distance
                self.cluster_doc_tuple[cluster].append((doc,distance))
        return error
        pass

    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster. These are the
        documents that are the closest to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (sorted alphabetically).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
        ###TODO
         
        if sys.stdout.encoding != 'cp850':
              sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'strict')

        for i in self.clusters:
            print ("CLUSTER %d" %i)
            top_n_docs=sorted(self.cluster_doc_tuple[i],key=operator.itemgetter(1))
            k=0
            j=0
            while (j<n and k<len(top_n_docs)):
                if(len(top_n_docs[k][0])>3):
                    print(r' '.join(top_n_docs[k][0].keys()).encode('cp850', errors='replace').decode('cp850'))
                    j+=1
                k+=1
        pass


def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    ###TODO
    counter_list = []
    counts = defaultdict(lambda:0)
    for document in docs:
        for key in document.keys():
            if document.get(key):
                counts[key] += 1 
                                  
    for document in docs:
        pruned_doc = defaultdict(lambda:0)
        for key in document.keys():
            if counts[key] >= min_df:
                pruned_doc[key] = document[key]
                
        if len(pruned_doc) > 0:
            counts_key = Counter(pruned_doc)
            counter_list.append(counts_key)
        
    return counter_list   
    pass

def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with gzip.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles


def main():
    profiles = read_profiles('profiles.txt.gz')
    print('read', len(profiles), 'profiles.')
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()