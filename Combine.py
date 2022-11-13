import pandas as pd
oc = pd.read_csv(r"Data\Waiver Form V3.0 - Sheet1.csv")
op = pd.read_csv(r"Data\Waiver Form Osborne Park - Sheet1.csv")
oc['Gym'] = 'Oconnor'
op['Gym'] = 'Osborne'

#dropping columns that aren't pertinant to this iteration of the project

oc_columns = oc[['Address', 'Street Number and Name', 'Suburb',
                 'State', 'Postcode', 'Date of Birth', 'Sex', 'Gym']]
op_columns = op[['Address', 'Street Number and Name', 'Suburb',
                 'State', 'Postcode', 'Date of Birth', 'Sex', 'Gym']]

combined_gyms = pd.concat([oc_columns,op_columns])

#combine columns relating to address into a single row
combined_gyms['Full_Address'] = combined_gyms['Address'].fillna('') + ' '+ combined_gyms['Street Number and Name'].fillna('') + ' '+ combined_gyms['Suburb'].fillna('') + ' '+combined_gyms['Postcode'].fillna('') + ' '+ combined_gyms['State'].fillna('')

combined_gyms.to_csv('combined_gyms.csv')
