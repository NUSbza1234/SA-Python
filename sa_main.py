import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import pandas_ta as ta

# Utility function
def load_data(stock, period):
    df = yf.Ticker(stock).history(period=period)[['Open', 'High', 'Low', 'Close', 'Volume']]
    df = df.reset_index()
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df['time'] = pd.to_datetime(df['time'])  # Ensure the 'time' column is datetime type
    df['time'] = df['time'].dt.strftime('%Y-%m-%d')  # Date to string

    # Calculate technical indicators
    df['EMA_20'] = ta.ema(df['close'], length=20)
    df['EMA_200'] = ta.ema(df['close'], length=200)
    df['RSI_14'] = ta.rsi(df['close'], length=14)
    
    # Calculate ADX and ensure it's not None
    adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
    if adx_df is not None and 'ADX_14' in adx_df and 'DMP_14' in adx_df and 'DMN_14' in adx_df:
        df['ADX_14'] = adx_df['ADX_14']
        df['DMP_14'] = adx_df['DMP_14']
        df['DMN_14'] = adx_df['DMN_14']
    else:
        df['ADX_14'] = pd.NA
        df['DMP_14'] = pd.NA
        df['DMN_14'] = pd.NA

    df['ATR_14'] = ta.atr(df['high'], df['low'], df['close'], length=14)

    return df

# Function to get emoji based on returns value
def get_returns_emoji(ret_val):
    return ":white_check_mark:" if ret_val >= 0 else ":red_circle:"

# Function to get emoji based on ema value
def get_ema_emoji(ltp, ema):
    return ":white_check_mark:" if ltp >= ema else ":red_circle:"

# Function to get emoji based on rsi value
def get_rsi_emoji(rsi):
    return ":white_check_mark:" if 30 < rsi < 70 else ":red_circle:"

# Function to get emoji based on adx value
def get_adx_emoji(adx):
    return ":white_check_mark:" if adx > 25 else ":red_circle:"

