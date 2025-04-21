# Ticket Data Summary & Visualization App

## 🌟 Overview
This Streamlit application allows you to:

- **Upload** a single text file containing system ticket data.
- **Preprocess** and **clean** the data, filtering only relevant categories.
- **Map** categories to high‑level product groups (Broadband, Voice, TV, GIGA, VOD).
- **Generate AI‑powered storytelling summaries** for each product category, organized by chronological phases:
  1. Initial Issue
  2. Follow‑ups
  3. Developments
  4. Later Incidents
  5. Recent Events
- **Visualize** key trends with:
  - Time series of ticket volume
  - Bar chart of ticket counts by product
  - Pie chart of processing status distribution
- **Export** processed data, summaries, and charts for offline analysis.

## 🚀 Prerequisites
- **python 3.12**
- **Streamlit**
- **Pandas**
- **Altair**
- **Plotly**
- **Matplotlib**
- **OpenPyXL**
- **OpenAI Python client**
- **Python dotenv**

## 📦 Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/mahmoud-mohsen97/System_Ticket_Summary.git
   cd System_Ticket_Summary
   ```
2. **Create & activate** a virtual environment
   ```bash
   conda create --name system_env  python=3.12 
   conda activate system_env
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set your OpenAI API key** (if using GPT‑4 summarization)
   - Environment variable
     ```bash
     echo "OPENAI_API_KEY=your_api_key_here" > .env
     ```

## 📁 Project Structure
```
ticket_analysis_app/
│
├── .env                   # API keys
├── .gitignore             
├── app.py                 # Main Streamlit application
├── README.md              # documentation
├── requirements.txt       # Python dependencies
│
├── data/                  # Example/test data files
│   └── sample_ticket_data.txt
│
└── src/                   # Modular application logic
    ├── preprocessing.py   # Data loading & cleaning
    ├── summarizer.py      # LLM prompt & API calls
    ├── visualizations.py  # Charting functions
    └── export.py          # Export/download utilities

```

## 🎯 Usage Guide
1. **Run the app**
   ```bash
   streamlit run app.py
   ```
2. **Upload** your ticket data file (*.txt* format) via the sidebar.
3. **Review** the data preview: filtered ticket count, date range, and a sample of rows.
4. **Download** filtered data as CSV or Excel if desired.
5. **Explore visualizations**:
   - Time series of tickets over time
   - Bar chart of ticket counts by product
   - Pie chart of processing status
   Download charts directly via provided buttons.
6. **Generate AI Summaries** by clicking **Generate Summaries**. Wait for the analysis to finish.
7. **Read** each product’s narrative in expandable sections.
8. **Export** the combined summary report as a Markdown file.

## 🛠 Developer Guide
- **Entry point**: `app.py` orchestrates the UI and calls functions from `src/`.
- **Data pipeline**: `preprocessing.py` handles file parsing, date conversion, category filtering, and product mapping.
- **Summarization**: `summarizer.py` builds event lists, constructs LLM prompts, and retrieves summaries via the OpenAI API.
- **Visualization**: `visualizations.py` provides reusable chart functions using Altair and Plotly.
- **Export**: `export.py` offers utilities to serialize DataFrames and figures for download.

### Extending the App
- **Add new categories**: Update `categories` and `mapping` in `preprocessing.py`.
- **Change summarization logic**: Modify the prompt template in `summarizer.py` or adjust model parameters.
- **Customize charts**: Tweak `visualizations.py` functions or add new chart types.
- **Support additional exports**: Extend `export.py` to generate PDFs or Word documents (e.g., using `python-docx`).

## ❓ Troubleshooting
- **File won’t parse**: Ensure the text file is comma- or tab-delimited and has a header row matching expected column names.
- **Dates show as NaT**: Verify the date format (`MM/DD/YYYY HH:MM`) aligns with the sample data. Adjust `date_format` in `preprocessing.py` if needed.
- **Summarization fails**: Check your OpenAI API key, rate limits, or network connection. Review error messages in the terminal.
- **Charts not rendering**: Confirm dependencies (`altair`, `plotly`, `matplotlib`) are installed and up to date.
