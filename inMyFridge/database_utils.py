# database_utils.py

import streamlit as st
import pandas as pd
from db_connector import get_db_connection
from sqlalchemy import text

# -----------------------------------------------------------------------------
# --- STOCK / INVENTORY FUNCTIONS ---
# -----------------------------------------------------------------------------

def get_inventory():
    """Fetches the current inventory, joining with stock_items to get names."""
    conn = get_db_connection()
    # Cache the result for 10 seconds to reduce DB calls on quick reloads
    return conn.query("""
        SELECT i.inventory_id, si.item_name, i.quantity, i.unit, i.last_updated
        FROM inventory i
        JOIN stock_items si ON i.item_id = si.item_id
        ORDER BY si.item_name;
    """, ttl=10)

def update_inventory_quantity(inventory_id, new_quantity):
    """Updates the quantity of a specific item in the inventory."""
    conn = get_db_connection()
    with conn.session as s:
        s.execute(
            text('UPDATE inventory SET quantity = :qty WHERE inventory_id = :id;'),
            params=dict(qty=new_quantity, id=inventory_id)
        )
        s.commit()
    # Clear all data caches to reflect the change immediately
    st.cache_data.clear()

def add_stock_item(name, quantity, unit):
    """Adds a new master item and sets its initial inventory quantity."""
    conn = get_db_connection()
    with conn.session as s:
        s.execute(
            text('INSERT IGNORE INTO stock_items (item_name, base_unit) VALUES (:name, :unit);'), 
            params=dict(name=name, unit=unit)
        )
        s.commit()
        
        result = s.execute(text('SELECT item_id FROM stock_items WHERE item_name = :name;'), params=dict(name=name))
        item_id = result.fetchone()[0]

        s.execute(
            text('INSERT IGNORE INTO inventory (item_id, quantity, unit) VALUES (:id, :qty, :unit);'),
            params=dict(id=item_id, qty=quantity, unit=unit)
        )
        s.commit()
    st.cache_data.clear()

def delete_inventory_item(inventory_id):
    """Deletes an item from the personal inventory."""
    conn = get_db_connection()
    with conn.session as s:
        s.execute(text('DELETE FROM inventory WHERE inventory_id = :id;'), params=dict(id=inventory_id))
        s.commit()
    st.cache_data.clear()

def upsert_inventory_item(item_name, quantity_to_add, unit):
    """Adds quantity to an existing inventory item or creates it if it doesn't exist."""
    conn = get_db_connection()
    with conn.session as s:
        s.execute(
            text('INSERT IGNORE INTO stock_items (item_name, base_unit) VALUES (:name, :unit);'),
            params={'name': item_name, 'unit': unit}
        )
        s.commit()
        
        result = s.execute(text('SELECT item_id FROM stock_items WHERE item_name = :name;'), params={'name': item_name})
        item_id = result.fetchone()[0]

        s.execute(
            text("""
                INSERT INTO inventory (item_id, quantity, unit)
                VALUES (:id, :qty, :unit)
                ON DUPLICATE KEY UPDATE quantity = quantity + :qty;
            """), 
            params={'id': item_id, 'qty': quantity_to_add, 'unit': unit}
        )
        s.commit()
    st.cache_data.clear()

# -----------------------------------------------------------------------------
# --- RECIPE & MENU FUNCTIONS ---
# -----------------------------------------------------------------------------

def get_recipes():
    """Fetches all recipes."""
    conn = get_db_connection()
    return conn.query('SELECT recipe_id, recipe_name FROM recipes ORDER BY recipe_name;', ttl=30)

def get_menu_plan():
    """Fetches the current weekly menu plan."""
    conn = get_db_connection()
    return conn.query("""
        SELECT mp.meal_day, mp.meal_time, r.recipe_name, mp.num_persons
        FROM menu_plan mp
        JOIN recipes r ON mp.recipe_id = r.recipe_id;
    """, ttl=10)

def set_menu_slot(day, time, recipe_id, persons):
    """Sets or updates a meal slot in the menu plan."""
    conn = get_db_connection()
    with conn.session as s:
        s.execute(
            text("""
                INSERT INTO menu_plan (meal_day, meal_time, recipe_id, num_persons)
                VALUES (:day, :time, :id, :persons)
                ON DUPLICATE KEY UPDATE recipe_id = :id, num_persons = :persons;
            """), 
            params=dict(day=day, time=time, id=recipe_id, persons=persons)
        )
        s.commit()
    st.cache_data.clear()