# Function to create chart
def create_chart(df):
    candlestick_chart = go.Figure(data=[go.Candlestick(x=df['time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
    ema20 = go.Scatter(x=df['time'], y=df['EMA_20'], name='EMA20')
    ema200 = go.Scatter(x=df['time'], y=df['EMA_200'], name='EMA200')
    candlestick_chart.add_trace(ema20)
    candlestick_chart.add_trace(ema200)
    candlestick_chart.update_layout(title=f'{stock} Historical Candlestick Chart', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=True)
    return candlestick_chart

# #########End of function #######

# Title of the application
#st.subheader(":rainbow[Tech Nuggets's  Stock :green[Technical] :red[Analysis] Dashboard!]")
st.subheader("Stock :red[Technical] :red[Analysis] Dashboard")


overview_markdown = """
### An overview of this Technical Analysis Dashboard...

- Input the stock ticker into the field on the left.
- We have 3 columns of analytical data: Returns, Momentum, and the trend strength of the stock.
- Select a timeframe that you would like to view, check show data and chart.
- The following financial indicators were used as they were some of the more basic ones.
- "RSI - Relative Strength Index"
- "EMA20/EMA200 - Exponential Moving Average (20/200 periods)"
- "LTP - Last Trading Price"
- "In trading, ADX, DMP, and DMN are components of the Average Directional Index (ADX) system"
- "ADX - Average Directional Index (Measures the strength of a trend)"
- "DMP - Directional Movement Plus (Indicates the strength of the upward movement)"
- "DMN - Directional Movement Minus (Indicates the strength of the downward movement)"
- "Make Trading Decisions: Enter trades in the direction of the trend when the ADX indicates a strong trend, and use the DMP and DMN lines to confirm the direction."

"""

st.markdown(overview_markdown)


# Sidebar Components
stock = st.sidebar.text_input("Stock Symbol e.g. AAPL", "AAPL")
timeframe_option = st.sidebar.selectbox("Timeframe?", ('1y', '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'))
show_data = st.sidebar.checkbox(label="Show Data")
show_chart = st.sidebar.checkbox(label="Show Chart")

# Load data
df = load_data(stock, timeframe_option)

# Check if DataFrame is empty or has no data
if df.empty or len(df) == 0:
    st.error("No data available for the selected stock and timeframe.")
else:
    # Reverse DataFrame for easy access to the latest data
    reversed_df = df.iloc[::-1]

    # Check if DataFrame has at least one row
    if len(reversed_df) > 0:
        # Extract latest values
        row1_val = reversed_df.iloc[0]['close']
        ema20_val = reversed_df.iloc[0]['EMA_20'] if not pd.isna(reversed_df.iloc[0]['EMA_20']) else None
        ema200_val = reversed_df.iloc[0]['EMA_200'] if not pd.isna(reversed_df.iloc[0]['EMA_200']) else None
        rsi_val = reversed_df.iloc[0]['RSI_14'] if not pd.isna(reversed_df.iloc[0]['RSI_14']) else None
        adx_val = reversed_df.iloc[0]['ADX_14'] if not pd.isna(reversed_df.iloc[0]['ADX_14']) else None
        dmp_val = reversed_df.iloc[0]['DMP_14'] if not pd.isna(reversed_df.iloc[0]['DMP_14']) else None
        dmn_val = reversed_df.iloc[0]['DMN_14'] if not pd.isna(reversed_df.iloc[0]['DMN_14']) else None
    else:
        row1_val = None
        ema20_val = None
        ema200_val = None
        rsi_val = None
        adx_val = None
        dmp_val = None
        dmn_val = None

    # Check if DataFrame has enough rows for the calculations
    if len(reversed_df) >= 241:
        row20_val = reversed_df.iloc[20]['close']  # 1 month return
        row60_val = reversed_df.iloc[60]['close']  # 3 months return
        row120_val = reversed_df.iloc[120]['close']  # 6 months return
        row240_val = reversed_df.iloc[240]['close']  # 12 months return

        # Return Percentage Calculation
        day20_ret_percent = (row1_val - row20_val) / row20_val * 100
        day20_ret_val = row1_val - row20_val
        day60_ret_percent = (row1_val - row60_val) / row60_val * 100
        day60_ret_val = row1_val - row60_val
        day120_ret_percent = (row1_val - row120_val) / row120_val * 100
        day120_ret_val = row1_val - row120_val
        day240_ret_percent = (row1_val - row240_val) / row240_val * 100
        day240_ret_val = row1_val - row240_val
    else:
        st.error("Not enough data for return calculations.")

    # Column wise Display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Returns")
        if len(reversed_df) >= 241:
            st.markdown(f"- 1 MONTH : {round(day20_ret_percent, 2)}% {get_returns_emoji(round(day20_ret_percent, 2))}")
            st.markdown(f"- 3 MONTHS : {round(day60_ret_percent, 2)}% {get_returns_emoji(round(day60_ret_percent, 2))}")
            st.markdown(f"- 6 MONTHS : {round(day120_ret_percent, 2)}% {get_returns_emoji(round(day120_ret_percent, 2))}")
            st.markdown(f"- 12 MONTHS : {round(day240_ret_percent, 2)}% {get_returns_emoji(round(day240_ret_percent, 2))}")
        else:
            st.markdown("Not enough data for return calculations.")
    with col2:
        st.subheader("Momentum")
        if row1_val is not None:
            st.markdown(f"- LTP : {round(row1_val, 2)}")
        else:
            st.markdown("- LTP : N/A")
        if ema20_val is not None:
            st.markdown(f"- EMA20 : {round(ema20_val, 2)} {get_ema_emoji(row1_val, ema20_val)}")
        else:
            st.markdown("- EMA20 : N/A")
        if ema200_val is not None:
            st.markdown(f"- EMA200 : {round(ema200_val, 2)} {get_ema_emoji(row1_val, ema200_val)}")
        else:
            st.markdown("- EMA200 : N/A")
        if rsi_val is not None:
            st.markdown(f"- RSI : {round(rsi_val, 2)} {get_rsi_emoji(rsi_val)}")
        else:
            st.markdown("- RSI : N/A")
    with col3:
        st.subheader("Trend Strength")
        if adx_val is not None:
            st.markdown(f"- ADX : {round(adx_val, 2)} {get_adx_emoji(adx_val)}")
        else:
            st.markdown("- ADX : N/A")
        if dmp_val is not None:
            st.markdown(f"- DMP : {round(dmp_val, 2)}")
        else:
            st.markdown("- DMP : N/A")
        if dmn_val is not None:
            st.markdown(f"- DMN : {round(dmn_val, 2)}")
        else:
            st.markdown("- DMN : N/A")

    if show_data:
        st.write(reversed_df)

    if show_chart:
        st.plotly_chart(create_chart(df))



# This will be the main python script for this analysis app in python.
