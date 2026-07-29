# Employee Attrition Analysis Dashboard

# Methodology
# 1. Load and clean the dataset
# 2. Define color palette and typography
# 3. Prepare title case display labels
# 4. Build KPI summary cards
# 5. Build interactive filters
# 6. Build attrition visual charts
# 7. Assemble layout and register callbacks

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Step 1 load and clean the dataset
df = pd.read_csv("attrition_dataset.csv")
df.columns = df.columns.str.strip()
df["OverTimeDisplay"] = df["OverTime"].map({"Yes": "Overtime", "No": "No Overtime"})

# Step 2 define color palette and typography
COLORS = {
    "background": "#f2f4f7",
    "panel": "#ffffff",
    "text": "#1f2933",
    "muted": "#7b8794",
    "accent": "#2f6690",
    "accent_alert": "#c9564f",
}
FONT_FAMILY = "Arial, Helvetica, sans serif"
CHART_TITLE_SIZE = 18
AXIS_TITLE_SIZE = 13

# Step 3 prepare title case display labels
department_options = sorted(df["Department"].unique())
gender_options = sorted(df["Gender"].unique())

def apply_chart_theme(fig, title_text):
    # Apply shared typography and color rules to a chart
    fig.update_layout(
        title=dict(
            text=f"<b>{title_text}</b>",
            x=0.5,
            font=dict(size=CHART_TITLE_SIZE, color=COLORS["text"], family=FONT_FAMILY),
        ),
        paper_bgcolor=COLORS["panel"],
        plot_bgcolor=COLORS["panel"],
        font=dict(family=FONT_FAMILY, size=AXIS_TITLE_SIZE, color=COLORS["muted"]),
        legend=dict(font=dict(size=AXIS_TITLE_SIZE, color=COLORS["muted"])),
        margin=dict(t=60, b=40, l=40, r=20),
    )
    fig.update_xaxes(
        title_font=dict(size=AXIS_TITLE_SIZE, color=COLORS["muted"]),
        tickfont=dict(size=AXIS_TITLE_SIZE, color=COLORS["muted"]),
    )
    fig.update_yaxes(
        title_font=dict(size=AXIS_TITLE_SIZE, color=COLORS["muted"]),
        tickfont=dict(size=AXIS_TITLE_SIZE, color=COLORS["muted"]),
    )
    return fig

# Step 4 build KPI summary cards
def kpi_card(label_text, value_id):
    return html.Div(
        [
            html.Div(label_text, style={
                "fontSize": "16px",
                "color": COLORS["muted"],
                "display": "block",
                "marginBottom": "6px",
            }),
            html.Div(id=value_id, style={
                "fontSize": "30px",
                "fontWeight": "bold",
                "color": COLORS["text"],
            }),
        ],
        style={
            "backgroundColor": COLORS["panel"],
            "borderRadius": "10px",
            "padding": "18px",
            "flex": "1",
            "marginRight": "16px",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.08)",
        },
    )

