# baskets.py

import streamlit as st
import datetime
import pandas as pd
from database_utils import (
    get_menu_plan, 
    get_inventory, 
    get_all_recipe_ingredients, 
    upsert_inventory_item
)

st.set_page_config(page_title="Prep Basket", layout="wide")
st.title("🧺 Prep Basket")
st.markdown("Here's what you need to buy for meals planned for **today and tomorrow**.")

# --- DATA FETCHING ---
menu_df = get_menu_plan()
inventory_df = get_inventory()
recipes_df = get_all_recipe_ingredients()

def get_basket_items():
    """Calculates the shopping list based on the next 48 hours of meals."""
    
    # 1. Identify relevant meals
    today = datetime.datetime.now().strftime('%A')
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%A')
    upcoming_meals_df = menu_df[menu_df['meal_day'].isin([today, tomorrow])]

    if upcoming_meals_df.empty:
        return pd.DataFrame()

    # 2. Merge to get required ingredients
    needed_df = pd.merge(upcoming_meals_df, recipes_df, on='recipe_name')
    needed_df['total_required'] = needed_df['num_persons'] * needed_df['quantity_per_person']
    
    # 3. Aggregate total requirements
    required_agg = needed_df.groupby('item_name').agg(
        total_required=('total_required', 'sum'),
        unit=('unit', 'first'), # Assuming unit is consistent for an ingredient
        dishes=('recipe_name', lambda x: list(set(x)))
    ).reset_index()

    # 4. Merge with current inventory to find shortfall
    comparison_df = pd.merge(
        required_agg, 
        inventory_df[['item_name', 'quantity']], 
        on='item_name', 
        how='left'
    ).fillna(0)
    
    comparison_df['shortfall'] = comparison_df['total_required'] - comparison_df['quantity']
    
    # 5. Filter for items you need to buy
    basket_df = comparison_df[comparison_df['shortfall'] > 0].copy()
    
    return basket_df

def add_to_stock_callback(item_name, quantity, unit):
    """Callback function to add a purchased item to the inventory."""
    try:
        upsert_inventory_item(item_name, quantity, unit)
        st.toast(f"Added {quantity:.2f} {unit} of {item_name} to your stock!")
    except Exception as e:
        st.error(f"Failed to update stock: {e}")

# --- UI DISPLAY ---
basket = get_basket_items()

st.markdown("---")

if basket.empty:
    st.success("✅ You're all set! You have all the ingredients for the next two days.")
else:
    st.subheader("Your Shopping List")
    for index, row in basket.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([0.7, 0.3])
            
            with col1:
                st.markdown(f"#### {row['item_name']}")
                st.markdown(f"**Need to buy:** `{row['shortfall']:.2f} {row['unit']}`")
                st.caption(f"Required for: {', '.join(row['dishes'])}")
            
            with col2:
                st.button(
                    "✓ Add to Stocks",
                    key=f"add_{row['item_name']}",
                    on_click=add_to_stock_callback,
                    args=(row['item_name'], row['shortfall'], row['unit']),
                    use_container_width=True
                )