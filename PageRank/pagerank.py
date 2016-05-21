""" Assignment 6: PageRank. """
from bs4 import BeautifulSoup
from sortedcontainers import SortedList, SortedSet, SortedDict
from collections import Counter
import glob
import os
import requests
from collections import defaultdict
import operator
import re
import urllib


def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    """ Return a dictionary mapping each url to its PageRank.
    The formula is R(u) = (1/N)(1-b) + b * (sum_{w in B_u} R(w) / (|F_w|)

    Initialize all scores to 1.0.

    Params:
      urls.......SortedList of urls (names)
      inlinks....SortedDict mapping url to list of in links (backlinks)
      outlinks...Sorteddict mapping url to list of outlinks
    Returns:
      A SortedDict mapping url to its final PageRank value (float)

    >>> urls = SortedList(['a', 'b', 'c'])
    >>> inlinks = SortedDict({'a': ['c'], 'b': set(['a']), 'c': set(['a', 'b'])})
    >>> outlinks = SortedDict({'a': ['b', 'c'], 'b': set(['c']), 'c': set(['a'])})
    >>> sorted(compute_pagerank(urls, inlinks, outlinks, b=.5, iters=0).items())
    [('a', 1.0), ('b', 1.0), ('c', 1.0)]
    >>> iter1 = compute_pagerank(urls, inlinks, outlinks, b=.5, iters=1)
    >>> iter1['a']  # doctest:+ELLIPSIS
    0.6666...
    >>> iter1['b']  # doctest:+ELLIPSIS
    0.333...
    """
    ###TODO
    final_rank = defaultdict(lambda:1.0)
    f_w = defaultdict(lambda:0.0)
    #initialise the value of pageranks to 1.0
    for url in urls:
        final_rank[url] = 1.0
    
    for outlink in outlinks:
        f_w[outlink] = len(outlinks[outlink])
    
    N = len(urls)
    for i in range(iters):
        for url in urls:
            summation = 0
            for inlink in inlinks[url]:
                summation += 1.0 * final_rank[inlink]/f_w[inlink]
            
            final_rank[url] = (1/N) * (1-b) + b * (summation)
        
    return SortedDict(dict(final_rank))
    pass


def get_top_pageranks(inlinks, outlinks, b, n=50, iters=20):
    """
    >>> inlinks = SortedDict({'a': ['c'], 'b': set(['a']), 'c': set(['a', 'b'])})
    >>> outlinks = SortedDict({'a': ['b', 'c'], 'b': set(['c']), 'c': set(['a'])})
    >>> res = get_top_pageranks(inlinks, outlinks, b=.5, n=2, iters=1)
    >>> len(res)
    2
    >>> res[0]  # doctest:+ELLIPSIS
    ('a', 0.6666...
    """
    ###TODO
    urls = SortedList(dict(inlinks).keys())
    page_ranks = compute_pagerank(urls, inlinks, outlinks, b, iters)
    top_page_ranks = sorted(page_ranks.items(),key=operator.itemgetter(1),reverse = True)[:n]
    return top_page_ranks
    pass


def read_names(path):
    """ Do not mofify. Returns a SortedSet of names in the data directory. """
    return SortedSet([os.path.basename(n) for n in glob.glob(path + os.sep + '*')])


def get_links(names, html):
    """
    Return a SortedSet of computer scientist names that are linked from this
    html page. The return set is restricted to those people in the provided
    set of names.  The returned list should contain no duplicates.

    Params:
      names....A SortedSet of computer scientist names, one per filename.
      html.....A string representing one html page.
    Returns:
      A SortedSet of names of linked computer scientists on this html page, restricted to
      elements of the set of provided names.

    >>> get_links({'Gerald_Jay_Sussman'},
    ... '''<a href="/wiki/Gerald_Jay_Sussman">xx</a> and <a href="/wiki/Not_Me">xx</a>''')
    SortedSet(['Gerald_Jay_Sussman'], key=None, load=1000)
    """
    ###TODO
    result = SortedSet()
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', html) # to find href values within anchor tag
    urls = list(set(urls))
    for url in urls:
        for name in names:
            if name == "Guy_L._Steele,_Jr":
                names.remove(name)
                name = "Guy_L._Steele,_Jr." #explicitly append the '.' -> problem while extracting file in Windows OS
                names.add(name)
                
            
            if url == "/wiki/"+name: #find url with desired suffix
                result.add(name)
            else:
                continue
    
    return result
    pass

