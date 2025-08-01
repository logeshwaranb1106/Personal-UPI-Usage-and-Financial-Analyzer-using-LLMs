import streamlit as st
import PyPDF2
import google.generativeai as genai

# --- Set your Google Gemini API key ---
GEMINI_API_KEY = "AIzaSyBrtKI8noISjUW3uINkGEHNO2lC5P7Rr0Y"  
genai.configure(api_key=GEMINI_API_KEY)

# --- Streamlit page setup ---
st.set_page_config(page_title="AI Personal Financial Analyzer", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for centering the title ---
st.markdown(
    """
    <style>
    .center-title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="center-title">🤖 AI Personal Financial Analyzer</h1>', unsafe_allow_html=True)

st.markdown('<p class="center-title" style="font-size:20px;">Upload your UPI Transaction History PDF to get smart financial insights.</p>', unsafe_allow_html=True)


# --- Custom CSS for styling ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e6f0ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar content ---
with st.sidebar:
    st.header("📌 How to use this app")
    st.markdown("""
    1️⃣ Upload your UPI transaction PDF
    2️⃣ Wait for text extraction ⏳  
    3️⃣ AI will analyze and give insights 🧠  
    4️⃣ Review your **monthly summary**, **spending habits**, and **tips**  
    ⚠️ **Note:**  
    - Upload clear PDF statements only (not scanned images).  
    - No sensitive info is stored.  
    """)


# --- Upload the PDF file ---
uploaded_file = st.file_uploader("📂 Upload a PDF File", type="pdf")

# --- Function to extract text from the uploaded PDF ---
def extract_text(uploaded_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        st.error(f"⚠️ Could not read PDF: {e}")
    return text.strip()

# --- Function to analyze the extracted text using Gemini AI ---
def analyze_financial_data(text):
    prompt = f"""
    You are a trusted personal finance advisor. A user has uploaded their UPI transaction history in raw text form. 
Your job is to deeply analyze this data and give insights that can help them improve their financial habits. Your analysis must include:
###💡 1️⃣ Monthly Summary
- Total Transactions
- Total Income
- Total Expenses
- Net Savings (Income - Expenses)
- Savings Rate (as % of Income)
**### Table format:**
| Month | Total Transactions | Total Income | Total Expenses | Net Savings | Savings Rate (%) |
|-------|--------------------|--------------|----------------|-------------|------------------|
**## If the user has no transactions, mention that clearly.**
| **Total** |                    |              |                |             |                  |
**make the total row bold.**
###💡 2️⃣ Spending Breakdown
- Category-wise total amounts (e.g., Food, Travel, Shopping, Utilities, Others)
- Highlight the biggest spending category
**### Table format:**
| Category   | Total Amount | Description |
|------------|--------------|-------------|
| Food       |              |             |
| Travel     |              |             |
| Shopping   |              |             |
| Utilities  |              |             |
| Others     |              |             |
| **Total**  |              |             |
###💡 Special Instruction:
- If the total spending under the "Others" category is **more than any other category**, analyze and try to **split it into more specific subcategories** using the transaction descriptions.
- Display the split subcategories under a separate table called **"Others Breakdown"**.
- If no meaningful split is possible, just keep "Others" as is.
** highlight the high spending category by bolding it.**                                                                                           
###💡 3️⃣ Hidden Patterns & Insights
- Are there any frequent small spends that add up?
- Are there impulse or irregular purchases?
- Identify peak spending days/times or trends (weekends, nights)
- Any unusual patterns that stand out?
**### Table format:**
| Insight Type          | Description |
|-----------------------|-------------|
| Frequent Small Spends |             |
| Impulse Purchases     |             |
| Irregular Purchases   |             |
| Peak Spending Days    |             |
| Unusual Patterns      |             |
**## If no patterns are found, mention that clearly.**
**highlight the important words in bold.**
###💡 4️⃣ Smart Suggestions
- Personalized tips to reduce wasteful spending
- Simple budget strategy based on their habits
- How to improve savings and set realistic goals
**### Table format:**
| Suggestion Type           | Description |
|---------------------------|-------------|
| Reduce Wasteful Spending  |             |
| Budget Strategy           |             |
| Improve Savings           |             |
| Set Goals                 |             |
**## If no suggestions are found, mention that clearly.**
###💡 5️⃣ One Motivational Quote
- End with a short, positive quote about financial discipline (don’t repeat quotes).
Here is the user's raw transaction data:
{text}
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        if response:
            return response.text.strip()
        else:
            return "⚠️ No response from Gemini."
    except Exception as e:
        return f"⚠️ Gemini API Error: {e}"

# --- Main app logic ---
if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text from PDF..."):
        text = extract_text(uploaded_file)

    if not text:
        st.error("⚠️ No text could be extracted. Please check your PDF file.")
    else:
        with st.spinner("🧠 Analyzing your financial data..."):
            result = analyze_financial_data(text)

        st.subheader("📊 Financial Insights")
        st.write(result)

        st.success("🎉 Analysis complete! Use these insights to improve your finances.")
        st.balloons()

