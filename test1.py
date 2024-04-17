import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import requests
from io import StringIO
import seaborn as sns
import matplotlib.pyplot as plt


#SETTING STREAMLIT PAGE CONFIGURATION
image = Image.open("logo.webp")
st.set_page_config(page_title="Zomato Data Analysis ",
                   page_icon=image,
                   layout='wide',
                   initial_sidebar_state="expanded")

#CREATING MENU ITEMS
Menu = option_menu(
menu_title='Menu',
options=["Home", "Overview", "Explore"],
icons=["house","graph-up-arrow","bar-chart-line"],
default_index=0,
orientation="horizontal")

# Load the DataFrame


# GitHub CSV URL
github_url = 'https://raw.githubusercontent.com/nethajinirmal13/Training-datasets/main/zomato/zomato.csv'

# Fetch the CSV file from GitHub
response = requests.get(github_url)

# Check if the request was successful
if response.status_code == 200:
    # Read the CSV data from the response
    csv_data = StringIO(response.text)
    
    # Create a DataFrame from the CSV data
    df = pd.read_csv(csv_data)
    json_data = df.to_json(orient="records")

else:
    print("Failed to retrieve the CSV file from GitHub.")



# Dictionary mapping country codes to country names
country_names = {
    1: 'India',
    14: 'Australia',
    30: 'Brazil',
    37: 'Canada',
    94: 'Indonesia',
    148: 'New Zealand',
    162: 'Phillipines',
    166: 'Qatar',
    184: 'Singapore',
    189: 'South Africa',
    191: 'Sri Lanka',
    208: 'Turkey',
    214: 'UAE',
    215: 'United Kingdom',
    216: 'United States'
}

# Add a new column "Country Name" based on "Country Code"
df['Country Name'] = df['Country Code'].map(country_names)

df.insert(2, 'Country Name', df.pop('Country Name'))


## 1. Add a column with rupees as the currency

# Hypothetical exchange rates relative to Indian Rupee
exchange_rates = {
    'Botswana Pula(P)': 6.08,
    'Brazilian Real(R$)': 16.31,
    'Dollar($)': 83.45,
    'Emirati Diram(AED)': 22.72,
    'Indian Rupees(Rs.)': 1.0,
    'Indonesian Rupiah(IDR)': 0.0052,  
    'NewZealand($)': 49.55,
    'Pounds(專)': 104.15,
    'Qatari Rial(QR)': 22.92,
    'Rand(R)': 4.42,
    'Sri Lankan Rupee(LKR)': 0.28, 
    'Turkish Lira(TL)': 2.58,
}

# Update 'Currency in Rupees' column based on the 'exchange_rates' dictionary

df['Currency in Rupees'] = df['Currency'].map(exchange_rates)

df['Currency in Rupees']= df['Average Cost for two'] * df['Currency in Rupees']

df.insert(13,'Currency in Rupees',df.pop('Currency in Rupees'))

df['Currency in Rupees'] = '₹' + df['Currency in Rupees'].astype(str)

zomato_df=df
#HOME PAGE
if Menu == "Home":
    col1, col2 = st.columns([1,3])
    with col1:
        st.image("Zomato-Logo (1).png", width=300)
    with col2:
        st.markdown("<h1 style='text-align: right; color: green;'>Zomato Data Analysis and Visualization</h1>", unsafe_allow_html=True)
    st.image("anls.jpg ",width=700)
    st.write(" ")
    st.markdown("## <span style='color:#FF5A5F;'>Description : </span> Zomato, a leading online food delivery and restaurant discovery platform, offers a treasure trove of data that can provide valuable insights into dining trends, consumer preferences, restaurant performances, and more. Analyzing Zomato data involves examining various facets such as restaurant ratings, cuisine popularity, price trends, customer reviews, and geographical distribution. Through effective visualization techniques using tools like Plotly or Matplotlib, analysts can present this data in an easily digestible format, showcasing patterns, correlations, and trends. This analysis not only benefits restaurant owners in understanding their market position but also aids consumers in making informed dining choices based on data-driven recommendations.", unsafe_allow_html=True)

# OVERVIEW PAGE
if Menu == "Overview":
    tab1, tab2 = st.tabs([":green[DATA]", ":blue[Currency comparison]"])
    with tab1:
        col1, col2 = st.columns([1,3])

        if col1.button("Dataframe"):
            col1.write('')
            col2.write(zomato_df)
    
    with tab2:

        currency_comparison = px.scatter(zomato_df, x='Currency in Rupees', y='Country Code', color='Country Name',
                                    title='Comparison of Indian Currency with Other Countries')
        st.plotly_chart(currency_comparison)

