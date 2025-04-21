import io
import pandas as pd
import matplotlib.pyplot as plt


def get_csv_bytes(df):
    """
    Convert a DataFrame to CSV bytes for download.
    """
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue().encode('utf-8')


def get_excel_bytes(df):
    """
    Convert a DataFrame to Excel bytes for download.
    """
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Tickets')
    return excel_buffer.getvalue()


def get_summary_markdown(summaries):
    """
    Combine product summaries dict into a single markdown report.

    summaries: dict mapping product_name -> summary_text
    """
    md = []
    for prod, text in summaries.items():
        md.append(f"## {prod} Summary\n")
        md.append(text)
        md.append("\n---\n")
    return "\n".join(md).strip().encode('utf-8')


def save_matplotlib_fig(fig, fmt='png'):
    """
    Save a Matplotlib figure to bytes for download.

    Parameters:
        fig: matplotlib.figure.Figure
        fmt: image format (e.g. 'png', 'pdf')
    """
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, bbox_inches='tight')
    buf.seek(0)
    return buf.getvalue()


def save_plotly_fig(fig):
    """
    Save a Plotly figure to PNG bytes (requires kaleido).
    """
    # Ensure kaleido is installed
    img_bytes = fig.to_image(format="png")
    return img_bytes
