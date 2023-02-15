import streamlit
import pandas as pd

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
pd.DataFrame(fruits_to_show)
