
class Cleaner:

	def tweet_cleaner (dfc, hashtag_just_sign=True, remove_stopwords=True, tp_start=4, tp_end=10, cleaner='self_made'):  
	    list_before = list()
	    list_after = list()
	    
	    #check one example before cleaning
	    print("example before cleaning at positions ", tp_start, " to ", tp_end)
	    #for row in (dfc.iloc[tp_start:tp_end]).rows:
	    #   print(row['tweet_text'], '  ---  ',row['choose_one_category'])

	    for index, row in dfc.iloc[tp_start:tp_end].iterrows():
	        list_before.append([row['tweet_text'], row['choose_one_category']])
	        
	    if(cleaner=='off_the_shelf'):
	        print("Not defined pre-processor, can\'t be used")
	    
	    if(cleaner=='self_made'):
	        #IN ANY CASE 
	        #non alpabetical/ numerical
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
	        dfc['tweet_text'] = dfc['tweet_text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))

	        if(remove_stopwords == True):
	            dfc.tweet_text = dfc.tweet_text.str.split() 
	            eng_stopwords = set(stopwords.words("english"))
	            dfc['tweet_text'] = dfc['tweet_text'].apply(lambda x: [item for item in x if item not in eng_stopwords])
	            #join the list items back to one string
	            dfc['tweet_text'] = dfc['tweet_text'].apply(lambda x: ' '.join(x))

	    
	    
	    #print('example after cleaning at positions ', tp_start, ' to ', tp_end)
	    #print(dfc.iloc[tp_start:tp_end].tweet_text)
	    
	    for index, row in dfc.iloc[tp_start:tp_end].iterrows():
	        list_after.append([row['tweet_text'], row['choose_one_category']])
	    
	    
	    for num in range(0, len(list_before)):
	        print(list_before[num])
	        print(list_after[num])
	        print('--------------------------------------------------------------')
	    
	    return dfc
