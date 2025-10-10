import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("covid_19.csv")
    return df

df = load_data()

# -------------------------------
# App Title
# -------------------------------
st.title("COVID-19 Data Visualization Dashboard 🦠")
st.markdown("### Explore insights and patterns from the COVID-19 dataset")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Select a Visualization",
    (
        "Dataset Overview",
        "Visualization 1",
        "Visualization 2",
        "Visualization 3",
        "Visualization 4",
        "Visualization 5",
        "Visualization 6",
        "Visualization 7",
        "Visualization 8"
    )
)

# -------------------------------
# Overview
# -------------------------------
if options == "Dataset Overview":
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Basic Info")
    st.write("Number of Rows:", df.shape[0])
    st.write("Number of Columns:", df.shape[1])

    st.subheader("Statistical Summary")
    st.write(df.describe())

# -------------------------------
# Visualization 1
# -------------------------------
elif options == "Visualization 1":
    st.subheader("Visualization 1 Title")
    # TODO: Paste code for graph 1 here
    # Example:
    # fig, ax = plt.subplots()
    # sns.barplot(x='Country', y='Cases', data=df, ax=ax)
    # st.pyplot(fig)
    pass

# -------------------------------
# Visualization 2
# -------------------------------
elif options == "Visualization 2":
    st.subheader("Visualization 2 Title")
    # TODO: Paste code for graph 2 here
    pass

# -------------------------------
# Visualization 3
# -------------------------------
elif options == "Visualization 3":
    st.subheader("Visualization 3 Title")
    # TODO: Paste code for graph 3 here
    pass

# -------------------------------
# Visualization 4
# -------------------------------
elif options == "Visualization 4":
    st.subheader("Visualization 4 Title")
    # TODO: Paste code for graph 4 here
    pass

# -------------------------------
# Visualization 5
# -------------------------------
elif options == "Visualization 5":
    st.subheader("Visualization 5 Title")
    # TODO: Paste code for graph 5 here
    pass

# -------------------------------
# Visualization 6
# -------------------------------
elif options == "Visualization 6":
    st.subheader("Visualization 6 Title")
    # TODO: Paste code for graph 6 here
    pass

# -------------------------------
# Visualization 7
# -------------------------------
elif options == "Visualization 7":
    st.subheader("Visualization 7 Title")
    # TODO: Paste code for graph 7 here
    pass

# -------------------------------
# Visualization 8
# -------------------------------
elif options == "Visualization 8":
    st.subheader("Visualization 8 Title")
    # TODO: Paste code for graph 8 here
    pass

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("Built with ❤️ by Abhay !")
