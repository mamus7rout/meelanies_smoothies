# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

from snowflake.snowpark.functions import col
import requests
import pandas as pd


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write(
    """ Choose the fruits you want in your custom Smoothie!.
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your smoothie will be:", name_on_order)

#option = st.selectbox(
 #   "What is your favourite fruit?",
  #  ("Banana", "Strawberries", "Peaches"),
#)

#st.write("You selected:", option)
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                 my_dataframe,max_selections=5)
if ingredients_list:
   # st.write(ingredients_list)
   # st.text(ingredients_list)
    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered,{name_on_order}', icon="✅")
if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        #st.write(fruityvice_response.json())
        #st.text(fruityvice_response)

        
       # fv_df = json_normalize(fruityvice_response.json())
        #st.dataframe(data=fv_df, use_container_width=True)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
