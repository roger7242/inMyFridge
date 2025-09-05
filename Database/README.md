# InfyFridge Database Project

This repository contains the SQL scripts to create and populate the `infy_fridge` database. This is a simple inventory management system for a kitchen, tracking items, stock levels, and dishes that can be made from those items.

## About the Database

The database consists of four main tables:

- `Item`: A list of all possible food items (e.g., Tomato, Potato, Paneer).
- `Stock`: Tracks the current quantity of each item in the fridge/pantry.
- `Dishes`: A list of all possible dishes (e.g., Tomato Soup, Palak Paneer).
- `Dish_Items`: A junction table that maps which items are required to make each dish, supporting many-to-many relationships.

## How to Use

1. **Create the Database**:
   Connect to your PostgreSQL server and run the following command:
   ```sql
   CREATE DATABASE infy_fridge;
   ```
2. **Run the Schema Script**:
   Connect to the newly created `infy_fridge` database and execute the `infy_fridge_schema.sql` file. This will create all the tables and insert the initial data.