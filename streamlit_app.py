import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Titanic Overview
overview = """
The Titanic Dashboard offers a comprehensive exploration of the iconic Titanic voyage, providing insights into the demographics, distribution, and survival outcomes of its passengers. This analysis is based on the well-known Titanic dataset, encompassing information about passengers' age, gender, class, fare, and more.

### **Titanic Overview:**
The RMS Titanic, a British passenger liner, embarked on its maiden voyage from Southampton to New York City on April 10, 1912. Tragically, the ship struck an iceberg and sank in the North Atlantic Ocean on April 15, 1912, resulting in one of the most infamous maritime disasters in history.

### **Dashboard Controls:**
Navigate through the dashboard controls on the sidebar to explore different aspects of the Titanic dataset. Adjust age and fare sliders, filter by passenger class, survival status, embarked location, and gender to tailor your analysis. The "Clear Filters" button resets the selections.

### **Data Analysis and Visualization:**
Explore the distribution of passengers' ages and fares through interactive histograms. Understand the survival count by gender, distribution of embarked locations, passenger class breakdown, and the prevalence of siblings/spouses and parents/children on board.

### **Statistics:**
On the sidebar, find the mean age and fare values for the currently selected filters, providing a quick overview of the dataset.

This Titanic Dashboard aims to engage users in a visual and informative journey, shedding light on the historical context and diverse aspects of the Titanic voyage.
"""

# Display the overview
st.markdown(overview)

# Load Titanic dataset
titanic_data = pd.read_csv("titanic.csv")

# Title and Subtitle
st.title("Titanic Dashboard")
st.sidebar.title("Dashboard Controls")

# Sidebar controls for age slicer
age_slider = st.sidebar.slider(
    "Select Age Range",
    min_value=int(titanic_data["Age"].min()),
    max_value=int(titanic_data["Age"].max()),
    value=(0, 80),
    step=1,
)

# Sidebar controls for fare slicer
fare_slider = st.sidebar.slider(
    "Select Fare Range",
    min_value=int(titanic_data["Fare"].min()),
    max_value=int(titanic_data["Fare"].max()),
    value=(0, 100),
    step=1,
)


# Sidebar controls for Pclass filter
selected_pclass = st.sidebar.selectbox(
    "Filter by Passenger Class",
    ["All", "First Class (1)", "Second Class (2)", "Third Class (3)"],
)

# Sidebar controls for Survived filter
selected_survived = st.sidebar.selectbox(
    "Filter by Survival", ["All", "Survived", "Not Survived"]
)

# Sidebar controls for Embarked filter
selected_embarked = st.sidebar.selectbox(
    "Filter by Embarked Location",
    ["All", "Cherbourg (C)", "Queenstown (Q)", "Southampton (S)"],
)

# Sidebar controls for Sex filter
selected_sex = st.sidebar.selectbox("Filter by Gender", ["All", "Male", "Female"])

# Clear button
if st.sidebar.button("Clear Filters"):
    age_slider = (int(titanic_data["Age"].min()), int(titanic_data["Age"].max()))
    fare_slider = (int(titanic_data["Fare"].min()), int(titanic_data["Fare"].max()))
    selected_pclass = "All"
    selected_survived = "All"
    selected_embarked = "All"
    selected_sex = "All"

# Data for selected range and filters
if selected_pclass == "All":
    filtered_data = titanic_data
else:
    filtered_data = titanic_data[titanic_data["Pclass"] == int(selected_pclass[0])]

if selected_survived != "All":
    filtered_data = filtered_data[
        filtered_data["Survived"] == (selected_survived == "Survived")
    ]

if selected_embarked != "All":
    filtered_data = filtered_data[filtered_data["Embarked"] == selected_embarked[0]]

if selected_sex != "All":
    filtered_data = filtered_data[filtered_data["Sex"] == selected_sex.lower()]

# Mean of Age and Fare
mean_age = filtered_data["Age"].mean()
mean_fare = filtered_data["Fare"].mean()

# Histogram for Age
st.subheader("Distribution of Passengers by Age")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=filtered_data, x="Age", bins=20, kde=True, ax=ax)
ax.set_xlabel("Age")
ax.set_ylabel("Number of Passengers")
st.pyplot(fig)

# Histogram for Fare
st.subheader("Distribution of Passengers by Fare")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=filtered_data, x="Fare", bins=20, kde=True, ax=ax)
ax.set_xlabel("Fare")
ax.set_ylabel("Number of Passengers")
st.pyplot(fig)

# Count plot for Sex and Hue Survived
st.subheader("Survival Count by Gender")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=filtered_data, x="Sex", hue="Survived", ax=ax)
ax.set_xlabel("Gender")
ax.set_ylabel("Number of Passengers")
st.pyplot(fig)

# Count plot for Embarked
st.subheader("Embarked Locations")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=filtered_data, x="Embarked", ax=ax)
ax.set_xlabel("Embarked Location")
ax.set_ylabel("Number of Passengers")
st.pyplot(fig)

# Pie chart for Pclass
st.subheader("Passenger Class Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
pclass_counts = filtered_data["Pclass"].value_counts()
ax.pie(
    pclass_counts,
    labels=pclass_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.85,
)
ax.set_title("Passenger Class Distribution")
st.pyplot(fig)

# Pie chart for SibSp
st.subheader("Siblings/Spouses Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sibsp_counts = filtered_data["SibSp"].value_counts()
ax.pie(
    sibsp_counts,
    labels=sibsp_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.85,
)
ax.set_title("Siblings/Spouses Distribution")
st.pyplot(fig)

# Pie chart for Parch
st.subheader("Parents/Children Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
parch_counts = filtered_data["Parch"].value_counts()
ax.pie(
    parch_counts,
    labels=parch_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.85,
)
ax.set_title("Parents/Children Distribution")
st.pyplot(fig)

# Display mean values
st.sidebar.subheader("Statistics:")
st.sidebar.text(f"Mean Age: {mean_age:.2f} years")
st.sidebar.text(f"Mean Fare: ${mean_fare:.2f}")

if __name__ == "__main__":
    st.set_page_config(page_title="Titanic Dashboard", page_icon=":ship:")
    st.title("Titanic Dashboard")
    st.sidebar.title("Dashboard Controls")
