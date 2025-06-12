# 💸 Expense Management System

An interactive Expense Management System built with **Streamlit** (frontend) and **FastAPI** (backend), using **MySQL** for local data storage and **Altair** for analytics visualizations.

---

## 📁 Project Structure

- **frontend/**: Contains the Streamlit application code.
- **backend/**: Contains the FastAPI backend server code.
- **tests/**: Contains the test cases for backend.
- **UI_overview/**: Contains pictures of UI.
- **requirements.txt**: Lists the required Python packages.
- **expense_manager_expenses.sql**: SQL dump to initialize the MySQL database.
- **README.md**: Provides an overview and instructions for the project.

---

## 🚀 Features

- ✅ Add, update, or delete expenses (set amount = 0 to delete)  
- 🔍 Filter by **date** or **month**  
- 📊 View as **table** or **category-wise chart**  
- 📈 Analytics by **category** for **date range** or **month**  
- 🧠 Intuitive, real-time UI  
- 📝 Logs all API requests to `server.log`  
- 🗂️ **Expense Passbook**: Paginated table of recent expenses  
- ➕ Set how many records to show in Passbook  
- 💡 See total spent for selected records  


---
## 🛠️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/expense-management-system.git
   cd expense-management-system
   ```
2. **Install dependencies:**   
   ```commandline
    pip install -r requirements.txt
   ```
3. **Set Up MySQL Database:**

- ✅ Make sure you have **MySQL Workbench** installed and running.
- ✅ Create a database named `expense_manager`.
- ✅ Import the `expense_manager_expenses.sql` file into your MySQL database using MySQL Workbench.
- ✅ Update your **FastAPI backend configuration** with the correct MySQL credentials in the file: **backend/db_helper.py**,
which contains the FastAPI backend server code.
- ✅ Make sure to set the following:

  - **Host**
  - **Username**
  - **Password**
  - **Database name**


4. **Run the FastAPI server:** 
   ```commandline
    cd backend
    uvicorn server:app --reload
   ```
5. **Run the Streamlit app:** 
   ```commandline
    streamlit run frontend/app.py
   ```
