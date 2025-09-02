from dotenv import load_dotenv
import cohere
import os

load_dotenv()

api_key = os.getenv('COHERE_API_KEY')
co = cohere.Client(api_key)

def get_budget_insights(user_query, transaction_text):
    prompt = f"""
User query: {user_query}
Transaction list: {transaction_text}

You are **BudgetBuddy**, a world-class AI financial analyst and personal money coach 
developed by Ayush Jain. Your role is to analyze a user's income and expense transactions 
and deliver *outstanding insights* that are accurate, practical, and easy to understand.

If the user asks about **yourself**, simply respond:
"I am BudgetBuddy, a financial assistant built by Ayush Jain to help with budgeting and expense management."
    """

    response = co.chat(
        model="command-r-plus",   # latest Cohere chat model
        message=prompt,
        max_tokens=300,
        temperature=0.7,
    )

    return response.text.strip()
