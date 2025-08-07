import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from sqlalchemy import create_engine

st.set_page_config(page_title="📱 PhonePe Pulse - Home", layout="wide")

view_option = st.sidebar.selectbox("Choose Data Type", ["Transaction", "User"])


engine = create_engine("postgresql+psycopg2://sindhulocal:7356@localhost:5432/newphonepay")

query = '''
SELECT state,
       year,
       quarter,
       SUM(transaction_count) AS total_transaction_count,
       ROUND(SUM(transaction_amount/10000000):: NUMERIC,2) AS total_transaction_amount
FROM aggregate_transaction
GROUP BY state, year, quarter
ORDER BY state, year, quarter
'''
df = pd.read_sql(query, engine)

user_query = '''
SELECT state,
       year,
       quarter,
       SUM(register_user) AS register_user,
       SUM(app_opens) AS app_opens
FROM aggregate_user_register
GROUP BY state, year, quarter
ORDER BY state, year, quarter
'''
df_user = pd.read_sql(user_query, engine)

st.markdown("<h1 style='text-align: center;'> PhonePe Pulse Dashboard </h1>", unsafe_allow_html=True)
st.markdown("### India’s Digital Payments Visualization — Powered by PhonePe Data")

def metric_transaction(df):
    col1, col2, col3,col4 =  st.columns(4)
    col1.metric("Total transaction count",f"{round(df['total_transaction_count'].sum()/10000000,2)}Cr")
    col2.metric("Total transaction amount",f"{(df['total_transaction_amount'].sum())}Cr")
    col3.metric("States Covered",df['state'].nunique())
    col4.metric("Years Covered",df['year'].nunique())

def metric_user(df):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", f"{round(df['register_user'].sum()/10000000, 2)} Cr")
    col2.metric("App Opens", f"{round(df['app_opens'].sum()/1000000, 2)} Cr")
    col3.metric("States Covered", df['state'].nunique())
    col4.metric("Years Covered", df['year'].nunique())
    



