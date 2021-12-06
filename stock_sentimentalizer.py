import streamlit as st
import spacy_streamlit
import pandas as pd
from streamlit.proto import DataFrame_pb2
import yfinance as yfs
import mplfinance as mpf
from matplotlib import pyplot as plt
import mplfinance as mpf
import plotly.express as px
import yahoo_fin.stock_info as yf
import requests
import urllib
from src import companyinfo
from src import piotroski_with_chart
from src import piotroski
from src import benish
from src import sentimentanalyzer
from src import index
from src import fundamental
from src import techanalysis
# from PIL import Image
plt.style.use("ggplot")

hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
</style>
"""

st.markdown(hide_st_style,unsafe_allow_html=True)

category= []
company_name=[]
stock_indices = ["-","NIFTY50","DOW","FTSE100","NASDAQ","SP500"]
api_key = '5df285c077779f8519c2bc667ae30191'
def retrieve_companyname(data,fetch,tic):
    data = data.dropna()
    comp_name= list(data[fetch])
    ticker = list(data[tic])
    return comp_name,ticker

st.title("Stock sentimentalizer")
st.sidebar.title("Stock sentimentalizer")

#Sidebar ends

# my_expander = st.sidebar.beta_expander(label="Company's Profile")
# with my_expander:

menu = st.sidebar.selectbox("Let's Explore",["About","Sentiment","Help"],index =0)


#Start of main page
if menu == 'About':
    try:
        st.title('About')
        st.markdown('''
    While it is hard to quantify the impact of news or unexpected developments inside a company, industry, or the global economy, you can't argue that it does influence investor sentiment. The political situation, negotiations between countries or companies, product breakthroughs, mergers and acquisitions, and other unforeseen events can impact stocks and the stock market. Since securities trading happens across the world and markets and economies are interconnected, news in one country can impact investors in another, almost instantly.

    News related to a specific company, such as the release of a company's earnings report, can also influence the price of a stock (particularly if the company is posting after a bad quarter).

    In general, strong earnings generally result in the stock price moving up (and vice versa). But some companies that are not making that much money still have a rocketing stock price. This rising price reflects investor expectations that the company will be profitable in the future. However, regardless of the stock price, there are no guarantees that a company will fulfill investors' current expectations of becoming a high-earning company in the future.
    ''')

        st.subheader('Hence we took a stand to analyze the sentiment')
        
        video_file = open("captain.mp4", "rb").read()

        st.video(video_file)
        st.subheader('"Whatever It takes"')
        
        # longName,symbol,logo,industry,phone,website,summary = companyinfo.info(symbol)
        # co_name = longName
        # st.markdown('''
        # # {} - {}'''.format(longName,symbol))
        # st.image(logo)
        # st.markdown('''
        # ## Industry type: {}
        # {}
        # ## Contact details
        # - phone no.- {}
        # - website - {}
        # '''.format(industry,summary,phone,website))
    except:
        st.info('Please select one symbol')
elif menu == 'Help':
    try:
        st.title('How to use this web app')
        st.subheader('There exist three steps:')
        st.subheader('Step - 1:')
        st.markdown('''
        - Select a stock from the index / Type the ticker symbol
        ''')
        st.subheader('Step - 2:')
        st.markdown('''
        - View the Sentiment section to know about the sentiment, news and key entitites present in it.
        ''')

        st.subheader('Step - 3:')
        video_file = open("step.mp4", "rb").read()

        st.video(video_file)
        
    except :

        st.info('There some issue in loading in this page')
        

elif menu =="Sentiment":
    st.subheader("News Sentiment Analyzer")
    search = st.radio("Choose one of the option: ",["Type the ticker","Search for ticker in stock index list"],index = 0)
    if search == "Type the ticker":
        symbol = st.text_input("Ticker of the company")
        try:
            # holder = yf.get_holders(symbol)
            comp_name = yfs.Ticker(symbol).info['longName']
            st.write("You have a selected {} and the ticker is {}".format(comp_name,symbol))
            
            st.success('Fetch the ticker')
        except:
            st.error('Unable to fetch the ticker')
        
    else:
 
        category = st.selectbox("Select a stock index ",stock_indices)
        data = index.extract_tickers()
        # print(data)
        if category == "-":
            st.info('Please select one index from dropdown')
        if category == "NIFTY50":
            company_name = list(data["NIFTY50"].keys())
            # print(company_name)
            ticker = [data['NIFTY50'][cname]['Symbol']+'.NS' for cname in company_name]
            # print(company_name)
            # print(ticker)
        if category == "DOW":
            company_name = list(data["DOW"].keys())
            # print(company_name)
            ticker = [data["DOW"][cname]['Symbol'] for cname in company_name]
            # print(ticker)
        if category == "FTSE100":
            # data = yf.tickers_ftse100(True)
            # company_name,ticker = retrieve_companyname(data,'Company','EPIC')
            company_name = list(data["FTSE100"].keys())
            # print(company_name)
            ticker = [data["FTSE100"][cname]['Symbol'] for cname in company_name]
            # print(ticker)
        if category == "FTSE250":
            # data = yf.tickers_ftse250(True)
            # company_name,ticker = retrieve_companyname(data,'Company',"Ticker")
            company_name = list(data["FTSE250"].keys())
            # print(company_name)
            ticker = [data["FTSE250"][cname]['Symbol'] for cname in company_name]
            # print(ticker)
        if category == "NASDAQ":
            # data = yf.tickers_nasdaq(True)
            # company_name,ticker = retrieve_companyname(data,'Security Name',"Symbol")
            company_name = list(data["NASDAQ"].keys())
            # print(company_name)
            ticker = [data["NASDAQ"][cname]['Symbol'] for cname in company_name]
            # print(ticker)
        if category == "SP500":
            # data = yf.tickers_sp500(True)
            # company_name,ticker = retrieve_companyname(data,'Security',"Symbol")
            company_name = list(data["SP500"].keys())
            # print(company_name)
            ticker = [data["SP500"][cname]['Symbol'] for cname in company_name]
            # print(ticker)
        
        if len(company_name)==0:
            st.sidebar.info('Please wait fetching the details')
        else:
            st.write("Total no. of companies : {}".format(len(company_name)))
            st.success('Fetched all the details')
            company = st.selectbox("Select a company",company_name)
            symbol = ticker[company_name.index(company)]
            if symbol:
                st.write("You have a selected {} and the ticker is {}".format(company,symbol))

    newsdata = companyinfo.fetch_news(symbol)
    sent_score = []
    postive_news = 0
    negative_news = 0
    neutral_news = 0
    total_news = len(newsdata)
    
    if total_news != 0:
        my_expander = st.beta_expander(label='View News')
        with my_expander:
            for news in newsdata:
                summary = news['summary']
                link = news['link']
                title = news['title']
                date = news['published']
                docx,sentiment_score,sub_words,text_summary,key_entity = sentimentanalyzer.sentiment(summary)
                st.subheader(title)
                st.write('''published date: {}'''.format(date))
                if text_summary:
                    st.markdown(text_summary)
                else:    
                    st.write(summary)
                st.markdown('''*Key-entities - {} *'''.format(key_entity))
                sent_score.append(sentiment_score)
                if sentiment_score > 0: 
                    postive_news+=1
                    st.markdown('''<p style="color:green">Sentiment score = {:.3f}</p>
                '''.format(sentiment_score), unsafe_allow_html=True)
                elif sentiment_score == 0:
                    neutral_news+=1
                    st.markdown('''<p>Sentiment score = {:.3f}</p>
                '''.format(sentiment_score), unsafe_allow_html=True)

                else:
                    negative_news+=1
                    st.markdown('''<p style="color:red">Sentiment score = {:.3f}.</p>
                '''.format(sentiment_score), unsafe_allow_html=True)

                st.markdown('''[click here to read more]({})'''.format(link))

        avg_sentiment = sum(sent_score)/total_news
        st.markdown('''
            - Total no. of news = {}
            - No. of positive news = {}
            - No. of negative news = {}
            - No. of neutral news = {}
            '''.format(total_news,postive_news,negative_news,neutral_news))
        if avg_sentiment > 0 or avg_sentiment == 0:
            st.markdown('''
                - <p style="color:green"> Average sentiment score = {:.3f}</p>
                '''.format(avg_sentiment), unsafe_allow_html=True)
        else:
                st.markdown('''
                - <p style="color:red">Average sentiment score =  {:.3f}</p>
                '''.format(avg_sentiment), unsafe_allow_html=True)

    else:
        st.info('Sorry unnable to find news about {}'.format(company))