import streamlit as st
from src.preprocessing import preprocess_data
from src.summarizer import summarize_all_products
from src.visualizations import (
    plot_ticket_volume_over_time,
    plot_tickets_by_product,
    plot_status_pie
)
from src.export import (
    get_csv_bytes,
    get_excel_bytes,
    get_summary_markdown,
    save_matplotlib_fig,
    save_plotly_fig
)

st.set_page_config(page_title="Ticket Data Analysis", layout="wide")

st.title("🎫 Ticket Data Summary & Visualization App")

# Sidebar for file upload and options
st.sidebar.header("Upload & Settings")
uploaded_file = st.sidebar.file_uploader(
    "Upload ticket data file (text)", type=["txt"], accept_multiple_files=False
)

# Process once file is uploaded
if uploaded_file is not None:
    # Preprocess data
    with st.spinner("Preprocessing data..."):
        df = preprocess_data(uploaded_file)
    
    # Show data summary
    st.subheader("Data Preview & Export")
    st.write(f"Total tickets (filtered): {len(df)}")
    st.write(f"Date range: {df['ACCEPTANCE_TIME'].min().date()} to {df['ACCEPTANCE_TIME'].max().date()}")
    st.dataframe(df.head(10))

    # Export raw and filtered data
    csv_bytes = get_csv_bytes(df)
    excel_bytes = get_excel_bytes(df)
    st.download_button("Download Filtered Data (CSV)", data=csv_bytes, file_name="filtered_tickets.csv", mime="text/csv")
    st.download_button("Download Filtered Data (Excel)", data=excel_bytes, file_name="filtered_tickets.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Visualizations
    st.subheader("Visualizations")
    # Time series
    ts_chart = plot_ticket_volume_over_time(df)
    st.altair_chart(ts_chart, use_container_width=True)

    # Bar & Pie charts side by side
    col1, col2 = st.columns(2)
    with col1:
        bar_chart = plot_tickets_by_product(df)
        st.altair_chart(bar_chart, use_container_width=True)
    with col2:
        pie_fig = plot_status_pie(df)
        st.plotly_chart(pie_fig, use_container_width=True)

    # Downloads for visualizations
    # Pie chart download
    pie_png = save_plotly_fig(pie_fig)
    st.download_button("Download Status Pie Chart", data=pie_png, file_name="status_pie.png", mime="image/png")

    st.download_button("Download Time Series Data (CSV)", data=ts_chart.data.to_csv(index=False).encode('utf-8'), file_name="timeseries.csv", mime="text/csv")

    # Summarization
    st.subheader("AI-Powered Summaries")
    if st.button("Generate Summaries", type="primary"):
        with st.spinner("Generating summaries (this may take a moment 😅)..."):
            # Call the summarize_all_products function directly
            summaries = summarize_all_products(df, desc_cols=['ORDER_DESCRIPTION_1', 'ORDER_DESCRIPTION_2', 'NOTE_MAXIMUM'])
            
        # Display summaries
        for product, text in summaries.items():
            with st.expander(f"{product} Summary", expanded=False):
                st.markdown(text)

        # Download summary report
        report_md = get_summary_markdown(summaries)
        st.download_button("Download Summary Report (Markdown)", data=report_md, file_name="ticket_summaries.md", mime="text/markdown")
else:
    st.info("Please upload a ticket data text file to begin analysis.")