def map_transaction(df):
    state_mapping = {
        'andaman-&-nicobar-islands': 'Andaman & Nicobar Islands',
        'andhra-pradesh': 'Andhra Pradesh',
        'arunachal-pradesh': 'Arunachal Pradesh',
        'assam': 'Assam',
        'bihar': 'Bihar',
        'chandigarh': 'Chandigarh',
        'chhattisgarh': 'Chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
        'delhi': 'Delhi',
        'goa': 'Goa',
        'gujarat': 'Gujarat',
        'haryana': 'Haryana',
        'himachal-pradesh': 'Himachal Pradesh',
        'jammu-&-kashmir': 'Jammu & Kashmir',
        'jharkhand': 'Jharkhand',
        'karnataka': 'Karnataka',
        'kerala': 'Kerala',
        'ladakh': 'Ladakh',
        'lakshadweep': 'Lakshadweep',
        'madhya-pradesh': 'Madhya Pradesh',
        'maharashtra': 'Maharashtra',
        'manipur': 'Manipur',
        'meghalaya': 'Meghalaya',
        'mizoram': 'Mizoram',
        'nagaland': 'Nagaland',
        'odisha': 'Odisha',
        'puducherry': 'Puducherry',
        'punjab': 'Punjab',
        'rajasthan': 'Rajasthan',
        'sikkim': 'Sikkim',
        'tamil-nadu': 'Tamil Nadu',
        'telangana': 'Telangana',
        'tripura': 'Tripura',
        'uttar-pradesh': 'Uttar Pradesh',
        'uttarakhand': 'Uttarakhand',
        'west-bengal': 'West Bengal'
    }
    df['state'] = df['state'].map(state_mapping)
    state_summary = df.groupby("state")[["total_transaction_amount"]].sum().reset_index()
    
    fig = px.choropleth(
        state_summary,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='total_transaction_amount',
        color_continuous_scale='Reds',
        title='Transaction Amount by State'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

def map_user(df_user):
    state_mapping = {
        'andaman-&-nicobar-islands': 'Andaman & Nicobar Islands',
        'andhra-pradesh': 'Andhra Pradesh',
        'arunachal-pradesh': 'Arunachal Pradesh',
        'assam': 'Assam',
        'bihar': 'Bihar',
        'chandigarh': 'Chandigarh',
        'chhattisgarh': 'Chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
        'delhi': 'Delhi',
        'goa': 'Goa',
        'gujarat': 'Gujarat',
        'haryana': 'Haryana',
        'himachal-pradesh': 'Himachal Pradesh',
        'jammu-&-kashmir': 'Jammu & Kashmir',
        'jharkhand': 'Jharkhand',
        'karnataka': 'Karnataka',
        'kerala': 'Kerala',
        'ladakh': 'Ladakh',
        'lakshadweep': 'Lakshadweep',
        'madhya-pradesh': 'Madhya Pradesh',
        'maharashtra': 'Maharashtra',
        'manipur': 'Manipur',
        'meghalaya': 'Meghalaya',
        'mizoram': 'Mizoram',
        'nagaland': 'Nagaland',
        'odisha': 'Odisha',
        'puducherry': 'Puducherry',
        'punjab': 'Punjab',
        'rajasthan': 'Rajasthan',
        'sikkim': 'Sikkim',
        'tamil-nadu': 'Tamil Nadu',
        'telangana': 'Telangana',
        'tripura': 'Tripura',
        'uttar-pradesh': 'Uttar Pradesh',
        'uttarakhand': 'Uttarakhand',
        'west-bengal': 'West Bengal'
    }
    df_user['state'] = df_user['state'].map(state_mapping)
    state_summary_user= df_user.groupby("state")[["register_user"]].sum().reset_index()
    
    fig = px.choropleth(
        state_summary_user,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='register_user',
        color_continuous_scale='Reds',
        title='Register User by State'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)
    
    
def top_10_values(df,years, quarters):
    
    genre = st.sidebar.radio("Select Level", ["State", "District", "Postal Codes"],horizontal=True)

    if genre == "State":
        
        filtered_state= df[
            (df['year'].isin(years)) &
            (df['quarter'].isin(quarters))
        ]
        top_states = (
            filtered_state.groupby("state")["total_transaction_amount"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.subheader("Top 10 States")
        st.dataframe(top_states, use_container_width=True)

    elif genre == "District":
        query = '''
        SELECT entity_name, year, quarter, SUM(transaction_amount) AS total_transaction_amount
        FROM top_transaction_district
        GROUP BY entity_name, year, quarter
        '''
        df_district = pd.read_sql(query, engine)

        filtered_district = df_district[
            (df_district['year'].isin(years)) &
            (df_district['quarter'].isin(quarters))
        ]
        top_districts = (
            filtered_district.groupby("entity_name")["total_transaction_amount"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.subheader("Top 10 Districts")
        st.dataframe(top_districts, use_container_width=True)
    elif genre == "Postal Codes":
        query = '''
        SELECT entity_name, year, quarter, SUM(transaction_amount) AS total_transaction_amount
        FROM top_transaction_pincode
        GROUP BY entity_name, year, quarter
        '''
        df_pincode= pd.read_sql(query, engine)

        filtered_pincode= df_pincode[
            (df_pincode['year'].isin(years)) &
            (df_pincode['quarter'].isin(quarters))
        ]
        top_pincodes= (
            filtered_pincode.groupby("entity_name")["total_transaction_amount"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.subheader("Top 10 Pincodes")
        st.dataframe(top_pincodes, use_container_width=True)

def top_10_values_user(df_user,years, quarters):
    
    genre1= st.sidebar.radio("Select Level", ["State", "District", "Postal Codes"],horizontal=True)

    if genre1 == "State":
        
        filtered_state_user= df_user[
            (df_user['year'].isin(years)) &
            (df_user['quarter'].isin(quarters))
        ]
        top_states_user = (
            filtered_state_user.groupby("state")["register_user"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.subheader("Top 10 States")
        st.dataframe(top_states_user, use_container_width=True)

    elif genre1 == "District":
        query = '''
        SELECT dis_name, year, qtr, SUM(reg_user) AS total_reg_user
        FROM top_user_dis_data
        GROUP BY dis_name, year, qtr
        '''
        df_district_user= pd.read_sql(query, engine)

        filtered_district_user = df_district_user[
            (df_district_user['year'].isin(years)) &
            (df_district_user['qtr'].isin(quarters))
        ]
        top_districts_user = (
            filtered_district_user.groupby("dis_name")["total_reg_user"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.subheader("Top 10 Districts")
        st.dataframe(top_districts_user, use_container_width=True)

    elif genre1== "Postal Codes":
        query = '''
        SELECT entity_name, year, quarter, SUM(reg_user) AS total_reg_user
        FROM top_user_pin_data
        GROUP BY entity_name, year, quarter
        '''
        df_pincode_user = pd.read_sql(query, engine)

        filtered_pincode_user = df_pincode_user[
            (df_pincode_user['year'].isin(years)) &
            (df_pincode_user['quarter'].isin(quarters))
        ]
        top_pincodes_user = (
            filtered_pincode_user.groupby("entity_name")["total_reg_user"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.subheader("Top 10 Pincodes")
        st.dataframe(top_pincodes_user, use_container_width=True)

def catogory(states,years,quarters):
    # Load and filter data outside the button to ensure proper filtering
    query = '''
    SELECT year,
           state,
           quarter,
           transaction_type,
           SUM(transaction_amount) AS total_transaction_amount
    FROM aggregate_transaction
    GROUP BY transaction_type, state, year, quarter
    '''
    category_df = pd.read_sql(query, engine)

    # Apply filters
    filtered_category = category_df[
        (category_df['state'].isin(states)) &
        (category_df['year'].isin(years)) &
        (category_df['quarter'].isin(quarters))
    ]


    if "show_category" not in st.session_state:
        st.session_state.show_category = False

    if st.sidebar.button("Categories"):
        st.session_state.show_category = not st.session_state.show_category

    if st.session_state.show_category:
        cat_df = (
                filtered_category.groupby('transaction_type')['total_transaction_amount']
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
        st.subheader("📊 Transaction Amount by Category")
        st.dataframe(cat_df, use_container_width=True)
            
      

def main():
    st.sidebar.header("🔍 Filter Transactions")
    if view_option=="Transaction":
        states = st.sidebar.multiselect("Select States", df['state'].unique(), default=df['state'].unique())
        years = st.sidebar.multiselect("Select Year(s)", df['year'].unique(), default=df['year'].unique())
        quarters = st.sidebar.multiselect("Select Quarter(s)", df['quarter'].unique(), default=df['quarter'].unique())

        filtered_df = df[
        (df['state'].isin(states)) &
        (df['year'].isin(years)) &
        (df['quarter'].isin(quarters))
        ]
        metric_transaction(filtered_df)
        st.markdown("---")
        map_transaction(filtered_df)
        st.markdown("---")
        top_10_values(df,years, quarters)
        st.markdown("---")
        catogory(states,years,quarters)

    elif view_option == "User":
        states = st.sidebar.multiselect("Select States", df_user['state'].unique(), default=df_user['state'].unique())
        years = st.sidebar.multiselect("Select Years", df_user['year'].unique(), default=df_user['year'].unique())
        quarters = st.sidebar.multiselect("Select Quarters", df_user['quarter'].unique(), default=df_user['quarter'].unique())

        filtered_user = df_user[
            (df_user['state'].isin(states)) &
            (df_user['year'].isin(years)) &
            (df_user['quarter'].isin(quarters))
        ]
        metric_user(filtered_user)
        st.markdown("---")
        map_user(filtered_user)
        st.markdown("---")
        top_10_values_user(df_user,years, quarters)
        st.markdown("---")

        

main()


                 



    


    






    

    
    
   
   
    
    


    













