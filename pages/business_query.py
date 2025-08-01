import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="📱 PhonePe Pulse - Home", layout="wide")

engine = create_engine("postgresql+psycopg2://sindhulocal:7356@localhost:5432/newphonepay")

view_option = st.sidebar.selectbox("Choose Data Type", ["Decoding Transaction Dynamics on PhonePe",
                                                        "Insurance Penetration and Growth Potential Analysis",
                                                        "Transaction Analysis for Market Expansion",
                                                         "User Engagement and Growth Strategy",
                                                         "Insurance Transactions Analysis"])

if view_option=="Decoding Transaction Dynamics on PhonePe":

###Query 1-state,Year, quarter wise total transaction and Total Count 

    query='''select state,
    year
    quarter,
    SUM(transaction_count) as total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM aggregate_transaction
    GROUP BY state,year,quarter
    ORDER BY state,year,quarter'''
    total_transaction=pd.read_sql(query,engine)
    st.subheader("State,Year, quarter wise total transaction and Total Count")
    st.dataframe(total_transaction)

    ###2.Top 10 states
    query='''SELECT
    state,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM aggregate_transaction
    GROUP BY state
    ORDER BY SUM(transaction_amount) desc
    limit 10'''
    top_states=pd.read_sql(query,engine)
    st.subheader("Top 10 states")
    st.dataframe(top_states)
    fig, ax = plt.subplots(figsize=(15, 6))
    sns.barplot(data=top_states,x='state',y='total_transaction_amount',ax=ax, palette="magma",width=0.5)
    ax.set_title("Top States by Amount")
    ax.set_xlabel("State")
    ax.set_ylabel("Amount")
    st.pyplot(fig)

    ###3.bottom 10 states
    query='''SELECT
    state,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM aggregate_transaction
    GROUP BY State
    ORDER BY SUM(transaction_amount) asc
    limit 10'''
    botttom_states=pd.read_sql(query,engine)
    st.subheader("Bottom 10 states")
    st.dataframe(botttom_states)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=botttom_states,x='state',y='total_transaction_amount',ax=ax, palette="magma",width=0.5)
    ax.set_title("Bottom States by Amount")
    ax.set_xlabel("State")
    ax.set_ylabel("Amount")
    st.pyplot(fig)

    ###5.top 5 categary 
    query='''SELECT 

    transaction_type,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM aggregate_transaction
    GROUP BY transaction_type
    ORDER BY SUM(transaction_amount) desc'''
    top_Categary=pd.read_sql(query,engine)
    st.subheader("Category wise payment")
    st.dataframe(top_Categary)
    fig=px.pie(top_Categary,
               names='transaction_type',
               values='total_transaction_amount',
               hole=0.4)
    st.plotly_chart(fig)
