import streamlit
import pandas as pd
import requests

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
f_choice = streamlit.text_input("What fruit would you like information about?", "Kiwi");
streamlit.text("The selected fruit is: {}".format(f_choice));
f_response = requests.get("https://fruityvice.com/api/fruit/"+f_choice); # watermelon info

streamlit.dataframe(pd.json_normalize(f_response.json()));
