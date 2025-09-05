import streamlit as st

home = st.Page("home.py", title="Home", icon="🏠")
basket = st.Page("baskets.py", title="Baskets", icon="🧺")
stock = st.Page("stocks.py", title="Stocks", icon="🥕")
menu = st.Page("menu.py", title="Menu", icon="🍲")

# Set up navigation
pg = st.navigation([home, stock, menu, basket])

# Run the selected page
pg.run()