def read_links(path):
    """
    Read the html pages in the data folder. Create and return two SortedDicts:
      inlinks: maps from a name to a SortedSet of names that link to it.
      outlinks: maps from a name to a SortedSet of names that it links to.
    For example:
    inlinks['Ada_Lovelace'] = SortedSet(['Charles_Babbage', 'David_Gelernter'], key=None, load=1000)
    outlinks['Ada_Lovelace'] = SortedSet(['Alan_Turing', 'Charles_Babbage'], key=None, load=1000)

    You should use the read_names and get_links function above.

    Params:
      path...the name of the data directory ('data')
    Returns:
      A (inlinks, outlinks) tuple, as defined above (i.e., two SortedDicts)
    """
    ###TODO
    inlinks = defaultdict(lambda:SortedSet())
    outlinks = defaultdict(lambda:SortedSet())
    #fp = open("results.txt",'w')
    sorted_set_names = SortedSet()
    html_link = ""
    for names in read_names(path):
        if names == "Guy_L._Steele,_Jr":
                names = "Guy_L._Steele,_Jr." #explicitly append the '.' -> problem while extracting file in Windows OS
        
        sorted_set_names.add(names)
        inlinks[names] = SortedSet()
       
    for names in sorted_set_names:
        html_link = ""
        links = []
        file_resp = open(path+"/"+names,'r',encoding = "utf-8")
        soup = BeautifulSoup(file_resp.read(),"html.parser")
        links = soup.findAll('a',href=re.compile("/wiki/"))  #filter url by /wiki/ href value to reduce number of links
        
        for link in links:
            link = str(link)
            html_link += link
            html_link += " and "
        outlinks[names] = get_links(sorted_set_names,html_link)
        #fp.write("Found %s links for %s\n"%(len(outlinks[names]),names))
        
        
        if names in outlinks[names]:
            outlinks[names].remove(names) #remove self reference
        
        
        sorted_inlink_names = SortedSet()
        
        #from outlinks calculate inlinks
        for link in outlinks[names]:
            sorted_inlink_names.add(names)
            inlinks[link].update(sorted_inlink_names)
            
    #print("Outlinks for Lovelace are %s"%outlinks['Ada_Lovelace'])
    #print ("Inlinks are %s"%inlinks['Ada_Lovelace'])
    #fp.write("Outlinks are %s"%dict(outlinks))
    #fp.write("Inlinks are %s"%dict(inlinks))
    #fp.close()
    return (SortedDict(dict(inlinks)),SortedDict(dict(outlinks)))
    pass


def print_top_pageranks(topn):
    """ Do not modify. Print a list of name/pagerank tuples. """
    print('Top page ranks:\n%s' % ('\n'.join('%s\t%.5f' % (u, v) for u, v in topn)))


def main():
    """ Do not modify. """
    if not os.path.exists('data'):  # download and unzip data
       from urllib.request import urlretrieve
       import tarfile
       urlretrieve('http://cs.iit.edu/~culotta/cs429/pagerank.tgz', 'pagerank.tgz')
       tar = tarfile.open('pagerank.tgz')
       tar.extractall()
       tar.close()

    inlinks, outlinks = read_links('data')
    print('read %d people with a total of %d inlinks' % (len(inlinks), sum(len(v) for v in inlinks.values())))
    print('read %d people with a total of %d outlinks' % (len(outlinks), sum(len(v) for v in outlinks.values())))
    topn = get_top_pageranks(inlinks, outlinks, b=.8, n=20, iters=10)
    print_top_pageranks(topn)


if __name__ == '__main__':
    main()