if Menu == "Explore":
    tab1,tab2,tab3,tab4 = st.tabs([":green[DATA]", ":blue[DATA1]",":yellow[DATA2]",":brown[DATA3]"])
    with tab1:
        ## Create a dropdown to choose the country-specific data
        selected_country = st.selectbox('Select a Country', zomato_df['Country Name'].unique())

        ## Filter data based on the selected country
        filtered_df = zomato_df[zomato_df['Country Name'] == selected_country]

        ## Chart 1: Any two charts of your choice
        # For example: Count of restaurants by city and Total votes by city
        chart1_data = filtered_df['City'].value_counts().reset_index()
        chart1_data.columns = ['City', 'Count']
        chart1 = px.bar(chart1_data, x='City', y='Count', title=f'Count of Restaurants in {selected_country}',)
        st.plotly_chart(chart1)

        chart2_data = filtered_df.groupby('City')['Votes'].sum().reset_index()
        chart2 = px.bar(chart2_data, x='City', y='Votes', title=f'Total Votes in {selected_country}')
        st.plotly_chart(chart2)
    with tab2:
        col1,col2=st.columns([3,1])
        with col1:
            # Filter data for India
            df_india = zomato_df[zomato_df['Country Name'] == 'India']

            # Group data by cuisine and calculate total price range
            grouped_df = df_india.groupby('Cuisines')['Price range'].sum().reset_index()

            # Sort by total price range in descending order and take top 5
            top_5_cuisines = grouped_df.sort_values(by='Price range', ascending=False).head(5)

            # Create pie chart
            fig, ax = plt.subplots()
            ax.pie(top_5_cuisines['Price range'], labels=top_5_cuisines['Cuisines'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.pyplot(fig)
    with tab3:
        # Filter based on city
        selected_country = st.selectbox('Select a country:', df['Country Name'].unique())
        country_filtered_df = zomato_df[zomato_df['Country Name'] == selected_country]

        selected_city = st.selectbox('Select a city:', country_filtered_df['City'].unique())
        filtered_df = country_filtered_df[country_filtered_df['City'] == selected_city]
        col1,col2=st.columns(2)
        with col1:
            # Bar chart for top 5 famous cuisines in the city
            st.header(' :green[Bar chart for top 5 famous cuisines in the city]')
            top_5_cuisines = filtered_df['Restaurant Name'].value_counts().head(5)
            plt.figure(figsize=(6, 6))
            sns.barplot(x=top_5_cuisines.values, y=top_5_cuisines.index, palette='coolwarm')
            plt.title(f'Top 5 Famous Cuisines in {selected_city}')
            plt.xlabel('Number of Restaurants')
            plt.ylabel('Cuisine')
            st.pyplot(plt)
 
        with col2:
            # Bar chart for top 5 costlier cuisines in the city
            st.header (':blue[Bar chart for top 5 costlier cuisines in the city]')
            costlier_cuisines = filtered_df.groupby('Restaurant Name')['Price range'].mean().sort_values(ascending=False).head(5)
            plt.figure(figsize=(6, 6))
            sns.barplot(x=costlier_cuisines.values, y=costlier_cuisines.index,palette='twilight_shifted')
            plt.title(f'Top 5 Costlier Cuisines in {selected_city}')
            plt.xlabel('Average Price Range')
            plt.ylabel('Cuisine')
            st.pyplot(plt)

        with col1:
            # Line chart of top 10 Rating count in the city (based on rating text)
            st.header("")
            st.header (':blue[Line chart of top 10 Rating count in the city based on rating text]')
            rating_counts = filtered_df['Rating text'].value_counts().sort_index()
            plt.figure(figsize=(10, 5))
            sns.lineplot(x=rating_counts.index, y=rating_counts.values, marker='o',palette='warm')
            plt.title(f'Rating Count in {selected_city}')
            plt.xlabel('Rating Text')
            plt.ylabel('Count')
            st.pyplot(plt)
   
        with col2:
            # Pie chart online delivery vs dine-in
            st.header("")
            st.header (':green[Pie chart online delivery vs dine-in]')
            delivery_counts = filtered_df['Has Online delivery'].value_counts()
            plt.figure(figsize=(7,5))
            plt.pie(delivery_counts, labels=delivery_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title('Online Delivery vs Dine-in')
            st.pyplot(plt)
    with tab4:
        col1,col2=st.columns(2)
        with col1:
             # Filter data for cities in India
            df_india = zomato_df[zomato_df['Country Name'] == 'India']
            st.header(":blue[Bar chart - Top 5 cities of India spends more on Online Delivery]")
            #1. Bar chart - Top 5 cities of India spends more on Online Delivery
            top_5_online_cities = df_india.groupby('City')['Price range'].sum().sort_values(ascending=False).head(5)
            plt.figure(figsize=(10, 6))
            sns.barplot(x=top_5_online_cities.index, y=top_5_online_cities.values, palette='Blues_d')
            plt.title('Top 5 Cities in India Spending More on Online Delivery')
            plt.xlabel('City')
            plt.ylabel('Total Spending on Online Delivery')
            plt.xticks(rotation=45)
            st.pyplot(plt)

            # 2. Bar chart - Top 5 cities of India spends more on Dine-in
            st.header(":blue[Bar chart - Top 5 cities of India spends more on Dine-in]")

            top_5_dine_in_cities = df_india[df_india['Has Table booking'] == 'Yes'].groupby('City')['Price range'].sum().sort_values(ascending=False).head(5)
            plt.figure(figsize=(10, 6))
            sns.barplot(x=top_5_dine_in_cities.index, y=top_5_dine_in_cities.values, palette='Reds')
            plt.title('Top 5 Cities in India Spending More on Dine-in')
            plt.xlabel('City')
            plt.ylabel('Total Spending on Dine-in')
            plt.xticks(rotation=45)
            st.pyplot(plt)

            # 3. Line chart - 5 cities has a high living cost vs low living cost
            st.header(":blue[Cities has a high living cost vs low living cost]")

            median_price = df_india['Price range'].median()
            df_india['Living Cost'] = df_india['Price range'].apply(lambda x: 'High' if x > median_price else 'Low')

            living_cost_counts = df_india['Living Cost'].value_counts().sort_index()
            plt.figure(figsize=(8, 6))
            sns.barplot(x=living_cost_counts.index, y=living_cost_counts.values, palette='Reds_r')
            plt.xlabel('Living Cost')
            plt.ylabel('Number of Cities')
            st.pyplot(plt)                   