if view_option=="Insurance Penetration and Growth Potential Analysis":
    ###query 1: State, Year, Qtr wise tolal insurance transaction count and amount
    st.markdown('------')
    query=''' SELECT
    state,
    year,
    quarter,
    transaction_type,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transction_amount
    FROM aggregate_insurance
    GROUP BY state,year,quarter,transaction_type
    ORDER BY state,year,quarter
    ''' 
    total_insurance=pd.read_sql(query,engine)
    st.subheader("State, Year, Qtr wise tolal insurance transaction count and amount")
    st.dataframe(total_insurance)
    st.markdown('------')

    ###Query 2: top 10 state based on transaction amount
    query='''SELECT
    state,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM aggregate_insurance
    GROUP BY state
    ORDER BY SUM(transaction_amount) desc
    limit 10'''
    top_state=pd.read_sql(query,engine)
    st.subheader('🔝Top 10 state based on transaction amount')
    fig, ax = plt.subplots(figsize=(15, 6))
    sns.barplot(data=top_state,x='state',y='total_transaction_amount',ax=ax,palette="magma",width=0.5)
    ax.set_title("Top 10 state based on transaction amount")
    ax.set_xlabel("state")
    ax.set_ylabel("transaction amount")
    st.pyplot(fig)
    st.markdown('------')
    ###Query 3: bottom 10 state based on transaction count
    query='''SELECT
    state,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM aggregate_insurance
    GROUP BY state
    ORDER BY SUM(transaction_amount) asc
    limit 10'''
    bottom_state=pd.read_sql(query,engine)
    st.subheader('Bottom 10 state based on transaction amount')
    fig, ax=plt.subplots(figsize=(15,6))
    sns.barplot(data=bottom_state,x='state',y='total_transaction_amount',palette="coolwarm",width=0.5,ax=ax)
    ax.set_title('bottom 10 state based on transaction count')
    ax.set_xlabel('state')
    ax.set_ylabel('transaction amount')
    ax.tick_params(axis='x', rotation=60)
    st.pyplot(fig)
    st.markdown('------')

    ### query 4:quarter has highest transaction
    query='''
    SELECT
    quarter,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM aggregate_insurance
    GROUP BY quarter
    ORDER BY SUM(transaction_amount)desc'''
    qtr_rank=pd.read_sql(query,engine)
    st.subheader('Quarter has highest transaction')
    fig=px.pie(qtr_rank, names='quarter', values='total_transaction_amount')
    st.plotly_chart(fig)
    st.markdown('------')
    ###Query 5: year on year growth
    query = '''
    WITH yearly_growth AS (
    SELECT 
    year,
    SUM("transaction_amount") AS total_transaction_amount
    FROM aggregate_insurance
    GROUP BY year)
    SELECT
    year,
    total_transaction_amount,
    COALESCE(LAG(total_transaction_amount) OVER (ORDER BY year), 0) AS previous_year_transaction,
    ROUND(((total_transaction_amount - COALESCE(LAG(total_transaction_amount) OVER (ORDER BY year), 0)) * 100.0 / 
        NULLIF(COALESCE(LAG(total_transaction_amount) OVER (ORDER BY year), 0), 0))::NUMERIC,0) AS growth_percentage
    FROM yearly_growth 
    ORDER BY year
    '''
    y_o_y = pd.read_sql(query, engine)
    y_o_y['growth_percentage']=y_o_y['growth_percentage'].fillna(0).astype(int)
    st.subheader("year on year growth")
    st.dataframe(y_o_y)
    fig=px.line(y_o_y, x='year', y='growth_percentage')
    st.plotly_chart(fig)

