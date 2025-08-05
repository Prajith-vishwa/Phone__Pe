import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#sql connection
mydb= psycopg2.connect(host= "localhost",
                       user= "postgres",
                       port= "5432",
                       database= "phonepe_data",
                       password= "Praji")
cursor= mydb.cursor()

#agg_insurance_df
cursor.execute("SELECT * FROM agg_insurance")
mydb.commit()
table1= cursor.fetchall()

Agg_insurance= pd.DataFrame(table1, columns=("States", "Years", "Quarter","Transaction_type",
                                             "Transaction_count", "Transaction_amount"))

#agg_transaction_df
cursor.execute("SELECT * FROM agg_transaction")
mydb.commit()
table2= cursor.fetchall()

Agg_transaction= pd.DataFrame(table2, columns=("States", "Years", "Quarter","Transaction_type",
                                             "Transaction_count", "Transaction_amount"))

#agg_user_df
cursor.execute("SELECT * FROM agg_user")
mydb.commit()
table3= cursor.fetchall()

Agg_user= pd.DataFrame(table3, columns=("States", "Years", "Quarter","Brands",
                                             "Transaction_count", "Percentage"))


#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

Map_insurance= pd.DataFrame(table4, columns=("States", "Years", "Quarter","Districts",
                                             "Transaction_count", "Transaction_amount"))

#map_transaction_df
cursor.execute("SELECT * FROM map_trans")
mydb.commit()
table5= cursor.fetchall()

Map_trans= pd.DataFrame(table5, columns=("States", "Years", "Quarter","Districts",
                                             "Transaction_count", "Transaction_amount"))


#map_users_df
cursor.execute("SELECT * FROM map_users")
mydb.commit()
table6= cursor.fetchall()

Map_users= pd.DataFrame(table6, columns=("States", "Years", "Quarter","Districts",
                                             "RegisteredUsers", "AppOpens"))

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

Top_insurance= pd.DataFrame(table7, columns=("States", "Years", "Quarter"," Pincode",
                                             "Transaction_count", "Transaction_amount"))

#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

Top_transaction= pd.DataFrame(table8, columns=("States", "Years", "Quarter"," Pincode",
                                             "Transaction_count", "Transaction_amount"))


#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

Top_user= pd.DataFrame(table9, columns=("States", "Years", "Quarter"," Pincode",
                                             "RegisteredUsers"))



def Transaction_amount_count_Y(df, year):

    tacy = df[df["Years"] == year]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered, height= 650, width= 600)
        st.plotly_chart(fig_count)


    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale= "Rainbow", 
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2= px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                color="Transaction_count", color_continuous_scale= "Rainbow", 
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy  




def Transaction_amount_count_Y_Q(df, quarter):
    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered, height= 650, width= 600)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale= "Rainbow", 
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1) 
    with col2:

        fig_india_2= px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                color="Transaction_count", color_continuous_scale= "Rainbow", 
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].unique()} YEAR {quarter} QUARTERTRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

def Agg_Tran_Transaction_type(df, state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2= st.columns(2)
    with col1:

        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.3)
        st.plotly_chart(fig_pie_1)
        
    with col2:

        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.3)
        st.plotly_chart(fig_pie_2)


#Agg_User_1

def Agg_User_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence= px.colors.sequential.Agsunset_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Agg_user_2
def Agg_User_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)


    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence= px.colors.sequential.BuPu_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Agg_user_3
def Agg_User_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace=True)
    

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION AMOUNT, PERCENTAGE",width=1000, markers= True)
    st.plotly_chart(fig_line_1)

#Map_insurance_districts
def Map_ins_Districts(df, state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "Districts", orientation= "h", height=600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.deep)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "Districts", orientation= "h", height=600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.amp)
        st.plotly_chart(fig_bar_2)

# Map_user_plot_1
def Map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg=muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{year} REGISTERED USERS AND APPOPENS",width=1000, height=800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# Map_user_plot_2
def Map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg=muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{df['Years'].min()} YEARS {quarter} QUARETER REGISTERED USERS AND APPOPENS",width=1000, height=800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#Map_user_plot_3
def Map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUsers", y= "Districts", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height=800, color_discrete_sequence= px.colors.sequential.Bluered)
        st.plotly_chart(fig_map_user_bar_1)
        
    with col2:
        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "Districts", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height=800, color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_map_user_bar_2)

#Top_ins_plot_1
def Top_ins_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_ins_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= " Pincode",
                                title= "TRANSACTION AMOUNT", height=650,width=600, color_discrete_sequence= px.colors.sequential.amp_r)
        st.plotly_chart(fig_top_ins_bar_1)

    with col2:
        fig_top_ins_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= " Pincode",
                                title= "TRANSACTION COUNT", height=650,width=600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_ins_bar_2)

