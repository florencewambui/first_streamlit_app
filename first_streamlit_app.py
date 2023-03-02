import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('Snowflake Learning Diner')

streamlit.header('Breakfast Menu')
streamlit.text('Blueberry Oatmeal Pancakes')
streamlit.text('Smoothies')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import csv file from aws bucket containing fruits data
fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_list = fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Choose the fruits you would like in your smoothie: ", list(fruit_list.index), ['Apple', 'Banana', 'Grapes'])
fruits_to_show = fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruit advice')
#user selects fruit to get advice on
fruit_choice = streamlit.text_input('What fruit would you like to learn more about?')

#fetch data from fruitvice api
fruitvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)
fruit_info = pd.json_normalize(fruitvice_response.json())
streamlit.text('Below is some helpful information about '+ fruit_choice)
streamlit.dataframe(fruit_info)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("Here is the list of fruits:")
streamlit.text(my_data_row)
