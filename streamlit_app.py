import streamlit as st
import pandas as pd
import numpy as np

# Create some example data
data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100)
})

# Sidebar
st.sidebar.title('Dashboard Options')
option = st.sidebar.selectbox(
    'Which plot would you like to see?',
    ('Scatter Plot', 'Histogram')
)

# Main area
st.title('Simple Dashboard')

if option == 'Scatter Plot':
    st.subheader('Scatter Plot')
    st.write(data)

    # Plot scatter plot
    st.write("### Scatter Plot")
    st.write("This is a scatter plot of random data")
    st.write(data)

    st.write("### Scatter Plot")
    st.write("This is a scatter plot of random data")
    st.write(data)

elif option == 'Histogram':
    st.subheader('Histogram')
    st.write(data)

    # Plot histogram
    st.write("### Histogram")
    st.write("This is a histogram of random data")
    st.hist(data['x'], bins=20)

    st.write("### Histogram")
    st.write("This is a histogram of random data")
    st.hist(data['y'], bins=20)
