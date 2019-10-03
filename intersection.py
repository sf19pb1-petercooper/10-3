"""
Outputs intersection of high frequency words in two different articles as determined by the
index.

Sample output:
Smart/Digital intersect in the following articles:

 1 article 1  
 2 article 10
 3 article 100
 4 article 101
 5 article 102
 6 article 103
 7 article 104
 8 article 105
 9 article 106
10 article 107
11 article 108
12 article 109
13 article 11
etc
"""
import collections
import requests
import pandas
import string
import matplotlib
import nltk
from nltk.corpus import stopwords 
import functools
import pprint

# from nltk.tokenize import word_tokenize - This looks to be a significantly 
# easier implementation of tokenizing words vs the string punctuation solution.

nltk.download('stopwords')
nltk.download('punkt')
  
stop_words = set(stopwords.words('english')) 
stop_words_additional = ("br","de","la")
for word in stop_words_additional:
    stop_words.add(word)
    print(stop_words)
#add words we don't want to analyze here (Html tags etc)
allWords = []

with open('/content/sample_data/cmt_media.csv', newline='',encoding='mac_roman') as csvfile:
     dataFrame = pandas.read_csv(csvfile)

#have a look at the data

#dataFrame
#print(dataFrame.body)
#print(type(dataFrame.body))


punctuation = string.punctuation + "\u201C\u201D"   #double quotes “ ”
articles = dataFrame.body.tolist()
print(articles)
print(type(articles))
keyed_articles = {}
keyed_set = set()
articleNumber = 1;
for article in articles[:]:
    articleWords = []
    for word in article.split():
        word = word.strip(punctuation)
        if word and word.lower() not in stop_words:
            # if word is not the empty string
            # make sure stop words are not counted
            allWords.append(word.lower())
            articleWords.append(word.lower())
    counter = collections.Counter(articleWords)
    keyed_articles.update( {articleNumber : articleWords} )
    keyed_articles.update( {"counts_"+str(articleNumber) : counter.most_common()} )
    keyed_set.add("article " + str(articleNumber))
    articleNumber+=1




#Counter is like a dict.  Keys are words, values are counts.
counter = collections.Counter(allWords)
listOfTuples = counter.most_common()
# print(counter)

list_of_set_article_numbers = []
article_combo = {}
#print(keyed_set)
for word, i in listOfTuples[1:4:2]:
    print(f"{i:2} {word}")
    for key in keyed_articles:
        if word in keyed_articles[key]:
            print(f"    article {key}")
            keyed_set.add("article " + str(key))
    print(keyed_set)
    list_of_set_article_numbers.append(keyed_set)
    keyed_set=set()
          
pprint.pprint(list_of_set_article_numbers, depth=10, indent=4)

def check_intersection():
    assert len(list_of_set_article_numbers) > 0
    intersection = list_of_set_article_numbers[0]
    for set_article in list_of_set_article_numbers[1:]:
        intersection &= set_article   #or intersection &= category
        print(type(set_article))
    for i, article_num in enumerate(sorted(intersection), start = 1):
        print(f"{i:2} {article_num}")
    
check_intersection()

# print()

# intersection = functools.reduce(lambda intersection, set_article: intersection & set_article, list_of_set_article_numbers)
    
# print(intersection)
#sys.exit(0)
