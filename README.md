inMyFridge - Smart Kitchen Inventory & Meal Planner
===================================================

inMyFridge is an intelligent web application designed to reduce food waste and streamline meal planning. It bridges the gap between your kitchen's inventory and your weekly menu, providing a seamless, at-a-glance dashboard to manage your culinary life.

✨ Key Features
--------------

*   **🏠 Smart Dashboard:** A homepage that displays today's menu with a real-time ingredient availability check (✅, ⚠️, ❌) and alerts you about low-stock items.
    
*   **🛒 Inventory Management:** A dedicated page to add, view, update, and delete items in your kitchen stock, tracking quantities and units.
    
*   **📅 Weekly Meal Planner:** An intuitive timetable to plan your breakfast, lunch, and dinner for the entire week. Includes a complete recipe book to define dishes and their per-person ingredient needs.
    
*   **🧺 Intelligent Prep Basket:** An automated shopping list that scans your menu for the next 48 hours, compares it against your current inventory, and tells you exactly what you need to buy.

🛠️ Tech Stack
--------------

*   **Frontend:** [Streamlit](https://streamlit.io/)
    
*   **Backend & Data Logic:** [Python](https://www.python.org/) & [Pandas](https://pandas.pydata.org/)
    
*   **Database:** [MySQL](https://www.mysql.com/)
    
*   **Database Connector:** [SQLAlchemy](https://www.sqlalchemy.org/) & [PyMySQL](https://github.com/PyMySQL/PyMySQL)
    
*   **Version Control:** [Git](https://git-scm.com/) & [GitHub](https://github.com/)
    
*   **Deployment:** [Streamlit Community Cloud](https://streamlit.io/cloud)
    

📂 Project Structure
--------------------

Your project is organized as follows, with a dedicated folder for database scripts and another for the Streamlit application code.


<img width="249" height="324" alt="image" src="https://github.com/user-attachments/assets/502617c4-5928-49a2-bb4f-58253131de1b" />


🚀 Setup and Installation
-------------------------

Follow these steps to get the application running on your local machine.

### 1\. Prerequisites

*   Python 3.8+
    
*   Git
    
*   A running MySQL Server instance
    
*   A MySQL client like MySQL Workbench
    

### 2\. Clone the Repository

`git clone [https://github.com/roger7242/inMyFridge](https://github.com/roger7242/inMyFridge)`

`cd inMyFridge/inMyFridge`
(Note: Navigate into the application subfolder to run Streamlit)

### 3\. Set Up a Virtual Environment

It is highly recommended to use a virtual environment inside the inMyFridge folder.

`# For Windows  python -m venv .venv  .\.venv\Scripts\activate`

`# For macOS/Linux  python3 -m venv .venv  source .venv/bin/activate`

### 4\. Install Dependencies

`pip install -r requirements.txt`

### 5\. Database Setup

1.  Open MySQL Workbench and connect to your MySQL server.
    
2.  CREATE DATABASE IF NOT EXISTS inmyfridge\_db;
    
3.  Run the **Database Schema Script** from Database/create\_database.sql to create all the necessary tables.
    
4.  (Optional but Recommended) Run the **Sample Data Script** from Database/load\_sample\_database.sql to populate your database with initial recipes and a sample menu.
    

### 6\. Configure Secrets

1.  Inside the inMyFridge folder, create a new folder named .streamlit.
    
2.  Inside .streamlit, create a file named secrets.toml.
    
  <img width="223" height="224" alt="image" src="https://github.com/user-attachments/assets/9bc3f9e5-0828-4cca-b873-afa822181184" />

    

▶️ How to Run the Application
-----------------------------

With your virtual environment activated and while you are inside the inMyFridge directory, run the following command:

`streamlit run streamlit_app.py`

Open your web browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).

🛣️ Future Enhancements
-----------------------

*   **Multiple recipes per meal slot:** Allow users to assign a combination of dishes (e.g., "Dal Tadka" + "Rice") to a single meal.
    
*   **"What can I make now?" feature:** A smart suggestion module on the homepage that lists all recipes that can be made with the current inventory.
    
*   **Barcode Scanning:** Integrate a barcode scanner to add new items to the inventory quickly.
    
*   **Nutritional Information:** Connect to a nutrition API to display calorie counts and other data for recipes.
