import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
import os
from sqlalchemy.exc import IntegrityError
from db import get_session
from models import Project, ProjectData, ProjectSummary, create_tables
from sqlalchemy.orm import joinedload
from io import StringIO
import base64

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Ensure tables exist
create_tables()

st.set_page_config(page_title="Optimization Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("Optimization Projects")
session = get_session()
projects = session.query(Project).all()
project_names = [p.name for p in projects]
selected_project = st.sidebar.selectbox("Select Project", ["Dashboard"] + project_names)

st.sidebar.markdown("---")
with st.sidebar.expander("Upload New Project"):
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    new_project_name = st.text_input("Project Name")
    if st.button("Upload & Create Project"):
        if not uploaded_file or not new_project_name:
            st.warning("Please provide both a CSV and a project name.")
        else:
            # Validate project name uniqueness
            if session.query(Project).filter_by(name=new_project_name).first():
                st.error("Project name already exists. Please choose another.")
            else:
                try:
                    df = pd.read_csv(uploaded_file, encoding="utf-8")
                except Exception as e:
                    st.error(f"CSV parsing error: {e}")
                    st.stop()
                required_cols = {"driver", "pickup_point", "lat", "lon", "original_dead_km", "optimized_dead_km", "swap_chain", "deviation"}
                if not required_cols.issubset(df.columns.str.strip().str.lower()):
                    st.error(f"CSV must contain columns: {', '.join(required_cols)}")
                    st.stop()
                # Clean and sanitize
                df.columns = df.columns.str.strip().str.lower()
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                for col in ["lat", "lon", "original_dead_km", "optimized_dead_km", "deviation"]:
                    try:
                        df[col] = pd.to_numeric(df[col], errors="coerce")
                    except Exception:
                        st.error(f"Column {col} must be numeric.")
                        st.stop()
                if df[required_cols].isnull().any().any():
                    st.error("Some required fields are missing or malformed.")
                    st.stop()
                # Insert project
                project = Project(name=new_project_name)
                session.add(project)
                session.commit()
                # Insert data
                for _, row in df.iterrows():
                    pdata = ProjectData(
                        project_id=project.id,
                        driver=row["driver"],
                        pickup_point=row["pickup_point"],
                        lat=row["lat"],
                        lon=row["lon"],
                        original_dead_km=row["original_dead_km"],
                        optimized_dead_km=row["optimized_dead_km"],
                        swap_chain=row["swap_chain"],
                        deviation=row["deviation"]
                    )
                    session.add(pdata)
                # Compute summary
                summary = ProjectSummary(
                    project_id=project.id,
                    total_routes=len(df),
                    total_drivers=df["driver"].nunique(),
                    total_dead_km=df["original_dead_km"].sum(),
                    optimized_dead_km=df["optimized_dead_km"].sum(),
                    swap_chains=df["swap_chain"].nunique(),
                    deviations=(df["deviation"] > 0).sum()
                )
                session.add(summary)
                try:
                    session.commit()
                    st.success("Project uploaded and processed!")
                    st.experimental_rerun()
                except IntegrityError:
                    session.rollback()
                    st.error("Database error: could not save project data.")

# Dashboard view
if selected_project == "Dashboard":
    st.title("Optimization Dashboard")
    st.markdown("Overview of all projects.")
    if not projects:
        st.info("No projects yet. Upload a CSV to get started.")
    else:
        # Summary metrics
        summaries = session.query(ProjectSummary).all()
        total_projects = len(projects)
        total_routes = sum(s.total_routes for s in summaries if s)
        total_drivers = sum(s.total_drivers for s in summaries if s)
        total_dead_km = sum(s.total_dead_km for s in summaries if s)
        total_optimized_dead_km = sum(s.optimized_dead_km for s in summaries if s)
        st.markdown("<div class='summary-card'><b>Total Projects:</b> {}<br><b>Total Routes:</b> {}<br><b>Total Drivers:</b> {}<br><b>Total Dead KM:</b> {:.2f}<br><b>Optimized Dead KM:</b> {:.2f}</div>".format(
            total_projects, total_routes, total_drivers, total_dead_km, total_optimized_dead_km), unsafe_allow_html=True)
        # Bar chart: original vs optimized dead km per project
        chart_df = pd.DataFrame({
            "Project": [p.name for p in projects],
            "Original Dead KM": [s.total_dead_km for s in summaries],
            "Optimized Dead KM": [s.optimized_dead_km for s in summaries]
        })
        fig = px.bar(chart_df, x="Project", y=["Original Dead KM", "Optimized Dead KM"], barmode="group",
                     title="Original vs Optimized Dead KM by Project", color_discrete_sequence=["#e5b79e", "#e2f8e4"])
        st.plotly_chart(fig, use_container_width=True)
        # Table of summaries
        st.dataframe(chart_df)

# Per-project detail view
else:
    project = session.query(Project).options(joinedload(Project.data), joinedload(Project.summary)).filter_by(name=selected_project).first()
    if not project:
        st.error("Project not found.")
        st.stop()
    st.title(f"Project: {project.name}")
    summary = project.summary
    if summary:
        st.markdown(f"<div class='summary-card'><b>Total Routes:</b> {summary.total_routes}<br><b>Total Drivers:</b> {summary.total_drivers}<br><b>Total Dead KM:</b> {summary.total_dead_km:.2f}<br><b>Optimized Dead KM:</b> {summary.optimized_dead_km:.2f}<br><b>Swap Chains:</b> {summary.swap_chains}<br><b>Deviations:</b> {summary.deviations}</div>", unsafe_allow_html=True)
    # Narrative explanation
    st.markdown("""
    #### Executive Summary
    This project analyzes route optimization for drivers and pickup points. The metrics above summarize the impact of optimization, including reduction in dead kilometers and swap chain efficiency. The charts and tables below provide further insights.
    """, unsafe_allow_html=True)
    # Data table
    data = pd.DataFrame([{**{c.name: getattr(d, c.name) for c in ProjectData.__table__.columns}} for d in project.data])
    if data.empty:
        st.info("No data for this project.")
    else:
        st.dataframe(data)
        # Bar chart: original vs optimized dead km per driver
        fig2 = px.bar(data, x="driver", y=["original_dead_km", "optimized_dead_km"], barmode="group", title="Dead KM per Driver",
                      color_discrete_sequence=["#e5b79e", "#e2f8e4"])
        st.plotly_chart(fig2, use_container_width=True)
        # Map: driver and pickup points
        map_df = data[["lat", "lon", "driver", "pickup_point"]].dropna()
        if not map_df.empty:
            driver_layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_df.drop_duplicates(subset=["driver", "lat", "lon"]),
                get_position='[lon, lat]',
                get_color='[229, 183, 158, 180]',  # #e5b79e, primary button color
                get_radius=100,
                pickable=True,
                tooltip=True,
            )
            pickup_layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_df.drop_duplicates(subset=["pickup_point", "lat", "lon"]),
                get_position='[lon, lat]',
                get_color='[226, 248, 228, 180]',  # #e2f8e4, secondary button color
                get_radius=60,
                pickable=True,
                tooltip=True,
            )
            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(
                    latitude=map_df["lat"].mean(),
                    longitude=map_df["lon"].mean(),
                    zoom=11,
                    pitch=0,
                ),
                layers=[driver_layer, pickup_layer],
                tooltip={"text": "Driver: {driver}\nPickup: {pickup_point}"}
            ))
        # Swap chains and deviations
        st.markdown("#### Swap Chains and Deviations")
        swap_df = data[["swap_chain", "deviation"]].groupby("swap_chain").agg({"deviation": "sum"}).reset_index()
        st.dataframe(swap_df)
        # Download buttons
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Project Data (CSV)", csv, file_name=f"{project.name}_data.csv", mime="text/csv")
        if summary:
            summary_df = pd.DataFrame([{c.name: getattr(summary, c.name) for c in ProjectSummary.__table__.columns}])
            summary_csv = summary_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Summary (CSV)", summary_csv, file_name=f"{project.name}_summary.csv", mime="text/csv") 