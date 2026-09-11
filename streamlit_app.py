import streamlit as st
from snowflake.snowpark.functions import col
import requests  

st.title("🍹 Customize Your Smoothie! 🍹")

st.write(
    """Choose the fruits you want in your custom smoothie!"""
)


name_on_order = st.text_input("Name on Order")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)



if st.button("Submit Order"):
    

    ingredients_string = ','.join(ingredients_list)

    my_insert_stmt = f"""
        insert into smoothies.public.orders
        (ingredients, name_on_order)
        values
        ('{ingredients_string}','{name_on_order}')
    """

    st.write(my_insert_stmt)
    session.sql(my_insert_stmt).collect()
    st.success("Your Smoothie is ordered!")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

