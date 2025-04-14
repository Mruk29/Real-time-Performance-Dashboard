from flask import Flask
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash
app = dash.Dash(__name__, server=server)

# Load dataset (Excel file)
df = pd.read_excel(r"D:\project\main copy internship.xlsx")

# Ensure column names are correct (trim spaces)
df.columns = df.columns.str.strip()

# Convert "month" to string (if needed)
df["month"] = df["month"].astype(str)

# Train Linear Regression Model for Productivity Gain
model = LinearRegression()
df_numeric = df[["Robots_Adopted", "Cost_Savings", "Jobs_Displaced", "Training_Hours", "Productivity_Gain"]].dropna()
X_train = df_numeric.drop(columns=["Productivity_Gain"])
y_train = df_numeric["Productivity_Gain"]
model.fit(X_train, y_train)

# Layout for Dashboard
app.layout = html.Div([
    html.H1("📊 Automation Performance Dashboard", style={'text-align': 'center'}),

    # Dropdown to filter by month
    html.Label("Select Month:", style={'font-size': '18px', 'font-weight': 'bold'}),
    dcc.Dropdown(
        id="month_filter",
        options=[{"label": m, "value": m} for m in sorted(df["month"].unique())],
        value=df["month"].unique()[0],  # Default selection
        clearable=False,
        style={'width': '50%'}
    ),

    # Graphs
    html.Div(className="graph-container", children=[
        dcc.Graph(id="robots_adopted_chart"),
        dcc.Graph(id="cost_savings_chart"),
        dcc.Graph(id="jobs_displaced_chart"),
        dcc.Graph(id="training_hours_chart"),
    ]),

    # Prediction Section
    html.H3("🔮 Predict Productivity Gain"),
    html.Label("Select Machine:", style={'font-size': '18px', 'font-weight': 'bold'}),
    dcc.Dropdown(
        id="machine_filter",
        options=[{"label": m, "value": m} for m in sorted(df["Machine Name"].unique())],
        clearable=False,
        style={'width': '50%'}
    ),
    html.Div(id="prediction_output", style={'font-size': '20px', 'font-weight': 'bold', 'margin-top': '10px'})
])


# Callback to update charts based on selected month
@app.callback(
    [Output("robots_adopted_chart", "figure"),
     Output("cost_savings_chart", "figure"),
     Output("jobs_displaced_chart", "figure"),
     Output("training_hours_chart", "figure")],
    [Input("month_filter", "value")]
)
def update_charts(selected_month):
    filtered_df = df[df["month"] == selected_month]

    # Robots Adopted Bar Chart
    fig1 = px.bar(filtered_df, x="Machine Name", y="Robots_Adopted", 
                  title="Robots Adopted by Machine Name", color="Machine Name")

    # Cost Savings Pie Chart
    fig2 = px.pie(filtered_df, values="Cost_Savings", names="Machine Name",
                  title="💰 Cost Savings Distribution by Machine Name")

    # Jobs Displaced Bar Chart
    fig3 = px.bar(filtered_df, x="Machine Name", y="Jobs_Displaced",
                  title="📊 Jobs Displaced by Machine",
                  color="Machine Name",
                  text_auto=True)  # Shows values on bars

    # Training Hours Box Plot
    fig4 = px.box(filtered_df, x="Machine Name", y="Training_Hours",
                  title="📚 Training Hours by Machine Name")

    return fig1, fig2, fig3, fig4


# Callback for Productivity Gain Prediction
@app.callback(
    Output("prediction_output", "children"),
    [Input("machine_filter", "value")]
)
def predict_productivity(machine_name):
    if not machine_name:
        return "Please select a machine."

    machine_data = df[df["Machine Name"] == machine_name][["Robots_Adopted", "Cost_Savings", "Jobs_Displaced", "Training_Hours"]].mean().values.reshape(1, -1)
    
    if machine_data.size == 0:
        return "Not enough data to make a prediction."

    predicted_productivity = model.predict(machine_data)[0]
    return f"📈 Predicted Productivity Gain: {predicted_productivity:.2f}"


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
