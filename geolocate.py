import pandas as pd
from geopy.geocoders import GoogleV3
geolocator = GoogleV3(api_key='AIzaSyDXJrPyEOm8s20hy8jpMADHb2jOuOD2TbA')

combined_gyms = pd.read_csv(r'Data\combined_gyms.csv')

def extract_clean_address(address):
    try:
        location = geolocator.geocode(address)
        return location.address
    except:
        return ''
    
combined_gyms['Clean_Full_Address'] = combined_gyms.apply(lambda x: extract_clean_address(x['Full_Address']) , axis =1  )

# # saves geolocated dataset to csv so we do not need to run google api again. 
combined_gyms.to_csv('Cleaned_and_combined.csv')