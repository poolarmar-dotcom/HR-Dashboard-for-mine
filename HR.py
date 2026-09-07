import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HR Dashboard", layout="wide")

st.title("HR Dashboard")
st.markdown("---")

hr = pd.read_excel("HR_Dashboard.xlsx")

hr["Status"] = hr["left"].map({
    0: "Stayed",
    1: "Left"
})

st.sidebar.header("Filters")

depts = ["All"] + sorted(hr["Department"].dropna().unique().tolist())
dept = st.sidebar.selectbox("Department", depts)

salaries = ["All"] + sorted(hr["salary"].dropna().unique().tolist())
salary = st.sidebar.selectbox("Salary Level", salaries)

statuses = ["All", "Stayed", "Left"]
status = st.sidebar.selectbox("Status", statuses)

filtered = hr.copy()

if dept != "All":
    filtered = filtered[filtered["Department"] == dept]

if salary != "All":
    filtered = filtered[filtered["salary"] == salary]

if status != "All":
    filtered = filtered[filtered["Status"] == status]

total = len(filtered)
left = filtered[filtered["left"] == 1].shape[0]
stayed = filtered[filtered["left"] == 0].shape[0]

turnover = (left / total) * 100 if total > 0 else 0
sat = filtered["satisfaction_level"].mean() if total > 0 else 0
eval_score = filtered["last_evaluation"].mean() if total > 0 else 0
projects = filtered["number_project"].mean() if total > 0 else 0
hours = filtered["average_montly_hours"].mean() if total > 0 else 0
tenure = filtered["time_spend_company"].mean() if total > 0 else 0
accidents = filtered["Work_accident"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Employees", f"{total:,}")
c2.metric("Turnover Rate", f"{turnover:.1f}%")
c3.metric("Avg Satisfaction", f"{sat:.2f}")
c4.metric("Avg Evaluation", f"{eval_score:.2f}")

c5, c6, c7, c8 = st.columns(4)

c5.metric("Avg Projects", f"{projects:.1f}")
c6.metric("Avg Hours", f"{hours:.0f}")
c7.metric("Avg Tenure", f"{tenure:.1f} yrs")
c8.metric("Accidents", f"{accidents:,}")

st.markdown("---")
st.subheader("Charts")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Turnover",
    "Satisfaction",
    "Projects",
    "Department",
    "Scatter"
])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        data = (
            filtered
            .groupby("Department")
            .agg(
                Total=("left", "count"),
                Left=("left", lambda x: (x == 1).sum())
            )
            .reset_index()
        )

        data["Rate"] = (data["Left"] / data["Total"]) * 100
        data = data.sort_values("Rate", ascending=False)

        fig = px.bar(
            data,
            x="Department",
            y="Rate",
            title="Turnover by Department",
            text_auto=".1f",
            template="plotly_white",
            color="Rate",
            color_continuous_scale="Reds"
        )

        fig.update_layout(
            height=400,
            title_x=0.5,
            yaxis_title="Turnover Rate (%)",
            xaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        data = (
            filtered
            .groupby("salary")
            .agg(
                Total=("left", "count"),
                Left=("left", lambda x: (x == 1).sum())
            )
            .reset_index()
        )

        data["Rate"] = (data["Left"] / data["Total"]) * 100

        fig = px.bar(
            data,
            x="salary",
            y="Rate",
            title="Turnover by Salary",
            text_auto=".1f",
            template="plotly_white",
            color="Rate",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            height=400,
            title_x=0.5,
            yaxis_title="Turnover Rate (%)",
            xaxis_title="Salary Level"
        )

        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(
            filtered,
            x="Status",
            y="satisfaction_level",
            title="Satisfaction: Stayed vs Left",
            template="plotly_white",
            color="Status",
            color_discrete_sequence=["#2ecc71", "#e74c3c"]
        )

        fig.update_layout(
            height=400,
            title_x=0.5,
            xaxis_title="",
            yaxis_title="Satisfaction Level"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(
            filtered,
            x="Status",
            y="last_evaluation",
            title="Evaluation: Stayed vs Left",
            template="plotly_white",
            color="Status",
            color_discrete_sequence=["#2ecc71", "#e74c3c"]
        )

        fig.update_layout(
            height=400,
            title_x=0.5,
            xaxis_title="",
            yaxis_title="Last Evaluation"
        )

        st.plotly_chart(fig, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)

    with col1:
        data = (
            filtered
            .groupby("number_project")
            .agg(
                Count=("left", "count")
            )
            .reset_index()
        )

        fig = px.bar(
            data,
            x="number_project",
            y="Count",
            title="Projects per Employee",
            text_auto=True,
            template="plotly_white",
            color="Count",
            color_continuous_scale="Greens"
        )

        fig.update_layout(
            height=400,
            title_x=0.5,
            xaxis_title="Number of Projects",
            yaxis_title="Employees"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            filtered,
            x="time_spend_company",
            color="Status",
            title="Years at Company",
            template="plotly_white",
            barmode="group",
            color_discrete_sequence=["#2ecc71", "#e74c3c"]
        )

        fig.update_layout(
            height=400,
            title_x=0.5,
            xaxis_title="Years at Company",
            yaxis_title="Employees"
        )

        st.plotly_chart(fig, use_container_width=True)

with tab4:
    col1, col2 = st.columns(2)

    with col1:
        data = filtered["Department"].value_counts().reset_index()
        data.columns = ["Department", "Count"]

        fig = px.bar(
            data,
            x="Department",
            y="Count",
            title="Department Size",
            text_auto=True,
            template="plotly_white",
            color="Count",
            color_continuous_scale="Purples"
        )

        fig.update_layout(
            height=400,
            title_x=0.5,
            xaxis_title="",
            yaxis_title="Employees"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        data = (
            filtered
            .groupby("Department")
            .agg(
                Total=("Work_accident", "count"),
                Accidents=("Work_accident", "sum")
            )
            .reset_index()
        )

        data["Rate"] = (data["Accidents"] / data["Total"]) * 100
        data = data.sort_values("Rate", ascending=False)

        fig = px.bar(
            data,
            x="Department",
            y="Rate",
            title="Accident Rate by Department",
            text_auto=".1f",
            template="plotly_white",
            color="Rate",
            color_continuous_scale="Oranges"
        )

        fig.update_layout(
            height=400,
            title_x=0.5,
            yaxis_title="Accident Rate (%)",
            xaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True)

with tab5:
    fig = px.scatter(
        filtered,
        x="satisfaction_level",
        y="last_evaluation",
        color="Status",
        title="Satisfaction vs Evaluation",
        template="plotly_white",
        opacity=0.6,
        color_discrete_sequence=["#2ecc71", "#e74c3c"],
        hover_data=[
            "Department",
            "salary",
            "number_project"
        ]
    )

    fig.update_layout(
        height=500,
        title_x=0.5,
        xaxis_title="Satisfaction Level",
        yaxis_title="Last Evaluation"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

with st.expander("View Data Table"):
    st.dataframe(
        filtered,
        use_container_width=True
    )

st.caption(
    f"HR Dashboard | Showing {total:,} employees"
)