# Step 5 build interactive filters
filters_section = html.Div(
    [
        html.Div(
            [
                html.Label("Department", style={
                    "fontSize": "16px",
                    "color": COLORS["text"],
                    "display": "block",
                    "marginBottom": "6px",
                }),
                dcc.Dropdown(
                    id="department_filter",
                    options=[{"label": d.title(), "value": d} for d in department_options],
                    value=None,
                    placeholder="All Departments",
                    style={"fontSize": "16px"},
                ),
            ],
            style={"flex": "1", "marginRight": "20px"},
        ),
        html.Div(
            [
                html.Label("Gender", style={
                    "fontSize": "16px",
                    "color": COLORS["text"],
                    "display": "block",
                    "marginBottom": "6px",
                }),
                dcc.RadioItems(
                    id="gender_filter",
                    options=[{"label": g.title(), "value": g} for g in gender_options],
                    value=None,
                    labelStyle={"fontSize": "16px", "marginRight": "14px", "color": COLORS["text"]},
                ),
            ],
            style={"flex": "1", "marginRight": "20px"},
        ),
        html.Div(
            [
                html.Label("Overtime Status", style={
                    "fontSize": "16px",
                    "color": COLORS["text"],
                    "display": "block",
                    "marginBottom": "6px",
                }),
                dcc.Checklist(
                    id="overtime_filter",
                    options=[{"label": "Overtime", "value": "Yes"}, {"label": "No Overtime", "value": "No"}],
                    value=["Yes", "No"],
                    labelStyle={"fontSize": "16px", "marginRight": "14px", "color": COLORS["text"]},
                ),
            ],
            style={"flex": "1"},
        ),
    ],
    style={
        "display": "flex",
        "backgroundColor": COLORS["panel"],
        "borderRadius": "10px",
        "padding": "18px",
        "marginBottom": "24px",
        "boxShadow": "0 1px 3px rgba(0,0,0,0.08)",
    },
)

# Step 6 build attrition visual charts
charts_row_one = html.Div(
    [
        dcc.Graph(id="attrition_by_department", style={"flex": "1", "marginRight": "16px"}),
        dcc.Graph(id="attrition_by_jobrole", style={"flex": "1"}),
    ],
    style={"display": "flex", "marginBottom": "24px"},
)

charts_row_two = html.Div(
    [
        dcc.Graph(id="age_distribution", style={"flex": "1", "marginRight": "16px"}),
        dcc.Graph(id="income_by_attrition", style={"flex": "1"}),
    ],
    style={"display": "flex", "marginBottom": "24px"},
)

charts_row_three = html.Div(
    [
        dcc.Graph(id="attrition_by_overtime", style={"flex": "1"}),
    ],
    style={"display": "flex", "marginBottom": "24px"},
)

# Step 7 assemble layout and register callbacks
from dash import Dash

app = Dash(__name__)
server = app.server

app.title = "Employee Attrition Dashboard"

app.index_string = """
<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>Employee Attrition Dashboard</title>
{%favicon%}
{%css%}
<style>
* { font-family: Arial, Helvetica, sans-serif; }
body { font-family: Arial, Helvetica, sans-serif; margin: 0; }
</style>
</head>
<body>
{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
"""

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Employee Attrition Dashboard", style={
                    "fontSize": "34px",
                    "color": COLORS["text"],
                    "marginBottom": "4px",
                }),
                html.P("A view of workforce attrition patterns and drivers", style={
                    "fontSize": "18px",
                    "color": COLORS["muted"],
                    "marginTop": "0px",
                }),
            ],
            style={"marginBottom": "20px"},
        ),
        html.Div(
            [
                kpi_card("Total Employees", "kpi_total"),
                kpi_card("Attrition Rate", "kpi_attrition_rate"),
                kpi_card("Average Monthly Income", "kpi_avg_income"),
                kpi_card("Average Years At Company", "kpi_avg_tenure"),
            ],
            style={"display": "flex", "marginBottom": "24px"},
        ),
        filters_section,
        charts_row_one,
        charts_row_two,
        charts_row_three,
    ],
    style={
        "backgroundColor": COLORS["background"],
        "padding": "28px",
        "fontFamily": FONT_FAMILY,
        "minHeight": "100vh",
    },
)

def filter_data(department, gender, overtime_values):
    # Filter dataframe based on selected filter values
    filtered = df.copy()
    if department:
        filtered = filtered[filtered["Department"] == department]
    if gender:
        filtered = filtered[filtered["Gender"] == gender]
    if overtime_values:
        filtered = filtered[filtered["OverTime"].isin(overtime_values)]
    return filtered

