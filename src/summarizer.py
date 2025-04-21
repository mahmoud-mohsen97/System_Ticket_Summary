import os
import pandas as pd
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def build_event_list(df, date_col='ACCEPTANCE_TIME', id_col='ORDER_NUMBER', desc_cols=None):
    """
    Construct a chronological list of ticket events for LLM input.

    Parameters:
        df: pd.DataFrame for a single product group, sorted by date
        date_col: str, name of the datetime column
        id_col: str, name of the ticket ID column
        desc_cols: list of str, columns containing descriptive text

    Returns:
        str: formatted event list
    """
    if desc_cols is None:
        desc_cols = []
    events = []
    for _, row in df.iterrows():
        date_str = row[date_col].strftime('%Y-%m-%d')
        ticket_id = row[id_col]
        # combine description fields if provided
        desc = " ".join(str(row[c]) for c in desc_cols if c in row and pd.notna(row[c]))
        events.append(f"- [{date_str}] Ticket {ticket_id}: {desc}")
    return "\n".join(events)


def prompt_for_product(product_name, event_list_text):
    """
    Build the LLM prompt for a single product category summary.
    """
    return f"""
Your task is to summarize the history of issues for the product: {product_name}.

I will provide a chronological list of ticket events, including dates and ticket IDs with brief details.

Please write a narrative summary organized into the following sections (use headings):

1. Initial Issue
2. Follow-ups
3. Developments
4. Later Incidents
5. Recent Events

For each section, include:
- Timeframe (e.g., months or date range)
- Related ticket IDs
- A narrative description of what happened in that phase.

Here are the events:
{event_list_text}

Generate the structured summary now.
""".strip()


def summarize_product(df, product_name,
                      date_col='ACCEPTANCE_TIME',
                      id_col='ORDER_NUMBER',
                      desc_cols=None,
                      model="gpt-4o-mini"):
    """
    Generate a storytelling summary for a single product group using the LLM.

    Parameters:
        df: pd.DataFrame subset for the product, sorted by date
        product_name: str, name of the product
        date_col, id_col, desc_cols: see build_event_list
        model: str, LLM model name

    Returns:
        str: LLM-generated summary text
    """
    # Build the event list text
    events_text = build_event_list(df, date_col, id_col, desc_cols)

    # Construct the prompt
    prompt = prompt_for_product(product_name, events_text)

    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)
    
    # Call the OpenAI ChatCompletion API
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "You are an experienced support analyst generating a chronological incident report."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024,
    )
    summary = response.choices[0].message.content
    return summary


def summarize_all_products(df, product_col='Product', **kwargs):
    """
    Generate summaries for every unique product group in the DataFrame.

    Parameters:
        df: pd.DataFrame, full preprocessed data
        product_col: str, column name for product grouping
        **kwargs: arguments forwarded to summarize_product

    Returns:
        dict: mapping product_name -> summary string
    """
    summaries = {}
    for product in df[product_col].unique():
        sub_df = df[df[product_col] == product].copy()
        # ensure chronological order
        sub_df = sub_df.sort_values(kwargs.get('date_col', 'ACCEPTANCE_TIME'))
        summaries[product] = summarize_product(sub_df, product, **kwargs)
    return summaries
