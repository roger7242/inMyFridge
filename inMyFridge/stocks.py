# stocks.py

import streamlit as st
import pandas as pd
from database_utils import (
    get_inventory, 
    add_stock_item, 
    update_inventory_quantity, 
    delete_inventory_item
)

st.set_page_config(page_title="Stock Management", layout="wide")
st.title("🛒 Stock Management")
st.markdown("Add, view, and manage your kitchen inventory directly from the database.")

# --- UI STATE MANAGEMENT ---
if 'show_add_stock_panel' not in st.session_state:
    st.session_state.show_add_stock_panel = False

if st.button("➕ Add New Stock Item", use_container_width=True):
    st.session_state.show_add_stock_panel = not st.session_state.show_add_stock_panel

# --- ADD NEW STOCK PANEL ---
if st.session_state.show_add_stock_panel:
    with st.container(border=True):
        with st.form("new_stock_form", clear_on_submit=True):
            st.subheader("Add a New Item to Your Inventory")
            
            c1, c2, c3 = st.columns(3)
            name = c1.text_input("Item Name", placeholder="e.g., Rice")
            quantity = c2.number_input("Initial Quantity", min_value=0.0, step=0.1, format="%.2f")
            unit = c3.selectbox("Unit", ["kg", "g", "L", "ml", "pcs"])
            
            submitted = st.form_submit_button("✔️ Add Stock Item")
            if submitted:
                if name:
                    try:
                        add_stock_item(name, quantity, unit)
                        st.success(f"Added '{name}' to your inventory!")
                        st.session_state.show_add_stock_panel = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding item: {e}")
                else:
                    st.warning("Please enter an item name.")
        
        if st.button("✖️ Close"):
            st.session_state.show_add_stock_panel = False
            st.rerun()

st.markdown("---")

# --- CURRENT STOCK DISPLAY ---
st.header("Current Stock List")

inventory_df = get_inventory()

if inventory_df.empty:
    st.info("Your inventory is empty. Add a new item to get started!")
else:
    # We will build an editable table. Store edits in a temporary dictionary in session state.
    if 'inventory_edits' not in st.session_state:
        st.session_state.inventory_edits = {}

    # Header for our custom table
    col_header = st.columns([0.1, 0.5, 0.2, 0.2])
    col_header[1].markdown("**Item Name**")
    col_header[2].markdown("**Quantity**")
    col_header[3].markdown("**Unit**")

    # Iterate through the DataFrame to display each item
    for index, row in inventory_df.iterrows():
        inventory_id = row['inventory_id']
        item_name = row['item_name']
        quantity = row['quantity']
        unit = row['unit']
        
        col_item = st.columns([0.1, 0.5, 0.2, 0.2])

        # Delete Button
        with col_item[0]:
            st.button("🗑️", key=f"del_{inventory_id}", on_click=delete_inventory_item, args=(inventory_id,))

        # Item Name (read-only)
        with col_item[1]:
            st.markdown(f"**{item_name}**")

        # Quantity (editable)
        with col_item[2]:
            new_quantity = st.number_input(
                "Quantity", 
                value=float(quantity), 
                key=f"qty_{inventory_id}", 
                label_visibility="collapsed",
                step=1.0 if unit == 'pcs' else 0.1,
                format="%.2f"
            )
            # If the value has changed from the original, store it in our edits dictionary
            if new_quantity != float(quantity):
                st.session_state.inventory_edits[inventory_id] = new_quantity
        
        # Unit (read-only for simplicity)
        with col_item[3]:
            st.markdown(unit)

    # --- SAVE CHANGES ---
    if st.session_state.inventory_edits:
        if st.button("💾 Save All Quantity Changes", use_container_width=True, type="primary"):
            for inv_id, new_qty in st.session_state.inventory_edits.items():
                update_inventory_quantity(inv_id, new_qty)
            st.session_state.inventory_edits = {} # Clear edits after saving
            st.success("All changes saved!")
            st.rerun()