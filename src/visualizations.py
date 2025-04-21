import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px


def plot_ticket_volume_over_time(df, date_col='ACCEPTANCE_TIME', freq='D'):
    """
    Generate an Altair line chart of ticket volume over time, aggregated by a given frequency.

    Parameters:
        df: pd.DataFrame with parsed datetime column
        date_col: str, name of the datetime column
        freq: str, pandas frequency string (e.g. 'D', 'W', 'M')

    Returns:
        alt.Chart object
    """
    # Create period column
    df_period = df.copy()
    df_period['Period'] = df_period[date_col].dt.to_period(freq).dt.to_timestamp()
    agg = df_period.groupby('Period').size().reset_index(name='TicketCount')

    chart = alt.Chart(agg).mark_line(point=True).encode(
        x=alt.X('Period:T', title='Date'),
        y=alt.Y('TicketCount:Q', title='Number of Tickets'),
        tooltip=['Period:T', 'TicketCount:Q']
    ).properties(
        title='Ticket Volume Over Time'
    )
    return chart


def plot_tickets_by_product(df, product_col='Product'):
    """
    Generate an Altair bar chart of ticket counts by product category.

    Parameters:
        df: pd.DataFrame containing a 'Product' column
        product_col: str, name of the product grouping column

    Returns:
        alt.Chart object
    """
    agg = df[product_col].value_counts().reset_index()
    agg.columns = ['Product', 'TicketCount']

    chart = alt.Chart(agg).mark_bar().encode(
        x=alt.X('Product:N', sort='-y', title='Product Category'),
        y=alt.Y('TicketCount:Q', title='Number of Tickets'),
        tooltip=['Product:N', 'TicketCount:Q']
    ).properties(
        title='Tickets by Product Category'
    )
    return chart


def plot_status_pie(df, status_col='PROCESSING_STATUS'):
    """
    Generate a Plotly pie chart showing distribution of ticket processing statuses.

    Parameters:
        df: pd.DataFrame with a status column
        status_col: str, name of the column to aggregate

    Returns:
        plotly.graph_objects.Figure object
    """
    counts = df[status_col].value_counts().reset_index()
    counts.columns = ['Status', 'Count']

    fig = px.pie(
        counts,
        names='Status',
        values='Count',
        title='Ticket Processing Status Distribution',
        hole=0.3
    )
    return fig
