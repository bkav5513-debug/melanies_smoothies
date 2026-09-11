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

# FRUIT_NAMEとSEARCH_ONの両方を取得する
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), col('SEARCH_ON')
)

# Snowpark DataFrameをPandas DataFrameに変換しておく(後で検索しやすくするため)
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # 選ばれたFRUIT_NAMEに対応するSEARCH_ONの値を取り出す
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
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
