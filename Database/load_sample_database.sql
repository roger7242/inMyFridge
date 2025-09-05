-- Sample Data Insertion Script for inMyFridge Project
-- This script populates the database with initial data for demonstration.
-- Run this after creating the tables with the schema script.

-- -----------------------------------------------------
-- 1. Populate the Master List of Stock Items
-- `INSERT IGNORE` prevents errors if an item already exists.
-- -----------------------------------------------------

INSERT IGNORE INTO `stock_items` (`item_name`, `base_unit`) VALUES
('Poha (rice flakes)', 'kg'),
('Peanuts', 'kg'),
('Onion', 'kg'),
('Mustard Seeds', 'kg'),
('Oil', 'L'),
('Salt', 'kg'),
('Rice', 'kg'),
('Urad dal', 'kg'),
('Rava (semolina)', 'kg'),
('Curry leaves', 'g'),
('Mixed veg', 'kg'),
('Whole spices', 'g'),
('Rajma', 'kg'),
('Tomato', 'kg'),
('Spices', 'g'),
('Toor dal', 'kg'),
('Ghee', 'kg'),
('Cumin', 'g'),
('Garlic', 'kg'),
('Chili', 'pcs'),
('Paneer', 'kg'),
('Butter', 'kg'),
('Cream', 'L'),
('Chickpeas', 'kg'),
('Basmati rice', 'kg'),
('Moong dal', 'kg'),
('Turmeric', 'g'),
('Wheat flour', 'kg'),
('Potato', 'kg'),
('Sambar powder', 'g'),
('Tamarind', 'g'),
('Veggies', 'kg');

-- -----------------------------------------------------
-- 2. Populate the Personal Inventory with Initial Quantities
-- We use a subquery `(SELECT item_id FROM ...)` to get the correct foreign key.
-- -----------------------------------------------------
INSERT IGNORE INTO `inventory` (`item_id`, `quantity`, `unit`) VALUES
((SELECT item_id FROM stock_items WHERE item_name = 'Rice'), 2.0, 'kg'),
((SELECT item_id FROM stock_items WHERE item_name = 'Onion'), 1.0, 'kg'),
((SELECT item_id FROM stock_items WHERE item_name = 'Toor dal'), 1.0, 'kg'),
((SELECT item_id FROM stock_items WHERE item_name = 'Paneer'), 0.5, 'kg'),
((SELECT item_id FROM stock_items WHERE item_name = 'Salt'), 1.0, 'kg'),
((SELECT item_id FROM stock_items WHERE item_name = 'Oil'), 1.0, 'L');

-- -----------------------------------------------------
-- 3. Populate the Recipes
-- -----------------------------------------------------
INSERT IGNORE INTO `recipes` (`recipe_name`) VALUES
('Poha'),
('Idli'),
('Upma'),
('Veg Pulao'),
('Rajma Chawal'),
('Dal Tadka'),
('Paneer Butter Masala'),
('Chole'),
('Veg Biryani'),
('Khichdi'),
('Aloo Paratha'),
('Sambar Rice');

-- -----------------------------------------------------
-- 4. Populate Recipe Ingredients (linking recipes to stock items)
-- -----------------------------------------------------
INSERT IGNORE INTO `recipe_ingredients` (`recipe_id`, `item_id`, `quantity_per_person`, `unit`) VALUES
-- Poha Ingredients
((SELECT recipe_id FROM recipes WHERE recipe_name = 'Poha'), (SELECT item_id FROM stock_items WHERE item_name = 'Poha (rice flakes)'), 0.1, 'kg'),
((SELECT recipe_id FROM recipes WHERE recipe_name = 'Poha'), (SELECT item_id FROM stock_items WHERE item_name = 'Onion'), 0.05, 'kg'),
-- Rajma Chawal Ingredients
((SELECT recipe_id FROM recipes WHERE recipe_name = 'Rajma Chawal'), (SELECT item_id FROM stock_items WHERE item_name = 'Rajma'), 0.1, 'kg'),
((SELECT recipe_id FROM recipes WHERE recipe_name = 'Rajma Chawal'), (SELECT item_id FROM stock_items WHERE item_name = 'Rice'), 0.15, 'kg'),
-- Paneer Butter Masala Ingredients
((SELECT recipe_id FROM recipes WHERE recipe_name = 'Paneer Butter Masala'), (SELECT item_id FROM stock_items WHERE item_name = 'Paneer'), 0.1, 'kg'),
((SELECT recipe_id FROM recipes WHERE recipe_name = 'Paneer Butter Masala'), (SELECT item_id FROM stock_items WHERE item_name = 'Butter'), 0.03, 'kg'),
((SELECT recipe_id FROM recipes WHERE recipe_name = 'Paneer Butter Masala'), (SELECT item_id FROM stock_items WHERE item_name = 'Tomato'), 0.15, 'kg');
-- Add other ingredients for other recipes as needed...

-- -----------------------------------------------------
-- 5. Populate the Weekly Menu Plan
-- `ON DUPLICATE KEY UPDATE` will update the dish if a slot is already filled.
-- -----------------------------------------------------
INSERT INTO `menu_plan` (`meal_day`, `meal_time`, `recipe_id`, `num_persons`) VALUES
('Monday', 'Breakfast', (SELECT recipe_id FROM recipes WHERE recipe_name = 'Poha'), 2),
('Monday', 'Lunch', (SELECT recipe_id FROM recipes WHERE recipe_name = 'Veg Pulao'), 2),
('Monday', 'Dinner', (SELECT recipe_id FROM recipes WHERE recipe_name = 'Paneer Butter Masala'), 4),
('Tuesday', 'Breakfast', (SELECT recipe_id FROM recipes WHERE recipe_name = 'Idli'), 2),
('Tuesday', 'Lunch', (SELECT recipe_id FROM recipes WHERE recipe_name = 'Rajma Chawal'), 4),
('Tuesday', 'Dinner', (SELECT recipe_id FROM recipes WHERE recipe_name = 'Chole'), 4),
('Wednesday', 'Breakfast', (SELECT recipe_id FROM recipes WHERE recipe_name = 'Upma'), 2)
ON DUPLICATE KEY UPDATE 
    recipe_id = VALUES(recipe_id), 
    num_persons = VALUES(num_persons);