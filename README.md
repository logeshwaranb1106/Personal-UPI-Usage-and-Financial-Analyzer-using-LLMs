# 💸 Personal UPI Usage and Financial Analyzer using LLMs

An AI-powered personal finance app that processes UPI transaction statements (Paytm, GPay, PhonePe, etc.) and delivers actionable insights and personalized financial advice using Large Language Models (LLMs).

---

## 🚀 Key Features

- 📄 Extracts and parses UPI PDF statements
- 🧹 Cleans and structures data: `Date`, `Time`, `Amount`, `Receiver`, `Description`, `Category`
- 📊 Analyzes spending habits and detects wasteful expenses
- 🧠 Generates personalized budget tips and financial recommendations using LLMs
- 🖥️ Interactive UI via **Streamlit** or **Gradio**
- ☁️ Deployable on **Hugging Face Spaces**

---

## 🛠️ Tech Stack

- **Python**, **Pandas**
- **pdfplumber** / **PyMuPDF** for PDF parsing
- **OpenAI API** / **Hugging Face Transformers**
- **Langflow** for LLM workflow chaining
- **Streamlit** / **Gradio**
- **Hugging Face Spaces** (Deployment)

---

## 📦 Installation & Running

```bash
# Clone the repo
git clone https://github.com/your-username/personal-upi-analyzer.git
cd personal-upi-analyzer

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py

# OR run Gradio app
python gradio_app.py

##📌 Use Cases
-✅ Unify and analyze UPI transactions from Paytm, PhonePe, GPay

-🔎 Identify spending patterns, top merchants, and unnecessary expenses

-💡 Get personalized monthly budget and saving tips

-📈 Monitor financial behavior across all apps in one dashboard

##🧾 Output Examples
-📁 CSV/JSON with structured transaction data

-📉 Graphs: Category-wise & time-based spend breakdowns

-🧠 LLM-generated financial recommendations:
--Budget planning

--Expense reduction tips

--Smart saving strategies

--Budget planning

--Expense reduction tips

--Smart saving strategies

##📈 Evaluation Metrics
-📊 PDF Parsing Accuracy – correctness of field extraction

-💬 LLM Insight Quality – relevance and helpfulness of advice

-🗂️ Data Completeness – all fields captured and normalized

-⚡ Response Speed – time taken for analysis and output

-👍 User Satisfaction – qualitative feedback from users

##🎯 Deliverables
-✅ Python codebase

-✅ Streamlit / Gradio-based UI

-✅ Deployed demo (Hugging Face Spaces)