if view_option== "Transaction Analysis for Market Expansion":
    ###query 1:State and year wise total_transaction_count and total_transaction_amount
    query=''' select
    state,
    year,
    district,
    SUM(transacion_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM map_transaction
    GROUP BY state,year,district
    ORDER BY state,year,district
    '''
    a=pd.read_sql(query,engine)
    st.subheader("State and year wise total_transaction_count and total_transaction_amount")
    st.dataframe(a)

    ###query2 2: Top 10 district
    query='''SELECT
    district,
    SUM(transaction_amount) AS total_transaction_amount
    FROM map_transaction
    GROUP BY district
    ORDER BY SUM(transaction_amount) desc
    limit 10'''
    top_district=pd.read_sql(query,engine)
    st.subheader("Top 10 district")
    fig,ax=plt.subplots(figsize=(15,6))
    sns.barplot(data=top_district,x="district",y="total_transaction_amount",palette="Set2",width=0.5)
    ax.set_title("Top 10 district")
    ax.set_xlabel("district")
    ax.set_ylabel("transaction_count")
    ax.tick_params(axis='x', rotation=60)
    st.pyplot(fig)

    ###query 3: bottom 10 district
    query='''SELECT
    district,
    SUM(transaction_amount) AS total_transaction_amount
    FROM map_transaction
    GROUP BY district
    ORDER BY SUM(transaction_amount) asc
    limit 10'''
    top_district=pd.read_sql(query,engine)
    st.subheader("bottom 10 district")
    fig,ax=plt.subplots(figsize=(15,6))
    sns.barplot(data=top_district,x="district",y="total_transaction_amount",palette="Set2",width=0.5)
    ax.set_title("bottom 10 district")
    ax.set_xlabel("district")
    ax.set_ylabel("transaction_count")
    ax.tick_params(axis='x', rotation=60)
    st.pyplot(fig)

    ###query 4:district which growing above 80%
    query='''WITH state_transaction AS (SELECT 
    state,
    year,
    SUM(transaction_amount) as total_transaction_amount
    from map_transaction
    group by state,year
    order by state,year),

    cumulative_calc AS(SELECT
    state,
    year,
    total_transaction_amount,
    SUM(total_transaction_amount) OVER(partition by state order by year 
        ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as running_transaction
    FROM state_transaction
    ORDER BY state,year
    ),

    state_total as(SELECT
    state,
    sum(total_transaction_amount) AS total_transaction_amount
    from cumulative_calc
    group by state
    ),

    running_state AS (
    SELECT
    state,
    running_transaction AS till_previous_year
    FROM cumulative_calc 
    WHERE year = '2024'
    ),

    growth_percentage AS (SELECT s.state,s.total_transaction_amount, r.till_previous_year from state_total s 
    join running_state r on s.state=r.state),

    final_transaction AS(SELECT state,
    total_transaction_amount,
    till_previous_year,
    ROUND(((total_transaction_amount-till_previous_year)*100.0/NULLIF(till_previous_year,0))::numeric,2) as growth_percentage
    FROM growth_percentage)

    select * from final_transaction
    where growth_percentage >=80


    '''
    b=pd.read_sql(query,engine)
    st.subheader("states growing percentage above 80%")
    st.dataframe(b) 
    
    ###query 5:district which growing below 30
    query='''WITH state_transaction AS (SELECT 
    state,
    year,
    SUM(transaction_amount) as total_transaction_amount
    from map_transaction
    group by state,year
    order by state,year),

    cumulative_calc AS(SELECT
    state,
    year,
    total_transaction_amount,
    SUM(total_transaction_amount) OVER(partition by state order by year 
        ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as running_transaction
    FROM state_transaction
    ORDER BY state,year
    ),

    state_total as(SELECT
    state,
    sum(total_transaction_amount) AS total_transaction_amount
    from cumulative_calc
    group by state
    ),

    running_state AS (
    SELECT
    state,
    running_transaction AS till_previous_year
    FROM cumulative_calc 
    WHERE year = '2024'
    ),

    growth_percentage AS (SELECT s.state,s.total_transaction_amount, r.till_previous_year from state_total s 
    join running_state r on s.state=r.state),

    final_transaction AS(SELECT state,
    total_transaction_amount,
    till_previous_year,
    ROUND(((total_transaction_amount-till_previous_year)*100.0/NULLIF(till_previous_year,0))::numeric,2) as growth_percentage
    FROM growth_percentage)

    select * from final_transaction
    where growth_percentage <=40
    '''
    b=pd.read_sql(query,engine)
    st.subheader("states growing percentage below 40")
    st.dataframe(b)


