import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title("🍹 Customize Your Smoothie! 🍹")

st.write(
    """Choose the fruits you want in your custom smoothie!"""
)

name_on_order = st.text_input("Name on Order")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    if st.button("Submit Order"):

        my_insert_stmt = f"""
            insert into smoothies.public.orders
            (ingredients, name_on_order)
            values
            ('{ingredients_string}','{name_on_order}')
        """

        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!")