@app.callback(
    Output("kpi_total", "children"),
    Output("kpi_attrition_rate", "children"),
    Output("kpi_avg_income", "children"),
    Output("kpi_avg_tenure", "children"),
    Output("attrition_by_department", "figure"),
    Output("attrition_by_jobrole", "figure"),
    Output("age_distribution", "figure"),
    Output("income_by_attrition", "figure"),
    Output("attrition_by_overtime", "figure"),
    Input("department_filter", "value"),
    Input("gender_filter", "value"),
    Input("overtime_filter", "value"),
)
def update_dashboard(department, gender, overtime_values):
    # Update KPIs and charts from current filter state
    filtered = filter_data(department, gender, overtime_values)

    total_employees = len(filtered)
    attrition_rate = (filtered["Attrition"] == "Yes").mean() * 100 if total_employees else 0
    avg_income = filtered["MonthlyIncome"].mean() if total_employees else 0
    avg_tenure = filtered["YearsAtCompany"].mean() if total_employees else 0

    kpi_total_text = f"{total_employees:,}"
    kpi_rate_text = f"{attrition_rate:.1f}%"
    kpi_income_text = f"${avg_income:,.0f}"
    kpi_tenure_text = f"{avg_tenure:.1f} Years"

    dept_summary = (
        filtered.groupby("Department")["Attrition"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="AttritionRate")
    )
    dept_summary["DepartmentDisplay"] = dept_summary["Department"].str.title()
    fig_department = px.bar(
        dept_summary,
        x="DepartmentDisplay",
        y="AttritionRate",
        color_discrete_sequence=[COLORS["accent"]],
    )
    fig_department.update_xaxes(title_text="Department")
    fig_department.update_yaxes(title_text="Attrition Rate Percent")
    apply_chart_theme(fig_department, "Attrition Rate By Department")

    role_summary = (
        filtered.groupby("JobRole")["Attrition"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="AttritionRate")
        .sort_values("AttritionRate")
    )
    role_summary["JobRoleDisplay"] = role_summary["JobRole"].str.title()
    fig_role = px.bar(
        role_summary,
        x="AttritionRate",
        y="JobRoleDisplay",
        orientation="h",
        color_discrete_sequence=[COLORS["accent"]],
    )
    fig_role.update_xaxes(title_text="Attrition Rate Percent")
    fig_role.update_yaxes(title_text="Job Role")
    apply_chart_theme(fig_role, "Attrition Rate By Job Role")

    fig_age = px.histogram(
        filtered,
        x="Age",
        color="Attrition",
        barmode="overlay",
        nbins=20,
        color_discrete_map={"Yes": COLORS["accent_alert"], "No": COLORS["accent"]},
    )
    fig_age.update_xaxes(title_text="Age")
    fig_age.update_yaxes(title_text="Employee Count")
    apply_chart_theme(fig_age, "Age Distribution By Attrition")

    fig_income = px.box(
        filtered,
        x="Attrition",
        y="MonthlyIncome",
        color="Attrition",
        color_discrete_map={"Yes": COLORS["accent_alert"], "No": COLORS["accent"]},
    )
    fig_income.update_xaxes(title_text="Attrition")
    fig_income.update_yaxes(title_text="Monthly Income")
    apply_chart_theme(fig_income, "Monthly Income By Attrition")

    overtime_summary = (
        filtered.groupby("OverTimeDisplay")["Attrition"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="AttritionRate")
    )
    fig_overtime = px.bar(
        overtime_summary,
        x="OverTimeDisplay",
        y="AttritionRate",
        color_discrete_sequence=[COLORS["accent"]],
    )
    fig_overtime.update_xaxes(title_text="Overtime Status")
    fig_overtime.update_yaxes(title_text="Attrition Rate Percent")
    apply_chart_theme(fig_overtime, "Attrition Rate By Overtime Status")

    return (
        kpi_total_text,
        kpi_rate_text,
        kpi_income_text,
        kpi_tenure_text,
        fig_department,
        fig_role,
        fig_age,
        fig_income,
        fig_overtime,
    )


import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8050))

if __name__ == "__main__":
    app.run(debug=False, host=HOST, port=PORT)