if view_option =="User Engagement and Growth Strategy":
    st.markdown('---')
    ###User Engagement and Growth Strategy
    ###query 1: Total register_user state and year wise
    query='''
    SELECT state,
    year,
    SUM(count) as registratoin_user,
    SUM(appopen) as total_appOpens
    FROM map_user
    group by state,year
    order by state,year
    '''
    register_user=pd.read_sql(query,engine)
    st.subheader("Total register_user state and year wise")
    st.dataframe(register_user)
    st.markdown('------')

    ### YOY growth percentage state wise
    query='''
    SELECT state,
    year,
    SUM(count) as total_register_user,
    COALESCE(lag(SUM(count)) over(partition by state order by year),0) AS previous_year_register,
    ROUND((SUM(count)-lag(SUM(count)) over(partition by state order by year))*100/
        NULLIF(lag(SUM(count)) over(partition by state order by year),0)) as growth_percentage
    FROM map_user
    GROUP BY state,year
    ORDER BY state,year
    '''
    YOY=pd.read_sql(query,engine)
    st.subheader('Year-over-Year User Growth (%) by State')
    st.dataframe(YOY)
    fig = px.line(YOY, x='year', y='growth_percentage', color='state',
              markers=True, title='Year-over-Year User Growth (%) by State')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('-------')

    ###Growth percentage by year
    query='''SELECT year,
    SUM(count) as total_register_user,
    COALESCE(lag(SUM(count)) over( order by year),0) AS previous_year_register,
    ROUND((SUM(count)-lag(SUM(count)) over(order by year))*100/
        NULLIF(lag(SUM(count)) over( order by year),0)) as growth_percentage
    FROM map_user
    GROUP BY year
    ORDER BY year'''
    year_wise=pd.read_sql(query,engine)
    st.subheader('Growth percentage by year')
    st.dataframe(year_wise)
    fig = px.line(year_wise, x='year', y='growth_percentage',
              markers=True, title='Year-over-Year User Growth')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('------')

    ##Top 10 district 
    query='''select district,
    SUM(count) AS total_register_user
    FROM map_user
    GROUP BY district
    ORDER BY SUM(count) desc
    LIMIT 10
    '''
    top_district_user=pd.read_sql(query,engine)
    st.subheader('top 10 district by registeruser ')
    fig=px.bar(top_district_user, x='district', y='total_register_user', color='district')
    st.plotly_chart(fig)
    st.markdown('-----')

    ###Bottom 10 district

    query='''select district,
    SUM(count) AS total_register_user
    FROM map_user
    GROUP BY district
    ORDER BY SUM(count) asc
    LIMIT 10
    '''
    bottom_district_user=pd.read_sql(query,engine)
    st.subheader('Bottom 10 district by registeruser ')
    fig=px.bar(bottom_district_user, x='district', y='total_register_user', color='district')
    st.plotly_chart(fig)
    st.markdown('------')

