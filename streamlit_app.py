import streamlit
import pandas
import requests 
import snowflake.connector
from urllib.error import URLError

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list =my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


# create a repeatable function
def get_fruityvice_date(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      fruityvice_normalize = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalize
    
    
#New section
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('what fruit information?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get info.")
  else:
      back_from_fruntion = get_fruityvice_date(fruit_choice)
      streamlit.dataframe(back_from_fruntion)

except URLError as e:
    streamlit.error()



streamlit.header("The fruit load list contains:")
#snowflake related funcitons
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
            return my_cur.fetchall()
      
# add a button
if streamlit.button('Get fruit load list'):     
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      my_cnx.close()
      streamlit.dataframe(my_data_rows)



#allow end user to add fruit dynamically
def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
            return "Thanks for adding " + new_fruit
      
      
add_my_fruit = streamlit.text_input('what fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(add_my_fruit)
      my_cnx.close()
      streamlit.text(back_from_function)
