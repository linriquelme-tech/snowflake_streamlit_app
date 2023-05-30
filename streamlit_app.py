import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner!');
streamlit.header('Breakfast Menu');
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal');
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie');
streamlit.text('🐔 Hard-Boiled Free-Range Egg');
streamlit.text('🥑🍞 Avocado Toast');
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇');

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt');
my_fruit_list = my_fruit_list.set_index('Fruit');
# Let's put a pick list here so they can pick the fruit they want to include 
show_fruits = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']);
# Display the table on the page.
streamlit.dataframe(my_fruit_list.loc[show_fruits]);

streamlit.header("Fruit Advice!");
try:
  f_choice = streamlit.text_input("What fruit would you like information about?");
  if not f_choice:
    streamlit.error("Please select a fruit to get information");
  else:
    streamlit.dataframe(get_fruityvice_data(f_choice));
except URLError as e:
  streamlit.error();

#database (snowflake) connection

# FUNCTIONS
def get_fruityvice_data(this_choice):
  f_response = requests.get("https://fruityvice.com/api/fruit/"+this_choice);
  return pd.json_normalize(f_response.json())

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()");
    my_cur.execute("SELECT * FROM fruit_load_list");
    #my_data_row = my_cur.fetchone();
    return my_cur.fetchall();
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list VALUES('from streamlit')")
    return "Thanks for adding" + new_fruit;
    

streamlit.text("The fruit load list contains:");
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]);
  my_data_rows = get_fruit_load_list();
  streamlit.dataframe(my_data_rows);

#add a fruit to list
f_add = streamlit.text_input("What fruit would you like to add?");
streamlit.text(insert_row_snowflake(f_add))
