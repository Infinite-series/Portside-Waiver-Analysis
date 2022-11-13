import pandas as pd
perth_post = pd.read_csv(r'Data\australian_postcodes.csv')
perth_post = perth_post[perth_post['state']=='WA'].copy()
perth_post.to_csv('Perth_postcodes.csv')