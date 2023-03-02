import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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
#fetch data from fruitvice api
def get_fruitvice_data(fruit_choice):
  fruitvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)
  fruit_info = pd.json_normalize(fruitvice_response.json())
  return fruit_info

try:
  fruit_choice = streamlit.text_input('What fruit would you like to learn more about?')
  if not fruit_choice:
    streamlit.error('Please input a fruit name in the text box above.')
  else:
    fruit_info_fetched = get_fruitvice_data(fruit_choice)
    streamlit.text('Below is some helpful information about '+ fruit_choice)
    streamlit.dataframe(fruit_info_fetched)
except URLError as e:
  streamlit.error()
    


def fetch_fruit_choice():
  #my_cur = my_cnx.cursor()
  my_cur.execute("select * from fruit_load_list")
  my_data_row = my_cur.fetchall()
  
if streamlit.button('Fetch fruits list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  with my_cnx.cursor as my_cur:
    fetched_fruits = fetch_fruit_choice()
    streamlit.dataframe(fetched_fruits)


fruit_choice_load = streamlit.text_input('What fruit would you like to load?')
streamlit.text('Thank you for adding ' + fruit_choice_load)

