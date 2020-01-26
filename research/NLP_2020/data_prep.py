import pandas as pd

class DataPreprocessing:

	def __init__(self):
		print("constructor working")

	def data_preprocessing():
		
			#print("Start dataset loading: ")
		    eq_pakistan_2013 = pd.read_csv('data/2013_pakistan_eq.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    eq_pakistan_2013['cat'] = 'eq'

		    eq_california_2014 = pd.read_csv('data/2014_california_eq.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    eq_california_2014['cat'] = 'eq'

		    eq_chile_2014 = pd.read_csv('data/2014_chile_eq_en.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    eq_chile_2014['cat'] = 'eq'

		    ebola_virus_2014 = pd.read_csv('data/2014_ebola_virus.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    ebola_virus_2014['cat'] = 'virus'

		    hurricane_odile_2014 = pd.read_csv('data/2014_hurricane_odile.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    hurricane_odile_2014['cat'] = 'storm'

		    flood_india_2014 = pd.read_csv('data/2014_india_floods.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    flood_india_2014['cat'] = 'flood'

		    middle_east_respiratory_2014 = pd.read_csv('data/2014_mers_cf_labels.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    middle_east_respiratory_2014['cat'] = 'virus'

		    flood_pakistan_2014 = pd.read_csv('data/2014_pakistan_floods_cf_labels.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    flood_pakistan_2014['cat'] = 'flood'

		    typhoon_philippines_2014 = pd.read_csv('data/2014_typhoon_hagupit_cf_labels.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    typhoon_philippines_2014['cat']='storm'

		    cyclone_pam_2015 = pd.read_csv('data/2015_cyclone_pam_cf_labels.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    cyclone_pam_2015['cat'] = 'storm'

		    eq_nepal_2015 = pd.read_csv('data/2015_nepal_eq_cf_labels.csv', skip_blank_lines=True, encoding = "ISO-8859-1")
		    eq_nepal_2015['cat'] = 'eq'
		    
		    #make it one dataframe
		    df = pd.concat([cyclone_pam_2015, eq_nepal_2015, typhoon_philippines_2014, flood_pakistan_2014,
		                middle_east_respiratory_2014, flood_india_2014, hurricane_odile_2014, 
		                ebola_virus_2014, eq_chile_2014, eq_california_2014, eq_pakistan_2013])
		    
		    #drop unneccessary columns
		    df = df.drop(['_unit_id', '_golden', '_trusted_judgments',
		       '_last_judgment_at', 'choose_one_category:confidence', 'choose_one_category_gold',
		       'tweet_id'], axis=1)
		    
		    #drop nan values
		    df = df.dropna()
		    
		    #print("Datasets ready to use!")
		    
		    #print("Total Length of DataFrame is", len(df))
	    
	    	#print('\n Study the choose_one_category')
	    	#display(df.groupby(['choose_one_category']).count())
	    
		    #print("\n Study the cat")
		    #display(df.groupby(['cat']).count())
		    
		    return df