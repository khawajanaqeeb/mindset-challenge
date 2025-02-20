# Necessary Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# App setup with styling by using markdown
st.markdown(
    """
    <style>
        /* Make the app full screen */
        .main .block-container {
            padding: 0px;
            margin: 0px;
            max-width: 100%;
        }

        /* Background color */
        .stApp {
            background-color: #87CEEB;
        }
        
        /* Main Title Styling */
        .title {
            color: #2E86C1;
            text-align: center;
            font-size: 50px;
            font-weight: bold;
        }
        
        /* style for Subtitle  */
        .subtitle {
            color: #333333;
            text-align: center;
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 20px;
        }

        /* style for Button  */
        .stButton>button {
            background-color: #2E86C1 !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
        }

        /* style for content */
        .center {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with Styling
st.markdown('<h1 class="title">💿 Welcom to  Data Sweeper by GIAIC</h1>', unsafe_allow_html=True)

# Subtitle with Styling
st.markdown(
    '<p class="subtitle"> ⚡ Transform Your Files Between CSV and Excel Format with Built-in Data Cleaning and Visualization!</p>',
    unsafe_allow_html=True,
)

# Add a Button with Custom Styling
st.markdown('<div class="center"><button class="stButton">Upload File</button></div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")  # Fix: Specify engine
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display Description about file
        st.write(f"**File Name:** {file.name}")  
        st.write(f"**File Size:** {file.getbuffer().nbytes / 1024:.2f} KB")  # Fix: Correct file size calculation

        # Showing 5 rows of our df
        st.write("👁️ Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Options for Data cleaning
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True) 
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")  

        # Choose columns to keep or convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns) 
        df = df[columns]                  
   
        # Visualization added
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.line_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File conversion from CSV to Excel
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")  # Fix: Ensure engine is specified
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)  # Fix: Ensure buffer is at start before download

            # Download converted file
            st.download_button(
                label=f"⏬ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )  

            st.success("🎉 All files processed!")
