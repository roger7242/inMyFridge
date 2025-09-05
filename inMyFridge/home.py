# home.py

import streamlit as st
import datetime
from database_utils import get_menu_plan, get_low_stock_items, check_dish_status

st.set_page_config(page_title="inMyFridge Home", layout="wide")
st.title("Welcome to inMyFridge 🏠")

# --- DATA FETCHING ---
menu_df = get_menu_plan()
low_stock_df = get_low_stock_items()
today_name = datetime.datetime.now().strftime('%A')

# Filter for today's menu
todays_menu_df = menu_df[menu_df['meal_day'] == today_name]

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns(2)

# --- Left Column: Today's Menu ---
with col1:
    with st.container(border=True):
        st.header(f"Today's Plan: {today_name}")

        for meal in ["Breakfast", "Lunch", "Dinner"]:
            meal_info = todays_menu_df[todays_menu_df['meal_time'] == meal]
            
            if not meal_info.empty:
                dish = meal_info['recipe_name'].iloc[0]
                persons = meal_info['num_persons'].iloc[0]
                
                # Check status against the database
                status_text, status_icon = check_dish_status(dish, persons)
                st.metric(label=f"{status_icon} {meal}", value=dish, delta=status_text, delta_color="off")
            else:
                st.metric(label=f"⚪ {meal}", value="Not Planned", delta_color="off")

# --- Right Column: Alerts & Actions ---
with col2:
    # "What's Running Low?" Widget
    with st.container(border=True):
        st.header("What's Running Low? 📉")
        
        if not low_stock_df.empty:
            for index, row in low_stock_df.iterrows():
                st.markdown(f"- **{row['item_name']}**: {row['quantity']} {row['unit']}")
        else:
            st.info("Your inventory looks well-stocked!")

    # "Quick Actions" Widget
    with st.container(border=True):
        st.header("Quick Actions ⚡")
        
        if st.button("🛒 Manage My Stock", use_container_width=True):
            st.switch_page("stocks.py")
        if st.button("📅 View & Edit Menu", use_container_width=True):
            st.switch_page("menu.py")
        if st.button("🧺 Go to Prep Basket", use_container_width=True):
            st.switch_page("baskets.py")