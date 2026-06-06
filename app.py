import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# 1. Load data safely
try:
    df = pd.read_csv("./formatted_output.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date")
except FileNotFoundError:
    print("Error: 'formatted_output.csv' not found. Please verify Task 2 output.")
    df = pd.DataFrame(columns=["sales", "date", "region"])

# 2. Layout (With polished CSS styling applied inline)
app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        "backgroundColor": "#f4f6f9",
        "minHeight": "100vh",
        "padding": "40px 20px",
        "boxSizing": "border-box"
    },
    children=[
        # Main Container Block
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "backgroundColor": "#ffffff",
                "borderRadius": "12px",
                "boxShadow": "0 8px 24px rgba(149, 157, 165, 0.15)",
                "padding": "40px"
            },
            children=[
                # Header Section
                html.Header(
                    style={"textAlign": "center", "marginBottom": "40px"},
                    children=[
                        html.H1(
                            "Soul Foods: Pink Morsel Regional Sales Dashboard",
                            style={"color": "#1e293b", "fontSize": "32px", "fontWeight": "700", "margin": "0 0 10px 0"}
                        ),
                        html.P(
                            "Analyze sales patterns before and after the January 15, 2021 pricing strategy adjustment.",
                            style={"color": "#64748b", "fontSize": "16px", "margin": "0"}
                        )
                    ]
                ),

                # Control Filter Card Block
                html.Div(
                    style={
                        "backgroundColor": "#f8fafc",
                        "border": "1px solid #e2e8f0",
                        "borderRadius": "8px",
                        "padding": "20px 30px",
                        "marginBottom": "30px",
                        "textAlign": "center"
                    },
                    children=[
                        html.Label(
                            "Select Geographic Region Filter:",
                            style={"fontWeight": "600", "color": "#475569", "display": "block", "marginBottom": "12px", "fontSize": "15px"}
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": " All Regions ", "value": "all"},
                                {"label": " North ", "value": "north"},
                                {"label": " East ", "value": "east"},
                                {"label": " South ", "value": "south"},
                                {"label": " West ", "value": "west"}
                            ],
                            value="all", # Default value
                            inline=True,
                            style={"display": "flex", "justifyContent": "center", "gap": "25px"},
                            inputStyle={"marginRight": "8px", "transform": "scale(1.1)"},
                            labelStyle={"color": "#334155", "fontSize": "15px", "cursor": "pointer"}
                        )
                    ]
                ),

                # Graph Visualizer Wrapper
                html.Div(
                    style={"border": "1px solid #f1f5f9", "borderRadius": "8px", "padding": "10px"},
                    children=[
                        dcc.Graph(id="sales-line-chart")
                    ]
                )
            ]
        )
    ]
)

# 3. Dynamic Interactive Callbacks
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    # Filter dataset according to selection
    if selected_region == "all":
        filtered_df = df
        chart_title = "Pink Morsel Sales Performance — All Regions Aggregate"
    else:
        filtered_df = df[df["region"].str.strip().str.lower() == selected_region.lower()]
        chart_title = f"Pink Morsel Sales Performance — {selected_region.capitalize()} Region"

    # Re-render line graph configuration
    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title=chart_title,
        labels={"date": "Transaction Date", "sales": "Total Sales Revenue ($)"},
        template="plotly_white"
    )

    # Clean styling definitions for the Plotly data lines
    fig.update_traces(line_color="#3b82f6", line_width=2.5)
    
    fig.update_layout(
        title={"font": {"size": 18, "color": "#1e293b"}, "x": 0.02},
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Re-draw price increase milestone marker
    fig.add_vline(
        x="2021-01-15",
        line_width=2,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="Price Increase (Jan 15, 2021)",
        annotation_position="top left",
        annotation_font_color="#ef4444"
    )

    return fig

# Run engine
if __name__ == "__main__":
    app.run(debug=True)