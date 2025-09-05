# menu.py

import streamlit as st
import pandas as pd
from database_utils import (
    get_recipes, 
    get_menu_plan, 
    set_menu_slot, 
    get_all_stock_items,
    get_recipe_details,
    save_recipe,
    delete_recipe
)

st.set_page_config(page_title="Menu Planner", layout="wide")
st.title("🍽️ Weekly Menu Planner")
st.markdown("Plan your meals, define recipes, and see your week at a glance.")

# --- DATA LOADING ---
recipes_df = get_recipes()
stock_items_df = get_all_stock_items()

# --- UI STATE MANAGEMENT ---
if 'show_management_panel' not in st.session_state:
    st.session_state.show_management_panel = False
if 'recipe_ingredients' not in st.session_state:
    st.session_state.recipe_ingredients = pd.DataFrame(columns=["item_id", "item_name", "quantity_per_person", "unit"])

if st.button("✏️ Manage Menu & Recipes", use_container_width=True):
    st.session_state.show_management_panel = not st.session_state.show_management_panel

# --- MANAGEMENT PANEL ---
if st.session_state.show_management_panel:
    with st.container(border=True):
        tab1, tab2 = st.tabs(["🗓️ Set Menu Slot", "🍲 Manage Recipes"])

        # --- TAB 1: SET MENU SLOT ---
        with tab1:
            with st.form("set_menu_form"):
                st.subheader("Assign a dish to a time slot")
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                times = ["Breakfast", "Lunch", "Dinner"]
                
                # Create a mapping from recipe name to recipe_id
                recipe_options = {name: id for id, name in zip(recipes_df['recipe_id'], recipes_df['recipe_name'])}
                
                c1, c2, c3 = st.columns(3)
                day = c1.selectbox("Day", days)
                time = c2.selectbox("Time", times)
                selected_recipe_name = c3.selectbox("Select Dish", ["— Clear Slot —"] + list(recipe_options.keys()))
                
                persons = st.number_input("Number of Persons", min_value=1, step=1, value=2)

                if st.form_submit_button("💾 Save Slot"):
                    if selected_recipe_name == "— Clear Slot —":
                        # Logic to clear a slot would go here (DELETE from menu_plan)
                        st.info("Slot cleared (functionality to be added).")
                    else:
                        selected_recipe_id = recipe_options[selected_recipe_name]
                        set_menu_slot(day, time, selected_recipe_id, persons)
                        st.success(f"Saved '{selected_recipe_name}' for {day} {time}.")
                    st.session_state.show_management_panel = False
                    st.rerun()

        # --- TAB 2: MANAGE RECIPES ---
        with tab2:
            st.subheader("Add, Edit, or Delete a Recipe")
            
            recipe_list = ["✨ Add New Recipe"] + recipes_df['recipe_name'].tolist()
            selected_recipe_name = st.selectbox("Select a recipe to edit", recipe_list)

            recipe_id = "new"
            recipe_name_default = ""

            if selected_recipe_name != "✨ Add New Recipe":
                recipe_id = recipes_df.loc[recipes_df['recipe_name'] == selected_recipe_name, 'recipe_id'].iloc[0]
                recipe_name_default = selected_recipe_name
                if st.button("Load Recipe to Edit"):
                    st.session_state.recipe_ingredients = get_recipe_details(recipe_id)

            with st.form(f"recipe_form_{recipe_id}"):
                recipe_name = st.text_input("Recipe Name", value=recipe_name_default)
                st.markdown("**Ingredients (per person)**")

                # Display existing ingredients in an editable format
                st.dataframe(st.session_state.recipe_ingredients, hide_index=True)
                
                st.markdown("---")
                st.markdown("**Add a new ingredient**")
                
                # Inputs to add a new ingredient
                item_map = {name: id for id, name in zip(stock_items_df['item_id'], stock_items_df['item_name'])}
                
                c1,c2,c3,c4 = st.columns([2,1,1,1])
                selected_item_name = c1.selectbox("Ingredient", options=item_map.keys(), key="new_ing_name")
                new_qty = c2.number_input("Qty", min_value=0.0, step=0.01, key="new_ing_qty")
                new_unit = c3.selectbox("Unit", ["kg", "g", "L", "ml", "pcs"], key="new_ing_unit")
                
                if c4.form_submit_button("➕ Add"):
                    new_row = pd.DataFrame([{
                        "item_id": item_map[selected_item_name],
                        "item_name": selected_item_name,
                        "quantity_per_person": new_qty,
                        "unit": new_unit
                    }])
                    st.session_state.recipe_ingredients = pd.concat([st.session_state.recipe_ingredients, new_row], ignore_index=True)
                    st.rerun()

                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                if c1.form_submit_button("💾 Save Recipe", use_container_width=True):
                    save_recipe(recipe_id, recipe_name, st.session_state.recipe_ingredients)
                    st.session_state.recipe_ingredients = pd.DataFrame() # Clear form state
                    st.success(f"Recipe '{recipe_name}' saved!")
                    st.rerun()
                
                if recipe_id != "new":
                    if c2.form_submit_button("🗑️ Delete Recipe", use_container_width=True):
                        delete_recipe(recipe_id)
                        st.session_state.recipe_ingredients = pd.DataFrame()
                        st.warning(f"Recipe '{recipe_name}' deleted.")
                        st.rerun()

                if c3.form_submit_button("✖️ Clear Form", use_container_width=True):
                    st.session_state.recipe_ingredients = pd.DataFrame()
                    st.rerun()

# --- WEEKLY TIMETABLE DISPLAY ---
st.markdown("---")
st.header("📅 Weekly Menu Timetable")

menu_plan_df = get_menu_plan()
# Pivot the data to create the timetable structure
if not menu_plan_df.empty:
    timetable = menu_plan_df.pivot_table(
        index='meal_day', 
        columns='meal_time', 
        values='recipe_name', 
        aggfunc='first'
    ).fillna("—")
    
    # Ensure correct order of days and meals
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meals_order = ["Breakfast", "Lunch", "Dinner"]
    timetable = timetable.reindex(index=days_order, columns=meals_order, fill_value="—")

    st.dataframe(timetable, use_container_width=True)
else:
    st.info("Your menu is empty. Add some meals using the management panel above!")