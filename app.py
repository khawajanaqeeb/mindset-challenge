import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Custom Styling
st.markdown(
    """
    <style>
        .stApp {background-color: #F0F8FF;}
        .title {color: #2E86C1; text-align: center; font-size: 40px; font-weight: bold;}
        .subtitle {color: #333; text-align: center; font-size: 18px; margin-bottom: 20px;}
        .stButton>button {background-color: #2E86C1 !important; color: white !important; border-radius: 8px;}
        .center {text-align: center;}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<h1 class="title">💿 Welcome to Data Sweeper by GIAIC</h1>', unsafe_allow_html=True)
# Subtitle
st.markdown('<p class="subtitle">⚡ Convert CSV and Excel files with built-in data cleaning and visualization!</p>', unsafe_allow_html=True)

# File uploader
uploaded_files = st.file_uploader("Upload files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read file based on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file details
        st.write(f"**File Name:** {file.name}")  
        st.write(f"**File Size:** {file.getbuffer().nbytes / 1024:.2f} KB")

        # Preview Data
        st.subheader("👁️ Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"Remove Duplicates - {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("Duplicates removed!")
                st.dataframe(df.head())
        
        with col2:
            if st.button(f"Fill Missing Values - {file.name}"):
                df.fillna(df.mean(numeric_only=True), inplace=True)
                st.success("Missing values filled!")
                st.dataframe(df.head())
        
        # Select Columns
        st.subheader("Select Columns")
        selected_columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        
        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization - {file.name}"):
            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            if numeric_cols:
                selected_viz_cols = st.multiselect("Select columns to plot", numeric_cols, default=numeric_cols[:2])
                st.line_chart(df[selected_viz_cols])
            else:
                st.warning("No numeric columns available for visualization.")
        
        # File Conversion
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
            else:
                df.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)
            
            st.download_button(
                label=f"⏬ Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            st.success("🎉 File ready for download!")
