import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import option_functions as op
import seaborn as sns
import pandas as pd

st.set_page_config(
    page_title="Delta Hedging",
    page_icon="📈",
    layout="wide"
)


st.title("Delta Hedging")


col1, col2, col3, col4 = st.columns(4)

with col1:
    option_type = st.selectbox("Select Option Type", ["call", "put"])
with col2:
    spot = st.number_input("Spot Price", value=100.0, step=1.0)
with col3:
    strike = st.number_input("Strike Price", value=100.0, step=1.0)
with col4:
    expiry = st.number_input("Expiry (in years)", format="%.3f", value=1.000, step=0.001)

# Seconda riga di colonne
col5, col6, col7, col8 = st.columns(4)

with col5:
    time = st.number_input("Evaluate at Time (in years)", format="%.3f", value=0.000, step=0.001)
with col6:
    vol = st.number_input("Volatility (in %)", value=20.0, step=0.1)
with col7:
    rate = st.number_input("Risk-Free Rate (in %)", value=5.0, step=0.1)
with col8:
    num_options = st.number_input("Number of Options", value=1, step=1)


if "hedge_strategy" not in st.session_state:
    st.session_state.hedge_strategy = None

if "pnl" not in st.session_state:
    st.session_state.pnl = None

if "total_pnl_matrix" not in st.session_state: 
    st.session_state.total_pnl_matrix = None 
    
if "option_pnl_matrix" not in st.session_state: 
    st.session_state.option_pnl_matrix = None 

col1, col2 = st.columns(2)


option = op.option(strike=strike, expiry=expiry, type=option_type)

with col1:
    if time >= expiry:
        st.write("ERROR! Time must precede the expiration date")
        
    if st.button("Calculate Hedge Strategy"):
        st.session_state.hedge_strategy = option.delta_hedging(spot, time, vol, rate, num_options)
    
with col1:
     if st.session_state.hedge_strategy is not None:
        st.markdown(f"<div style='color: #16db16; font-size: 18px; font-weight: bold;text-align: left; margin-bottom: 10px;'> {st.session_state.hedge_strategy}</div>", unsafe_allow_html=True)

with col2:
    with st.expander("Delta Hedging Explained"):
        st.write("""
        Delta hedging is a strategy used in options trading to reduce or eliminate the risk associated with price movements
        in the underlying asset. The 'delta' of an option represents the sensitivity of the option's price to changes in the
        price of the underlying asset. By adjusting the position in the underlying asset to offset the delta of the option,
        a trader can create a 'delta-neutral' portfolio, meaning that small movements in the asset's price will not affect
        the overall value of the portfolio. This technique is often used to manage risk in options trading, allowing traders
        to maintain a stable position regardless of market fluctuations.
        """)


st.subheader("Profit and Losses Calculation")
st.info("""
    In this section, you can evaluate the profit and loss (PnL) of your portfolio that was constructed using the delta hedging strategy.
    By inputting a new spot price for the underlying asset, adjusting the time to a future evaluation period, and altering the
    volatility, you can see how these changes impact the value of your portfolio. The results will help you understand how your
    delta-hedged portfolio performs under different market conditions before the option expires.
    
    The heatmap feature allows you to visualize the potential outcomes of your portfolio's value over a range of spot prices and
    volatility levels. Each point on the heatmap represents the PnL for a specific combination of spot price and volatility, helping
    you to quickly identify areas of higher or lower profitability under varying market scenarios.    
    """)

current_spot = st.number_input("New Spot Price", value=100.0, step=1.0)
current_time = st.number_input("New evaluation at Time (in years)", format="%.3f", value=0.083, step=0.001)
current_vol = st.number_input("New Volatility (in %)", value=20.0, step=0.1)

if st.button("Calculate PnL"):
    if time >= expiry:
        st.write("ERROR! Time must precede the expiration date")
    if current_time>= expiry:
        st.write("ERROR! The new time selected must precede the expiration date")
        
    total_pnl, option_pnl, hedge_pnl = option.calculate_pnl(spot, time, vol, rate, num_options, current_spot, current_time, current_vol)
    profit_data = {
            "Total profit": [f"${total_pnl:.2f}"],
            "Earnings on option position": [f"${option_pnl:.2f}"],
            "Earnings on underlying position": [f"${hedge_pnl:.2f}"]
        }
    st.session_state.pnl = pd.DataFrame(profit_data)

if st.session_state.pnl is not None:
    st.table(st.session_state.pnl.style.set_properties(**{
            'background-color': '#B6C7B6',
            'color': 'black',
            'border-color': 'black'
        }))
        



with st.sidebar:
    
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=float(spot*0.8), step=2.0)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=float(spot*1.2), step=2.0)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=1.0, max_value=100.0, value=float(vol*0.5), step=1.0)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=1.0, max_value=100.0, value=float(vol*1.2), step=1.0)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    calculate_btn = st.button('Generate Heatmap')

col1, col2 = st.columns(2)

if calculate_btn:
  
    total_pnl_matrix = np.zeros((len(vol_range), len(spot_range)))
    option_pnl_matrix = np.zeros((len(vol_range), len(spot_range)))

    # Calculate PnL values for each spot and volatility combination
    for i, current_vol in enumerate(vol_range):
        for j, current_spot in enumerate(spot_range):
            total_pnl, option_pnl, _ = option.calculate_pnl(spot, time, vol, rate, num_options, current_spot, current_time, current_vol)
            total_pnl_matrix[i, j] = total_pnl
            option_pnl_matrix[i, j] = option_pnl

    st.session_state.total_pnl_matrix = total_pnl_matrix
    st.session_state.option_pnl_matrix = option_pnl_matrix


if st.session_state.total_pnl_matrix is not None and st.session_state.option_pnl_matrix is not None:
    with col1:
        st.subheader('With Hedge Strategy')
        fig, ax = plt.subplots(figsize=(12,8))
        sns.heatmap(st.session_state.total_pnl_matrix, annot=True, fmt=".2f", xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), ax=ax, cmap="RdYlGn", center=0)
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        ax.set_title('Total PnL')
        st.pyplot(fig)

    
    with col2:
        st.subheader('Without Hedge Strategy')
        fig, ax = plt.subplots(figsize=(12,8))
        sns.heatmap(st.session_state.option_pnl_matrix, annot=True, fmt=".2f", xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), ax=ax, cmap="RdYlGn", center=0)
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        ax.set_title('Option PnL')
        st.pyplot(fig)




 
