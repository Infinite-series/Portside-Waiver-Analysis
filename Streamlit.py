import streamlit as st
import pandas as pd
# Portside Boulders Osborne Park = [-31.913804807106942, 115.81700105099641]
# Portside Boulders OConnor = [-32.058028246537745, 115.78597443149988]
sorted_post_cleaned_suburbs = pd.read_csv(r'Data\Full_cleaned.csv')

APP_TITLE = 'Portside Wavier Data Visualisation'
st.set_page_config(APP_TITLE)
st.title(APP_TITLE)


piv = sorted_post_cleaned_suburbs.pivot_table(
    index=["Postcode_updated", 'Suburb_updated','Lat_precise','Long_precise'],values=['Sex'],aggfunc=len).sort_values('Sex',ascending=False)
piv.rename(columns={'Sex':'Count'},inplace=True)

st.write(piv)