def get_all_stock_items():
    """Fetches the master list of all possible stock items."""
    conn = get_db_connection()
    return conn.query('SELECT item_id, item_name FROM stock_items ORDER BY item_name;', ttl=30)

def get_recipe_details(recipe_id):
    """Fetches the ingredients for a specific recipe."""
    conn = get_db_connection()
    return conn.query(
        'SELECT ri.item_id, si.item_name, ri.quantity_per_person, ri.unit FROM recipe_ingredients ri JOIN stock_items si ON ri.item_id = si.item_id WHERE ri.recipe_id = :id;',
        params={'id': recipe_id}, ttl=10
    )

def save_recipe(recipe_id, recipe_name, ingredients_df):
    """Adds a new recipe or updates an existing one."""
    conn = get_db_connection()
    with conn.session as s:
        if recipe_id == "new":
            result = s.execute(text('INSERT INTO recipes (recipe_name) VALUES (:name);'), params={'name': recipe_name})
            new_recipe_id = result.lastrowid
        else:
            new_recipe_id = recipe_id
            s.execute(text('UPDATE recipes SET recipe_name = :name WHERE recipe_id = :id;'), params={'name': recipe_name, 'id': recipe_id})
            s.execute(text('DELETE FROM recipe_ingredients WHERE recipe_id = :id;'), params={'id': recipe_id})

        for _, row in ingredients_df.iterrows():
            s.execute(
                text('INSERT INTO recipe_ingredients (recipe_id, item_id, quantity_per_person, unit) VALUES (:rid, :iid, :qty, :unit);'),
                params={'rid': new_recipe_id, 'iid': row['item_id'], 'qty': row['quantity_per_person'], 'unit': row['unit']}
            )
        s.commit()
    st.cache_data.clear()

def delete_recipe(recipe_id):
    """Deletes a recipe and its ingredients from the database."""
    conn = get_db_connection()
    with conn.session as s:
        s.execute(text('DELETE FROM recipes WHERE recipe_id = :id;'), params={'id': recipe_id})
        s.commit()
    st.cache_data.clear()

# -----------------------------------------------------------------------------
# --- DASHBOARD & BASKET LOGIC ---
# -----------------------------------------------------------------------------

def get_low_stock_items():
    """Fetches inventory items that are below a certain threshold."""
    conn = get_db_connection()
    return conn.query("""
        SELECT si.item_name, i.quantity, i.unit
        FROM inventory i
        JOIN stock_items si ON i.item_id = si.item_id
        WHERE 
            (i.unit IN ('kg', 'L') AND i.quantity < 0.25) OR
            (i.unit IN ('g', 'ml') AND i.quantity < 100) OR
            (i.unit = 'pcs' AND i.quantity <= 2);
    """, ttl=30)

def check_dish_status(dish_name, num_persons):
    """Checks if a single dish can be made and returns a status tuple."""
    conn = get_db_connection()
    recipe_df = conn.query(
        "SELECT si.item_name, ri.quantity_per_person, ri.unit FROM recipe_ingredients ri JOIN stock_items si ON ri.item_id = si.item_id JOIN recipes r ON ri.recipe_id = r.recipe_id WHERE r.recipe_name = :dish;",
        params={'dish': dish_name}
    )
    if recipe_df.empty: return "Recipe not found", "❓"

    inventory_df = get_inventory()
    inventory_map = {row['item_name']: row['quantity'] for _, row in inventory_df.iterrows()}

    missing, low_stock = [], []
    for _, ing in recipe_df.iterrows():
        required = ing['quantity_per_person'] * num_persons
        available = inventory_map.get(ing['item_name'], 0)
        
        # NOTE: Assumes consistent units. A more robust check would convert to base units first.
        if available < required:
            missing.append(ing['item_name'])
        elif (available - required) < (0.2 * available):
            low_stock.append(ing['item_name'])
            
    if missing: return f"Missing: {', '.join(missing)}", "❌"
    if low_stock: return f"Low Stock: {', '.join(low_stock)}", "⚠️"
    return "Available", "✅"

def get_all_recipe_ingredients():
    """Fetches a DataFrame with all ingredients for all recipes."""
    conn = get_db_connection()
    return conn.query("""
        SELECT r.recipe_name, si.item_name, ri.quantity_per_person, ri.unit
        FROM recipe_ingredients ri
        JOIN recipes r ON ri.recipe_id = r.recipe_id
        JOIN stock_items si ON ri.item_id = si.item_id;
    """, ttl=30)