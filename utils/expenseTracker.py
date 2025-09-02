import sqlite3
import pandas as pd
import streamlit as st

# expense manager class using the db

class ExpenseManager:



    def __init__(self,db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()


        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses( 
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT,
                               date DATE,
                               amount REAL,
                               category TEXT,
                               description TEXT
                            )
                            ''')
        self.conn.commit()
    def addExpense(self,date,name,amount,category,description):
        self.cursor.execute('''INSERT INTO EXPENSES(name,date,amount,category,description)
                               VALUES (?,?,?,?,?)''',
                               (name,date,amount,category,description))
        self.conn.commit()

    def viewExpense(self):
        query = "SELECT * FROM expenses"
        return pd.read_sql(query,self.conn)
    
    def deleteExpense(self,expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id = ?",(expense_id,))
        self.conn.commit()

class IncomeManager:
    def __init__(self,db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # creating the table if it dosent exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS income(
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT,
                               date DATE,
                               amount REAL,
                               source TEXT,
                               description TEXT)''')
        self.conn.commit()

    def addIncome(self,date,name,amount,source,description):
        self.cursor.execute('''INSERT INTO income(name,date,amount,source,description)
                               VALUES(?,?,?,?,?)''',
                               (name,date,amount,source,description))
        self.conn.commit()

    def viewIncome(self):
        query = "SELECT * FROM INCOME"
        return pd.read_sql(query,self.conn)
    
    def deleteIncome(self,income_id):
        self.cursor.execute("DELETE FROM income WHERE id = ?",(income_id,))
        self.conn.commit()

class Account:

    def __init__(self,db_name):
        self.IncomeManager = IncomeManager(db_name)
        self.ExpenseManager = ExpenseManager(db_name)
        self.balance = 0.0

    def getBalance(self):
        total_income = self.IncomeManager.viewIncome()['amount'].sum()
        total_expense = self.ExpenseManager.viewExpense()['amount'].sum()
        self.balance = total_income - total_expense
        return self.balance
    
    def addExpense(self,date,name,amount,category,description):
        self.ExpenseManager.addExpense(date,name,amount,category,description)
        self.balance -= amount
        st.success(f"Expense added Successfully!")

    def addIncome(self,date,name,amount,source,description):
        self.IncomeManager.addIncome(date,name,amount,source,description)
        self.balance += amount
        st.success(f"Income added Successfully!")

    def expenseList(self):
        return self.ExpenseManager.viewExpense()

    def incomeList(self):
        return self.IncomeManager.viewIncome()
    
    def deleteExpense(self,expense_id):
        expenses = self.ExpenseManager.viewExpense()
        if expenses.empty:
            st.warning('No expenses to delete!')
            return
        
        if expense_id in expenses['id'].values:
            amount = expenses.loc[expenses['id'] == expense_id,"amount"].iloc[0]
            self.ExpenseManager.deleteExpense(expense_id)
            self.balance += amount
            st.success(f"Expense {expense_id} deleted succesfully!")

        else:
            st.warning(f"Invalid Expense Id: {expense_id}")

    def deleteIncome(self,income_id):
        incomes = self.IncomeManager.viewIncome()
        if incomes.empty:
            st.warning("No income to delete!")
            return
        
        if income_id in incomes['id'].values:
            amount = incomes.loc[incomes['id'] == income_id,"amount"].iloc[0]
            self.IncomeManager.deleteIncome(income_id)
            self.balance -= amount
            st.success(f"Income {income_id} deleted succesfully!")

        else:
            st.warning(f"Invalid Income Id: {income_id}")
    
    def format_transactions_for_AI(self):
        expenses = self.ExpenseManager.viewExpense()
        incomes = self.IncomeManager.viewIncome()


        formatted_expenses = expenses[["name","date","amount","category","description"]].to_dict(orient = 'records')
        formatted_income = incomes[["name","date","amount","source","description"]].to_dict(orient = 'records')

        transactions = {
            'income' : formatted_income,
            'expenses' : formatted_expenses
        }


        return transactions

