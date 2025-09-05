CREATE DATABASE IF NOT EXISTS inmyfridge_db;
USE inmyfridge_db;

CREATE TABLE IF NOT EXISTS `stock_items` (
  `item_id` INT NOT NULL AUTO_INCREMENT,
  `item_name` VARCHAR(100) NOT NULL,
  `base_unit` ENUM('kg', 'g', 'L', 'ml', 'pcs') NOT NULL,
  PRIMARY KEY (`item_id`),
  UNIQUE INDEX `item_name_UNIQUE` (`item_name` ASC) VISIBLE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `inventory` (
  `inventory_id` INT NOT NULL AUTO_INCREMENT,
  `item_id` INT NOT NULL,
  `quantity` DECIMAL(10,2) NOT NULL,
  `unit` VARCHAR(10) NOT NULL,
  `last_updated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`inventory_id`),
  UNIQUE INDEX `item_id_UNIQUE` (`item_id` ASC) VISIBLE,
  CONSTRAINT `fk_inventory_stock_items`
    FOREIGN KEY (`item_id`) REFERENCES `stock_items` (`item_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `recipes` (
  `recipe_id` INT NOT NULL AUTO_INCREMENT,
  `recipe_name` VARCHAR(150) NOT NULL,
  `description` TEXT NULL,
  PRIMARY KEY (`recipe_id`),
  UNIQUE INDEX `recipe_name_UNIQUE` (`recipe_name` ASC) VISIBLE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `recipe_ingredients` (
  `ingredient_id` INT NOT NULL AUTO_INCREMENT,
  `recipe_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  `quantity_per_person` DECIMAL(10,2) NOT NULL,
  `unit` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`ingredient_id`),
  UNIQUE INDEX `recipe_item_UNIQUE` (`recipe_id` ASC, `item_id` ASC) VISIBLE,
  CONSTRAINT `fk_recipe_ingredients_recipes`
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`recipe_id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_recipe_ingredients_stock_items`
    FOREIGN KEY (`item_id`) REFERENCES `stock_items` (`item_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `menu_plan` (
  `plan_id` INT NOT NULL AUTO_INCREMENT,
  `recipe_id` INT NOT NULL,
  `meal_day` ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
  `meal_time` ENUM('Breakfast', 'Lunch', 'Dinner') NOT NULL,
  `num_persons` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`plan_id`),
  UNIQUE INDEX `meal_slot_UNIQUE` (`meal_day` ASC, `meal_time` ASC) VISIBLE,
  CONSTRAINT `fk_menu_plan_recipes`
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`recipe_id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;