import os
import streamlit as st
import PyPDF2
import google.generativeai as genai
import plotly.express as px
import pandas as pd
import time  # Import time for progress bar

# Set up Google Gemini API Key
GEMINI_API_KEY = "AIzaSyAgO5I6sN-2euuM_ZeomQG-ZVZ2EYqEOA4"
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit UI
st.set_page_config(page_title="AI Personal Finance Assistant", page_icon="💰", layout="wide")

# Sidebar with usage info
st.sidebar.title("ℹ️ How to Use This Tool?")
st.sidebar.write("- Upload your (Paytm, Gpay, PhonePe or UPI) Transaction History PDF.")
st.sidebar.write("- The AI will analyze your transactions.")
st.sidebar.write("- You will receive financial insights including income, expenses, savings, spending trends, and advice.")
st.sidebar.write("- Use this data to plan your finances effectively.")

# Main title and subtitle
st.title("💰 AI-Powered Personal Finance Assistant")
st.subheader("Upload your (Paytm, Gpay, PhonePe or UPI) Transaction History PDF for Financial Insights")

# Upload PDF File
uploaded_file = st.file_uploader("📂 Upload PDF File", type=["pdf"], help="Only PDF files are supported")

def extract_text_from_pdf(file_path):
    """Extracts text from the uploaded PDF file."""
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def analyze_financial_data(text):
    """Sends extracted text to Google Gemini AI for financial insights."""
    model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
    prompt = f"""
    Analyze the following Paytm or UPI transaction history and generate financial insights:
    {text}
    Provide a detailed breakdown in the following format:
    **Financial Insights for [User Name]**

    **Key Details:**

    - **Overall Monthly Income & Expenses:**
      - Month: [Month]
      - Income: ₹[Amount]
      - Expenses: ₹[Amount]

    - **Unnecessary Expenses Analysis:**
      - Expense Category: [Category Name]
      - Amount: ₹[Amount]
      - Recommendation: [Suggestion]

    - **Savings Percentage Calculation:**
      - Savings Percentage: [Percentage] %

    - **Expense Trend Analysis:**
      - Notable Trends: [Trend Details]

    - **Cost Control Recommendations:**
      - Suggestion: [Detailed Suggestion]
      
    - **Category-Wise Spending Breakdown:**
      - Category: [Category Name] - ₹[Amount]
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠️ Error processing financial data."

def generate_visualizations(data):
    """Generates interactive visualizations for the financial data using Plotly."""
    # Convert data into a DataFrame for plotting
    df = pd.DataFrame(data)

    # Spending by Category Visualization (Bar Chart)
    bar_fig = px.bar(df, x='Category', y='Amount',title="Spending by Category", labels={'Amount': 'Amount (₹)'})
    st.plotly_chart(bar_fig)

    # Income vs Expenses Visualization (Bar Chart)
    income_expenses_fig = px.bar(x=['Income', 'Expenses'], y=[df['Income'][0], df['Expenses'][0]], 
                                 title="Income vs Expenses", labels={'y': 'Amount (₹)', 'x': ''})
    st.plotly_chart(income_expenses_fig)

    # Savings vs Expenses Visualization (Bar Chart)
    savings_percentage = df['Savings'][0]
    expense_percentage = 100 - savings_percentage
    savings_expenses_fig = px.bar(x=['Savings', 'Expenses'], y=[savings_percentage, expense_percentage],
                                  title="Savings vs Expenses", labels={'y': 'Percentage (%)', 'x': ''})
    st.plotly_chart(savings_expenses_fig)

    # Spending by Category (Pie Chart)
    pie_fig = px.pie(df, names='Category', values='Amount', title="Spending Distribution by Category", 
                     color='Category', color_discrete_sequence=px.colors.qualitative.Set3)
    pie_fig.update_traces(textinfo='percent+label')  # Show percentage and label on pie chart
    pie_fig.update_layout(height=600, width=600)  # Set size of pie chart
    st.plotly_chart(pie_fig)

def display_advice_and_trends(insights):
    """Display advice and trends based on the AI analysis."""
    # Extracting relevant advice and trends from the generated insights
    lines = insights.split('\n')
    advice = []
    trends = []

    for line in lines:
        if "Recommendation" in line:
            advice.append(line)
        elif "Notable Trends" in line:
            trends.append(line)

    if advice:
        st.subheader("💡 Cost Control & Savings Advice")
        for a in advice:
            st.write(a)

    if trends:
        st.subheader("📊 Spending Trends & Patterns")
        for t in trends:
            st.write(t)

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text from document..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠️ Failed to extract text. Ensure the document is not a scanned image PDF.")
    else:
        progress_bar = st.progress(0)
        with st.spinner("🧠 AI is analyzing your financial data..."):
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.05)  # Simulate work being done
            insights = analyze_financial_data(extracted_text)

        progress_bar.progress(100)

        st.subheader("📊 Financial Insights Report")
        st.write(f"📄 Financial Report for {uploaded_file.name}")
        st.write(insights)

        # Example data for visualization (this would normally come from the AI's analysis)
        example_data = {
            'Category': ['Groceries', 'Entertainment', 'Transport', 'Rent', 'Utilities'],
            'Amount': [5000, 3000, 2000, 12000, 1500],
            'Income': [25000, 25000, 25000, 25000, 25000],  # Same income for all categories
            'Expenses': [21500, 21500, 21500, 21500, 21500],  # Same expenses for all categories
            'Savings': [3500, 3500, 3500, 3500, 3500]  # Same savings for all categories
        }
        generate_visualizations(example_data)

        # Display cost control advice and spending trends
        display_advice_and_trends(insights)

        st.success("🎉 Analysis Completed! Plan your finances wisely. 🚀")
        st.balloons()

    try:
        os.remove(file_path)  # Cleanup
    except Exception as e:
        st.error(f"⚠️ Failed to clean up the file: {str(e)}")