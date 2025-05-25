#import dependencies
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from interestOverTime import interest_over_time as iot
import matplotlib.dates as mdates

# Set the title for the app
st.title("Trend Analyzer for Keywords")

# Set up formatting so button is next to input
left, middle, right = st.columns(3, vertical_alignment='bottom')

# Read in the current data
df = pd.read_csv('current_data.csv')

# Get the input text from the user, and remove whitespace and commas from the
# result. put this in the left column
with left:
    kws = [text.strip() for text in 
        st.text_input("Enter keywords, separated by commas (max 5 words)").split(",")]
        
# Have the user select a timeframe
with middle:
    tframe = st.selectbox("Select timeframe", ['today 5-y', 'today 12-m', 'today 3-m', 'now 7-d', 'all'])


# Display the current keywords if it is not empty
if not df.empty:
    current_keywords = df.columns.to_list()[1:] if df.columns.to_list()[0] == 'date' else df.columns.to_list()
    st.text(f'Current Keywords: {current_keywords}')

# Get the data for the listed Kws
with right:
    if st.button('Use New Keywords'):
        if len(kws) > 5:

            # Concatinate the kws list, and tell the user that the list was too long
            kws = kws[:5]
            st.text(f'Too many Keywords passed. The queried list is {kws}')

        # Get the dataframe of the interest over time for the requested words
        df = iot(kws, tframe=tframe)

        # Save the dataframe to the current_data csv file if it did not return empty
        if not df.empty:
            df.to_csv('current_data.csv')
        else:
            st.text('No data found')

# Button to display data for interest over time
if st.button("Get Interest over time"):

    # Get the data from the csv
    df = pd.read_csv('current_data.csv')

    #make sure the df is not empty
    if df.empty:
        st.text('No data found. Please search again for new data.')
    else:
        # Display table using the dataframe of most recent data
        st.table(df.sort_index(ascending=False).head(10))

        # Set the title using the list
        title = 'Interest over time for '+ ', '.join(kws)

        # Set up the subplots to plot on
        fig, ax = plt.subplots()

        # Create a lineplot on the subplot, passing in the ax
        sns.lineplot(data=df, x='date', y=df.columns[1], ax=ax)

        # Plot all pts
        for col in df.columns:
            if col != 'date':
                ax.plot(df['date'], df[col], label=col)
        ax.legend()

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
        fig.tight_layout()

        # Put the plot into streamlit
        st.pyplot(fig=fig)

        # Close the plot
        plt.close()
        