#Top_user_plot_1
def Top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)
    
    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)
    

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width=1000, height=800,
                        color_discrete_sequence= px.colors.sequential.Blugrn, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#Top_user_plot_2
def Top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "RUPQ",
                        width=1000, height= 800, color= "RegisteredUsers", hover_data= " Pincode",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

#sql connection
def Top_chart_transaction_amount(table_name):
    mydb= psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database= "phonepe_data",
                        password= "Praji")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("states", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="states", y="transaction_amount", title="TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600, hover_name= "states")
        st.plotly_chart(fig_amount_1)


    #plot_2
    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''
    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("states", "transaction_amount"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650, width= 600, hover_name= "states")
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="TRANSACTION AMOUNT", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered, height= 800, width= 1000, hover_name= "states")
    st.plotly_chart(fig_amount_3)

#sql connection
def Top_chart_transaction_count(table_name):
    mydb= psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database= "phonepe_data",
                        password= "Praji")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("states", "transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="states", y="transaction_count", title="TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600, hover_name= "states")
        st.plotly_chart(fig_amount_1)


    #plot_2
    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''
    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("states", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title="TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650, width= 600, hover_name= "states")
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title="TRANSACTION COUNT", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered, height= 800, width= 1000, hover_name= "states")
    st.plotly_chart(fig_amount_3)




#streamlit part


st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select= option_menu("Main Menu",["HOME", "DATA EXPLORATION", "CHARTS"])

