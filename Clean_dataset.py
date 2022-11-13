# Imports:
import datetime as dt
import re
import numpy as np
import pandas as pd
pd.options.display.max_columns = None  # lets us view all columns

combined_gyms_sorted = pd.read_csv(r'Data\Cleaned_and_combined.csv')

# removing null values
combined_gyms_sorted = combined_gyms_sorted[combined_gyms_sorted['Clean_Full_Address'].notnull(
)]

# Extracting postcode from our cleaned_full_address column
expression = r"([6][0-9]{3})"
sorted_dataset = combined_gyms_sorted[combined_gyms_sorted['Clean_Full_Address'].str.contains(
    expression)].copy()
sorted_dataset['Postcode_updated'] = sorted_dataset['Clean_Full_Address'].str.extract(
    expression)
# Checking if postcode data is consistent ie: no letters


# Extracting suburb from our cleaned_full_address column
expression_2 = r"((?<=,\s)\w*\s?\w+(?=\sWA))"
sorted_dataset = sorted_dataset[sorted_dataset['Clean_Full_Address'].str.contains(
    expression_2)].copy()
sorted_dataset['Suburb_updated'] = sorted_dataset['Clean_Full_Address'].str.extract(
    expression_2)
sorted_dataset['Suburb_updated'] = sorted_dataset['Suburb_updated'].str.lower(
).str.capitalize()  # Ensuring data is homogeneous

# importing dataset that contains postcodes,suburb, and lat/long data.
perth_post = pd.read_csv(
    r"Data\Perth Postcodes.csv")
perth_post.head()

# creating new smaller dataframe for merge.
perth_post_updated = perth_post[[
    'postcode', 'locality', 'Lat_precise', 'Long_precise']].copy()
perth_post_updated['locality'] = perth_post_updated['locality'].str.lower(
).str.capitalize()  # Ensuring data is homogeneous
perth_post_updated['postcode'] = perth_post_updated['postcode'].astype('str')

sorted_post = sorted_dataset.merge(perth_post_updated, left_on=[
                                   'Postcode_updated', 'Suburb_updated'], right_on=['postcode', 'locality'])

# dropping postcode and locality column, as they are identical to existing Postcode_updated, and Suburb_updated column
# Also cleaning up columns to prep for analysis.
sorted_post_cleaned = sorted_post[['Date of Birth', 'Sex', 'Gym',
                                   'Clean_Full_Address', 'Postcode_updated', 'Suburb_updated',
                                   'Lat_precise', 'Long_precise']].copy()


sorted_post_cleaned.dropna(inplace=True)

# we will now clean the date of birth column.
sorted_post_cleaned['Year_of_Birth'] = sorted_post_cleaned['Date of Birth'].str.extract(
    r"([1-2][0-9]{3})")

sorted_post_cleaned.dropna(inplace=True)

current_year = dt.datetime.now().year
sorted_post_cleaned['Age'] = current_year - \
    sorted_post_cleaned['Year_of_Birth'].astype('int')
sorted_post_cleaned['Age'].value_counts().sort_index(ascending=False)


# We then need to create age-categorization buckets
sorted_post_cleaned.drop(
    sorted_post_cleaned[sorted_post_cleaned.Age > 83].index, inplace=True)
sorted_post_cleaned['Age'].value_counts().sort_index(ascending=False)

# Create a function that maps age into categories.


def age_range(val):
    if pd.isnull(val):
        return np.nan
    elif val <= 4:
        return '0-04'
    elif val > 4 and val <= 9:
        return '05-09'
    elif val > 9 and val <= 14:
        return '10-14'
    elif val > 14 and val <= 19:
        return '15-19'
    elif val > 19 and val <= 24:
        return '20-24'
    elif val > 24 and val <= 29:
        return '25-29'
    elif val > 29 and val <= 34:
        return '30-34'
    elif val > 34 and val <= 39:
        return '35-39'
    elif val > 39 and val <= 44:
        return '40-44'
    elif val > 44 and val <= 49:
        return '45-49'
    elif val > 49 and val <= 54:
        return '50-54'
    elif val > 54 and val <= 59:
        return '55-59'
    elif val > 59 and val <= 64:
        return '60-64'
    elif val > 64 and val <= 69:
        return '65-69'
    elif val > 69 and val <= 74:
        return '70-74'
    elif val > 74 and val <= 79:
        return '75-79'
    elif val > 79 and val <= 84:
        return '80-84'


sorted_post_cleaned['Age_range'] = sorted_post_cleaned['Age'].apply(age_range)


# Portside Boulders Osborne Park = [-31.913804807106942, 115.81700105099641]
# Portside Boulders OConnor = [-32.058028246537745, 115.78597443149988]

sorted_post_cleaned_suburbs = sorted_post_cleaned[[
    'Sex', 'Gym', 'Suburb_updated', 'Postcode_updated', 'Lat_precise', 'Long_precise', 'Age']].copy()

sorted_post_cleaned_suburbs.to_csv('Full_cleaned.csv')

