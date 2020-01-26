import pandas as pd

#Custom transformer that breaks dates column into year, month and day into separate columns and
#converts certain features to binary 
class OwnTransformer:
   
    #Class constructor method that takes in a list of values as its argument
    def __init__(self, hashtag_just_sign=True, remove_stopwords=True):
        self._hashtag_just_sign = hashtag_just_sign
        self._remove_stopwords = remove_stopwords
    
    def fit(self, X, y=None):
        return self


    #Transformer method we wrote for this transformer 
    def transform(self, X , y = None ):
       #Depending on constructor argument break dates column into specified units
       #using the helper functions written above 
       
       #IN ANY CASE 
        #non alpabetical/ numerical
        dfc = X
        dfc = dfc.replace(to_replace =r'&amp;', value = '', regex = True)
        dfc = dfc.replace(to_replace =r'&gt;', value = '', regex = True)
        #hyperlinks
        dfc = dfc.replace(to_replace =r'http\S+', value = '', regex = True)
        #usernames
        dfc = dfc.replace(to_replace =r'@\S+', value = '', regex = True) 
        #remove retweet
        dfc = dfc.replace(to_replace ='RT :', value = '', regex = True) 
        dfc = dfc.replace(to_replace ='RT ', value = '', regex = True)


        #HASHTAG OPTIONAL REMOVE
        if(hashtag_just_sign == True):
            dfc = dfc.replace(to_replace ='#', value = '', regex = True) 
        else:
            dfc = dfc.replace(to_replace =r'#\S+', value = '', regex = True)

        #IN ANY CASE
        #remove punctation
        dfc = dfc.replace(to_replace ='[",:!?\\-]', value = ' ', regex = True)
        #4. Tokenize into words (all lower case)
        dfc.tweet_text = dfc.tweet_text.str.lower()
        #make sure no weird letters left

        #u = df.select_dtypes(object)
        dfc = dfc.apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))

        if(remove_stopwords == True):
            dfc = dfc.str.split() 
            eng_stopwords = set(stopwords.words("english"))
            dfc = dfc.apply(lambda x: [item for item in x if item not in eng_stopwords])
            #join the list items back to one string
            dfc = dfc.apply(lambda x: ' '.join(x))


        return dfc