if select== "HOME":

     # Full-width image
    st.image(r"C:\Users\rpraj\OneDrive\Desktop\Phonepe\images.jpeg", width=850)

    # Main Header
    st.markdown("<h1 style='color:#6C3483; text-align:center;'> PHONEPE INDIA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>India’s Best Digital Transaction App</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Section 1: Intro
    st.markdown("###  Welcome to PhonePe")
    st.markdown("""
    PhonePe is India’s most trusted digital payments app, allowing secure and fast transactions anytime, anywhere.  
    Experience convenience, security, and rewards with every payment you make using PhonePe.
    """)

    # Section 2: Features
    st.markdown("### Core Features")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("- **Credit & Debit Card Linking**")
        st.markdown("- **Check Bank Balance Instantly**")
        st.markdown("- **Secure Money Storage**")
        st.image(r"C:\Users\rpraj\OneDrive\Desktop\Phonepe\download.png", width=400)

    with col2:
        st.markdown("- **PIN-Based Authorization**")
        st.markdown("- **Quick & Easy UPI Payments**")
        

    # Section 3: Why Choose PhonePe
    st.markdown("###  Why Choose PhonePe?")
    st.markdown("""
    -  One App For All Your Payments  
    -  Easy & Fast Transactions  
    -  Your Bank Account Is All You Need  
    -  Shop Anywhere with PhonePe Merchants  
    -  Multiple Ways To Pay (Direct Transfer, QR Code)  
    -  Earn Rewards with Every Use
    """)
    st.image(r"C:\Users\rpraj\OneDrive\Desktop\Phonepe\download.jpeg", width=400)

    # Section 4: Additional Benefits
    st.markdown("### Additional Benefits")
    st.markdown("""
    -  No Wallet Top-Up Required  
    -  Pay Directly from Any Bank  
    -  Instant Transfers — Absolutely Free  
    -  100% Secure and RBI-Compliant  
    """)

    # Section 5: Download Button (Saves a dummy text file)
    st.markdown("### Download Now")
    st.download_button(
        label="DOWNLOAD THE APP INFO", 
        data="Visit https://www.phonepe.com/app-download/ to download the PhonePe app.",
        file_name="PhonePe_Info.txt",
        mime="text/plain"
    )

    # External Link
    st.markdown(" [Visit Official PhonePe Website](https://www.phonepe.com/app-download/)", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:grey;'> R. PRAJITH VISHWA </p>", unsafe_allow_html=True)





elif select== "DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["AGGREGATED ANALYSIS", "MAP ANALYSIS", "TOP ANALYSIS"])

    with tab1:
        method = st.radio("Select The Method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year", Agg_insurance["Years"].min(), Agg_insurance["Years"].max(), Agg_insurance["Years"].min())
            tac_Y= Transaction_amount_count_Y(Agg_insurance, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)

        elif method == "Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year", Agg_transaction["Years"].min(), Agg_transaction["Years"].max(), Agg_transaction["Years"].min())
            Agg_tran_tac_Y= Transaction_amount_count_Y(Agg_transaction, years)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State", Agg_tran_tac_Y["States"].unique())

            Agg_Tran_Transaction_type(Agg_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter", Agg_tran_tac_Y["Quarter"].min(), Agg_tran_tac_Y["Quarter"].max(), Agg_tran_tac_Y["Quarter"].min())
            Agg_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Agg_tran_tac_Y, quarters)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_ty", Agg_tran_tac_Y["States"].unique())

            Agg_Tran_Transaction_type(Agg_tran_tac_Y_Q, states)


        elif method == "User Analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year", Agg_user["Years"].min(), Agg_user["Years"].max(), Agg_user["Years"].min())
            Agg_user_Y= Agg_User_plot_1(Agg_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter", Agg_user_Y["Quarter"].min(), Agg_user_Y["Quarter"].max(), Agg_user_Y["Quarter"].min())
            Agg_user_Y_Q= Agg_User_plot_2(Agg_user_Y, quarters)


            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State", Agg_user_Y_Q["States"].unique())

            Agg_User_plot_3(Agg_user_Y_Q, states)


    with tab2:
        method_2 = st.radio("Select The Method", ["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi", Map_insurance["Years"].min(), Map_insurance["Years"].max(), Map_insurance["Years"].min())
            Map_ins_tac_Y= Transaction_amount_count_Y(Map_insurance, years)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_mi", Map_ins_tac_Y["States"].unique())

            Map_ins_Districts(Map_ins_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mi", Map_ins_tac_Y["Quarter"].min(), Map_ins_tac_Y["Quarter"].max(), Map_ins_tac_Y["Quarter"].min())
            Map_ins_tac_Y_Q= Transaction_amount_count_Y_Q(Map_ins_tac_Y, quarters)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_mi", Map_ins_tac_Y_Q["States"].unique())

            Map_ins_Districts(Map_ins_tac_Y_Q, states)


        elif method_2 == "Map Transaction":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mt", Map_trans["Years"].min(), Map_trans["Years"].max(), Map_trans["Years"].min())
            Map_tran_tac_Y= Transaction_amount_count_Y(Map_trans, years)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_mi", Map_tran_tac_Y["States"].unique())

            Map_ins_Districts(Map_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mt", Map_tran_tac_Y["Quarter"].min(), Map_tran_tac_Y["Quarter"].max(), Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Map_tran_tac_Y, quarters)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_mt", Map_tran_tac_Y_Q["States"].unique())

            Map_ins_Districts(Map_tran_tac_Y_Q, states)
         
        
        elif method_2 == "Map User":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mu", Map_users["Years"].min(), Map_users["Years"].max(), Map_users["Years"].min())
            Map_user_Y= Map_user_plot_1(Map_users, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mu", Map_user_Y["Quarter"].min(), Map_user_Y["Quarter"].max(), Map_user_Y["Quarter"].min())
            Map_user_Y_Q= Map_user_plot_2(Map_user_Y, quarters)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_mu", Map_user_Y_Q["States"].unique())

            Map_user_plot_3(Map_user_Y_Q, states)  



    with tab3:
        method_3 = st.radio("Select The Method", ["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_ti", Top_insurance["Years"].min(), Top_insurance["Years"].max(), Top_insurance["Years"].min())
            Top_ins_tac_Y= Transaction_amount_count_Y(Top_insurance, years)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_ti", Top_ins_tac_Y["States"].unique())

            Top_ins_plot_1(Top_ins_tac_Y, states)
           
            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_ti", Top_ins_tac_Y["Quarter"].min(), Top_ins_tac_Y["Quarter"].max(), Top_ins_tac_Y["Quarter"].min())
            Top_ins_tac_Y_Q= Transaction_amount_count_Y_Q(Top_ins_tac_Y, quarters)


        elif method_3 == "Top Transaction":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tt", Top_transaction["Years"].min(), Top_transaction["Years"].max(), Top_transaction["Years"].min())
            Top_tran_tac_Y= Transaction_amount_count_Y(Top_transaction, years)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_tt", Top_tran_tac_Y["States"].unique())

            Top_ins_plot_1(Top_tran_tac_Y, states)
           
            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_tt", Top_tran_tac_Y["Quarter"].min(), Top_tran_tac_Y["Quarter"].max(), Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Top_tran_tac_Y, quarters)



        elif method_3 == "Top User":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tu", Top_user["Years"].min(), Top_user["Years"].max(), Top_user["Years"].min())
            Top_user_tac_Y= Top_user_plot_1(Top_user, years)

            col1,col2= st.columns(2) 
            with col1:
                states= st.selectbox("Select The State_tu", Top_user_tac_Y["States"].unique())

            Top_user_plot_2(Top_user_tac_Y, states)        

elif select== "CHARTS":
    
    question= st.selectbox("Select The Question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                   "2. Transaction Amount and Count of Map Insurance",
                                                   "3. Transaction Amount and Count of Top Insurance",
                                                   "4. Transaction Amount and Count of Aggregated Transaction",
                                                   "5. Transaction Amount and Count of Map Transaction",
                                                   "6. Transaction Amount and Count of Top Transaction",
                                                   "7. Transaction Count of Aggregated User",])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("agg_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("agg_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("agg_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("agg_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_trans")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_trans")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("agg_user")

    