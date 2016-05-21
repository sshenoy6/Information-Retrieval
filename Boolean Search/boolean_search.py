""" Assignment 0

You will implement a simple in-memory boolean search engine over the jokes
from http://web.hawkesnest.net/~jthens/laffytaffy/.

The documents are read from documents.txt.
The queries to be processed are read from queries.txt.

Your search engine will only need to support AND queries. A multi-word query
is assumed to be an AND of the words. E.g., the query "why because" should be
processed as "why AND because."
"""
from collections import defaultdict
import re


def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Remove all punctuation and split on whitespace.
    Params:
      document...a string to be tokenized
    Returns:
      A list of strings, one per token.
    Here is a doctest:
    >>> tokenize("Hi  there. What's going on?")
    ['hi', 'there', 'what', 's', 'going', 'on']
    """
    ###TODO
    return list(re.sub('[^a-zA-Z]+', " ", document).lower().split()); """replace all those characters that are not alphabets by a space and split on the space."""
    pass


def create_index(tokens):
    """
    Create an inverted index given a list of document tokens. The index maps
    each unique word to a list of document ids, sorted in increasing order.
    Params:
      tokens...A list of lists of strings
    Returns:
      An inverted index. This is a dict where keys are words and values are
      lists of document indices, sorted in increasing order.
    Below is an example, where the first document contains the tokens 'a' and
    'b', and the second document contains the tokens 'a' and 'c'.
    >>> index = create_index([['a', 'b'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [0, 1]
    >>> index['b']
    [0]
    """
    ###TODO
    index = defaultdict(list)
    result = set();
    for i in tokens:
        for x in i:
            result.add(x); # result contains the unique set of keys

    for i,inner_list in enumerate(tokens):#iterate over outer list
        for j,token in enumerate(inner_list):#iterate over inner list
            for k in range(len(result)):#index for inner list element to be compared with key value in result
                if token == sorted(result)[k]:
                    index[token].append(i);#if match is found add the document ID
    return dict(index);
    pass


def intersect(list1, list2):
    """ Return the intersection of two posting lists. Use the optimize
    algorithm of Figure 1.6 of the MRS text. Your implementation should be
    linear in the sizes of list1 and list2. That is, you should only loop once
    through each list.
    Params:
      list1....A list of document indices, sorted in ascending order.
      list2....Another list of document indices, sorted in ascending order.
    Returns:
      The list of document ids that appear in both lists, sorted in ascending order.
    >>> intersect([1, 3, 5], [3, 4, 5, 10])
    [3, 5]
    >>> intersect([1, 2], [3, 4])
    []
    """
    ###TODO
    answer = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]: #if values beign compared are equal, add value to answer array and advance both pointers
            answer.append(list1[i]);
            i += 1
            j += 1
            continue
        elif list1[i] < list2[j]: #if value in list1 is less than value in list2,advance pointer to list1
            i += 1
        else:                    #if value in list1 is greater than value in list2,advance pointer to list2
            j += 1
    return answer
    pass


def sort_by_num_postings(words, index):
    """
    Sort the words in increasing order of the length of their postings list in
    index. You may use Python's builtin sorted method.
    Params:
      words....a list of strings.
      index....An inverted index; a dict mapping words to lists of document
      ids, sorted in ascending order.
    Returns:
      A list of words, sorted in ascending order by the number of document ids
      in the index.

    >>> sort_by_num_postings(['a', 'b', 'c'], {'a': [0, 1], 'b': [1, 2, 3], 'c': [4]})
    ['c', 'a', 'b']
    """
    ###TODO
    words = []
    for sorted_value in sorted(index, key=lambda sorted_value: len(index[sorted_value]), reverse=False):
        words.append(sorted_value)
    return words
    pass


def search(index, query):
    """ Return the document ids for documents matching the query. Assume that
    query is a single string, possibly containing multiple words. The steps
    are to:
    1. tokenize the query
    2. Sort the query words by the length of their postings list
    3. Intersect the postings list of each word in the query.

    If a query term is not in the index, then an empty list should be returned.

    Params:
      index...An inverted index (dict mapping words to document ids)
      query...A string that may contain multiple search terms. We assume the
      query is the AND of those terms by default.

    E.g., below we search for documents containing 'a' and 'b':
    >>> search({'a': [0, 1], 'b': [1, 2, 3], 'c': [4]}, 'a b')
    [1]
    """
    ###TODO
    document_ids = []
    tokens = tokenize(query)
    words = sort_by_num_postings(tokens,index)
    
    for i in tokens:
        if i not in words: # if token not in index then return empty list
            return document_ids
    
    if len(tokens) == 1: #handle the case where there is a single query word and intersection is not required
        document_ids = index[tokens[0]]
        return document_ids
    
    for j in range(len(tokens) - 1): #iterate over the tokens and intersect the postings lists   
        index[tokens[j+1]] = intersect(index[tokens[j]],index[tokens[j+1]])
        document_ids = index[tokens[j+1]]
        
    return document_ids
    pass


def main():
    """ Main method. You should not modify this. """
    documents = open('documents.txt').readlines()
    tokens = [tokenize(d) for d in documents]
    index = create_index(tokens)
    queries = open('queries.txt').readlines()
    for query in queries:
        results = search(index, query)
        print('\n\nQUERY:%s\nRESULTS:\n%s' % (query, '\n'.join(documents[r] for r in results)))


if __name__ == '__main__':
    main()
