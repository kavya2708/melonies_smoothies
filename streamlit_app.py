import requests
import streamlit as st
from snowflake.snowpark.functions import col

# --- 1. App Header ---
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# --- 2. User Input ---
name_on_order = st.text_input('Name on Smoothie')
if name_on_order:
    st.write('The name on your smoothie will be:', name_on_order)

# --- 3. Snowflake Connection ---
# Using st.connection handles session management more efficiently
cnx = st.connection("snowflake")
session = cnx.session()

# Get the data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))

# --- 4. Ingredient Selection ---
ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# --- 5. Order Submission ---
if ingredient_list:
    ingredient_string = ""

    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        # 4. Use the search_on variable for the API call
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    # Strip the trailing space for a cleaner database entry
    ingredient_string = ingredient_string.strip()

    # Build the SQL Insert Statement
    # Note: Ensure name_on_order isn't empty before inserting
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredient_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        if name_on_order:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        else:
            st.error("Please add a name to the order before submitting.")
