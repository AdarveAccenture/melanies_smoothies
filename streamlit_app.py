# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize your smoothie!:cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")


smoothie_name = st.text_input("Name of Smoothie")
st.write("The name of your smoothie will be", smoothie_name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    
    ingredients_string = ''
    
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '

    time_to_insert = st.button('Submit Order')
        
    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders( name_on_order , ingredients)
            values ('""" + smoothie_name + """','""" + ingredients_string + """')"""
        
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {smoothie_name}!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/apple")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
