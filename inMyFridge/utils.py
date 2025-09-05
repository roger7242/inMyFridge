# utils.py

import streamlit as st

def format_quantity(quantity, unit):
    """Formats a quantity into a human-readable string (e.g., 1500g -> 1.5 kg)."""
    unit = unit.lower()
    if unit == 'g' and quantity >= 1000:
        return f"{quantity / 1000:.2f} kg"
    if unit == 'ml' and quantity >= 1000:
        return f"{quantity / 1000:.2f} L"
    # For 'pcs' or small quantities, show the number directly
    if unit == 'pcs':
        return f"{int(quantity)} pcs"
    return f"{quantity:.2f} {unit}"

def initialize_data():
    """Initializes the session state with empty data structures for a clean start."""
    if "recipes" not in st.session_state:
        st.session_state.recipes = {}
    if "menu_plan" not in st.session_state:
        st.session_state.menu_plan = {}
    if "inventory" not in st.session_state:
        st.session_state.inventory = []
    if "person_counts" not in st.session_state:
        st.session_state.person_counts = {}

def load_dummy_data():
    """Loads a full set of sample data for demonstration purposes."""
    st.session_state.recipes = {
        "Poha": {"Poha (rice flakes)": {"qty": 0.1, "unit": "kg"}, "Onion": {"qty": 0.05, "unit": "kg"}, "Peanuts": {"qty": 0.02, "unit": "kg"}},
        "Idli": {"Rice": {"qty": 0.1, "unit": "kg"}, "Urad dal": {"qty": 0.04, "unit": "kg"}, "Salt": {"qty": 0.002, "unit": "kg"}},
        "Upma": {"Rava (semolina)": {"qty": 0.1, "unit": "kg"}, "Onion": {"qty": 0.05, "unit": "kg"}},
        "Veg Pulao": {"Rice": {"qty": 0.15, "unit": "kg"}, "Mixed veg": {"qty": 0.1, "unit": "kg"}},
        "Rajma Chawal": {"Rajma": {"qty": 0.1, "unit": "kg"}, "Rice": {"qty": 0.15, "unit": "kg"}},
        "Dal Tadka": {"Toor dal": {"qty": 0.1, "unit": "kg"}, "Ghee": {"qty": 0.01, "unit": "kg"}},
        "Paneer Butter Masala": {"Paneer": {"qty": 0.1, "unit": "kg"}, "Butter": {"qty": 0.03, "unit": "kg"}},
        "Chole": {"Chickpeas": {"qty": 0.1, "unit": "kg"}, "Onion": {"qty": 0.05, "unit": "kg"}},
        "Veg Biryani": {"Basmati rice": {"qty": 0.15, "unit": "kg"}, "Mixed veg": {"qty": 0.1, "unit": "kg"}},
        "Khichdi": {"Rice": {"qty": 0.1, "unit": "kg"}, "Moong dal": {"qty": 0.05, "unit": "kg"}},
        "Aloo Paratha": {"Wheat flour": {"qty": 0.15, "unit": "kg"}, "Potato": {"qty": 0.1, "unit": "kg"}},
        "Sambar Rice": {"Rice": {"qty": 0.15, "unit": "kg"}, "Toor dal": {"qty": 0.05, "unit": "kg"}},
    }
    st.session_state.menu_plan = {
        ("Monday","Breakfast"): "Poha", ("Monday","Lunch"): "Veg Pulao", ("Monday","Dinner"): "Paneer Butter Masala",
        ("Tuesday","Breakfast"): "Idli", ("Tuesday","Lunch"): "Rajma Chawal", ("Tuesday","Dinner"): "Chole",
        ("Wednesday","Breakfast"): "Upma", ("Wednesday","Lunch"): "Dal Tadka", ("Wednesday","Dinner"): "Veg Biryani",
        ("Thursday","Breakfast"): "Aloo Paratha", ("Thursday","Lunch"): "Sambar Rice", ("Thursday","Dinner"): "Paneer Butter Masala",
        ("Friday","Breakfast"): "Poha", ("Friday","Lunch"): "Veg Pulao", ("Friday","Dinner"): "Khichdi",
    }

def convert_to_base_unit(quantity, unit):
    # ... (function remains the same)
    unit = unit.lower()
    if unit == 'kg': return quantity * 1000, 'g'
    if unit == 'l': return quantity * 1000, 'ml'
    if unit in ['g', 'ml', 'pcs']: return quantity, unit
    return quantity, unit

def check_dish_status(dish_name, num_persons):
    # ... (function remains the same)
    if not dish_name or dish_name not in st.session_state.recipes: return "Not Planned", "⚪"
    recipe = st.session_state.recipes[dish_name]
    missing_ingredients, low_stock_ingredients = [], []
    inventory_map = {item['name'].lower(): item for item in st.session_state.inventory}
    for ingredient, details in recipe.items():
        total_required_qty = details['qty'] * num_persons
        if ingredient.lower() not in inventory_map:
            missing_ingredients.append(ingredient)
            continue
        available_item = inventory_map[ingredient.lower()]
        available_qty, base_unit = convert_to_base_unit(available_item['quantity'], available_item['unit'])
        required_qty, _ = convert_to_base_unit(total_required_qty, details['unit'])
        if available_qty < required_qty: missing_ingredients.append(ingredient)
        elif (available_qty - required_qty) < (0.2 * available_qty): low_stock_ingredients.append(ingredient)
    if missing_ingredients: return f"Missing: {', '.join(missing_ingredients)}", "❌"
    if low_stock_ingredients: return f"Low Stock: {', '.join(low_stock_ingredients)}", "⚠️"
    return "Available", "✅"

def delete_stock(index_to_delete):
    """Deletes an item from the stock inventory."""
    st.session_state.inventory.pop(index_to_delete)