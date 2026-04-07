# Import python packages
import requests
import streamlit as st
import pandas as pd  # Added Pandas
#from snowflake.snowpark.functions import col
#from snowflake.snowpark.context import get_active_session
#from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
  """Choose the Fruits you want in your custom Smoothie!
  """
)
name_on_order =st.text_input('Name on Smoothie')
st.write('the name on your smoothie will be:',name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

pd_df = my_dataframe.to_pandas()
#st.dataframe(data=my_dataframe, use_container_width=True)
Ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:",my_dataframe,max_selections=5
)
#st.write(Ingredient_list)
#st.text(Ingredient_list)

if Ingredient_list :
    #st.write(Ingredient_list)
    #st.text(Ingredient_list)
    ingredient_string=''
    for fruit_chosen in Ingredient_list:
        ingredient_string+=fruit_chosen+' '
    #st.write(ingredient_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredient_string + """','""" + name_on_order + """')"""
    
    #st.write(my_insert_stmt)
    time_to_insert= st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