if view_option=="Insurance Transactions Analysis":
    col1, col2 = st.columns(2)
    with col1:
        year = st.sidebar.selectbox("Select Year", [2020, 2021, 2022, 2023,2024])
    with col2:
        quarter = st.sidebar.multiselect("Select Quarter", [1, 2, 3, 4],default=[1,2,3,4])
        quarter_str = ','.join(map(str, quarter))


    ## top 10 distrct
    query = '''
    SELECT
    state,
    dis_name,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM top_insurance_district
     WHERE year::int = %s AND quarter::int = ANY(%s)
    GROUP BY state, dis_name
    ORDER BY total_transaction_amount DESC
    LIMIT 10;
    '''

    df = pd.read_sql(query, engine, params=(year, quarter))
    st.subheader("Top 10 district insurance transaction")
    st.dataframe(df)

    fig_district_top= px.bar(df,
    x='dis_name',
    y='total_transaction_amount',
    color='state',
    title=f"Top 10 Districts by Insurance Transaction Amount - Q{','.join(map(str, quarter))} {year}",
    labels={'total_transaction_amount': 'Insurance Amount (₹)', 'dis_name': 'District'},
    height=500)
    st.plotly_chart(fig_district_top, key="district_chart_top")

    ## Bottom 10 distrct
    query = '''
    SELECT
    state,
    dis_name,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM top_insurance_district
    WHERE year::int = %s AND quarter::int = ANY(%s)
    GROUP BY state, dis_name
    ORDER BY total_transaction_amount ASC 
    LIMIT 10;
    '''

    bottom_df = pd.read_sql(query, engine, params=(year, quarter))
    st.subheader("Bottom 10 district insurance transaction")
    st.dataframe(bottom_df)

    fig_district_bottom = px.bar(bottom_df,
    x='dis_name',
    y='total_transaction_amount',
    color='state',
    title=f"Bottom 10 Districts by Insurance Transaction Amount - Q{','.join(map(str, quarter))} {year}",
    labels={'total_transaction_amount': 'Insurance Amount (₹)', 'dis_name': 'District'},
    height=500)
    st.plotly_chart(fig_district_bottom, use_container_width=True,key="fig_district_bottom")

    ##top 10 pincode
    query ='''
    SELECT
        state,
        entity_name,
        SUM(transaction_count) AS total_transaction_count,
        SUM(transaction_amount) AS total_transaction_amount
    FROM top_insurance_pincode
    WHERE year::int = %s AND quarter::int = ANY(%s)
    GROUP BY state, entity_name
    ORDER BY total_transaction_amount DESC
    LIMIT 10;
    '''

    df_top_pincode = pd.read_sql(query, engine, params=(year, quarter))
    df_top_pincode['entity_name'] = df_top_pincode['entity_name'].astype(str)
    df_top_pincode['entity_name'] = pd.Categorical(df_top_pincode['entity_name'], categories=df_top_pincode['entity_name'], ordered=True)


    st.subheader("Top 10 Pincode Insurance Transactions")
    st.dataframe(df_top_pincode)

    fig_pincode_top = px.bar(
        df_top_pincode,
        x='entity_name',
        y='total_transaction_amount',
        color='state',
        text='total_transaction_amount',
        title=f"Top {len(df_top_pincode)} Pincode(s) by Insurance Transaction Amount - Q{','.join(map(str, quarter))} {year}",
        labels={
            'entity_name': 'Pincode',
            'total_transaction_amount': 'Insurance Amount (₹)'
        },
        height=500
    )
    fig_pincode_top.update_traces(
        texttemplate='%{text:.2s}',
        textposition='outside',
        width=0.5
    )
    fig_pincode_top.update_layout(
        xaxis_title='Pincode',
        yaxis_title='Insurance Amount (₹)',
        xaxis_type='category',  # ✅ Ensures correct categorical bar plot
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    st.plotly_chart(fig_pincode_top, use_container_width=True, key="pincode_chart_top")
    
    ##Bottomm 10 pincode
    query = '''
    SELECT
        state,
        entity_name,
        SUM(transaction_count) AS total_transaction_count,
        SUM(transaction_amount) AS total_transaction_amount
    FROM top_insurance_pincode
    WHERE year::int = %s AND quarter::int = ANY(%s)
    GROUP BY state, entity_name
    ORDER BY total_transaction_amount asc
    LIMIT 10;
    '''

    df_bottom_pincode = pd.read_sql(query, engine, params=(year, quarter))
    df_bottom_pincode['entity_name'] = df_bottom_pincode['entity_name'].astype(str)
    df_bottom_pincode['entity_name'] = pd.Categorical(df_bottom_pincode['entity_name'], categories=df_bottom_pincode['entity_name'], ordered=True)


    st.subheader("Top 10 Pincode Insurance Transactions")
    st.dataframe(df_bottom_pincode)

    fig_pincode_bottom = px.bar(
        df_bottom_pincode,
        x='entity_name',
        y='total_transaction_amount',
        color='state',
        text='total_transaction_amount',
        title=f"Top {len(df_bottom_pincode)} Pincode(s) by Insurance Transaction Amount - Q{','.join(map(str, quarter))} {year}",
        labels={
            'entity_name': 'Pincode',
            'total_transaction_amount': 'Insurance Amount (₹)'
        },
        height=500
    )
    fig_pincode_bottom.update_traces(
        texttemplate='%{text:.2s}',
        textposition='outside',
        width=0.5
    )
    fig_pincode_bottom.update_layout(
        xaxis_title='Pincode',
        yaxis_title='Insurance Amount (₹)',
        xaxis_type='category',  # ✅ Ensures correct categorical bar plot
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    st.plotly_chart(fig_pincode_bottom, use_container_width=True, key="pincode_chart_bottom")

    ###year and quarter wise

    query='''SELECT 
    year,
    quarter,
    SUM(transaction_count) AS total_transaction_count,
    SUM(transaction_amount) AS total_transaction_amount
    FROM top_insurance_district 
    GROUP BY year, quarter
    ORDER BY year, quarter'''
    df_year=pd.read_sql(query,engine,)
    st.subheader("Year and Quarter wise insurance transaction")
    st.dataframe(df_year)
    fig_year= px.bar(
        df_year,
        x='year',
        y='total_transaction_amount',
        color='year',
        title=f"year by Insurance Transaction Amount ",
        labels={
            'year': 'Years',
            'total_transaction_amount': 'Insurance Amount (₹)'
        },
        height=500,
        
    )
    
    st.plotly_chart(fig_year, use_container_width=True, key="year and quartes wise")



        


   






    







    

        


