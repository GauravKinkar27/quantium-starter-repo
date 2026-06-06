import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# 1. Load and prepare the processed data
try:
    df = pd.read_csv("./formatted_output.csv")
    # Ensure date column is treated as a datetime object for proper plotting
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date")
except FileNotFoundError:
    print("Error: 'formatted_output.csv' not found. Please run your data processing script first!")
    df = pd.DataFrame(columns=["sales", "date", "region"])

# 2. Create the Plotly Express Line Chart
fig = px.line(
    df, 
    x="date", 
    y="sales", 
    title="Pink Morsel Sales Performance (Over Time)",
    labels={"date": "Date of Transaction", "sales": "Total Revenue ($)"},
    template="plotly_white"
)

# Customize line aesthetics and add a vertical reference line for the price increase
fig.update_traces(line_color="#e06666", line_width=2.5)

# Add a dashed vertical line on January 15, 2021 (The Price Increase Date)
fig.add_vline(
    x="2021-01-15", 
    line_width=2, 
    line_dash="dash", 
    line_color="#333333",
    annotation_text="Price Increase (Jan 15, 2021)", 
    annotation_position="top left"
)

# 3. Define the HTML Layout of the Page
app.layout = html.Div(
    style={
        "fontFamily": "Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
        "backgroundColor": "#f9f9f9",
        "padding": "40px",
        "maxWidth": "1100px",
        "margin": "0 auto"
    },
    children=[
        # App Header
        html.H1(
            children="Soul Foods: Pink Morsel Sales Visualizer",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "10px",
                "fontWeight": "600"
            }
        ),
        
        # Subheading descriptive block
        html.P(
            children="An interactive data tool analyzing the financial impact of the January 15th, 2021 price realignment strategy.",
            style={
                "textAlign": "center",
                "color": "#7f8c8d",
                "marginBottom": "40px"
            }
        ),
        
        # Container holding the Graph component
        html.Div(
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "8px",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"
            },
            children=[
                dcc.Graph(
                    id="sales-line-chart",
                    figure=fig
                )
            ]
        )
    ]
)

# 4. Run the web server locally
if __name__ == "__main__":
    app.run(debug=True)