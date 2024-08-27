import streamlit as st 
import option_functions as op 
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CheckboxGroup, Span, Label, HoverTool, CustomJS
from bokeh.layouts import column
from bokeh.palettes import Spectral11

st.set_page_config(
    page_title="Option Price",
    page_icon="📊",
)



st.title("Black-Scholes Pricing Model")



col1, col2, col3, col4 = st.columns(4)

with col1:
    option_type = st.selectbox("Select Option Type", ["call", "put"])
with col2:
    spot = st.number_input("Spot Price", value=100.0, step=1.0)
with col3:
    strike = st.number_input("Strike Price", value=100.0, step=1.0)
with col4:
    expiry = st.number_input("Expiry (in years)",format="%.3f", value=1.000, step=0.001)


col5, col6, col7, col8 = st.columns(4)

with col5:
    time = st.number_input("Evaluate at Time (in years)",format="%.3f", value=0.000, step=0.001)
with col6:
    vol = st.number_input("Volatility (in %)", value=20.0, step=0.1)
with col7:
    rate = st.number_input("Risk-Free Interest Rate (in %)", value=5.0, step=0.1)
with col8:
    num_options = st.number_input("Number of Options", value=1, step=1)

input_data = {
    "Option Type": [option_type],
    "Current Asset Price": [spot],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [expiry],
    "Evaluate at Time (Years)" : [time],
    "Volatility (σ)": [vol],
    "Risk-Free Interest Rate": [rate]
    }
input_df = pd.DataFrame(input_data)
st.subheader("Input Summary")
st.table(input_df.style.set_properties(**{
        'background-color': '#B6C7B6',
        'color': 'black',
        'border-color': 'black'
    }))

if "price" not in st.session_state:
    st.session_state.price = None

if "greeks" not in st.session_state:
    st.session_state.greeks_df = None

col1, col2 = st.columns([1,1], gap="large")

with col1:
    if time >= expiry:
        st.write("ERROR! Time must precede the expiration date")
        
    if st.button("Calculate Option Price"):
        # Creazione dell'oggetto opzione
        option = op.option(strike=strike, expiry=expiry, type=option_type)
        st.session_state.price = option.price(spot, time, vol, rate)
        
       
with col2:
    if time >= expiry:
        st.write("ERROR! Time must precede the expiration date")
        
    if st.button("Calculate Option Greeks"):
        # Creazione dell'oggetto opzione
        option = op.option(strike=strike, expiry=expiry, type=option_type)
        
        delta = option.delta(spot, time, vol, rate)
        gamma = option.gamma(spot, time, vol, rate)
        vega = option.vega(spot, time, vol, rate)
        theta = option.theta(spot, time, vol, rate)

        
        results_data = {
            "Delta": [delta],
            "Gamma": [gamma],
            "Vega": [vega],
            "Theta": [theta]
        }
        
        st.session_state.greeks_df = pd.DataFrame(results_data)
        
        


with col1:
    if st.session_state.price is not None:
        st.markdown(f"<div style='color: #16db16; font-size: 18px; font-weight: bold;text-align: center; margin-bottom: 10px;'>Price : ${st.session_state.price}</div>", unsafe_allow_html=True)
        with st.expander("Black-Scholes Model Explained"):
                st.write(r'''
                        The Black-Scholes model, developed by economists Fischer Black, Myron Scholes, and Robert Merton in 1973,
                        is a landmark in the field of financial mathematics. This model revolutionized the pricing of options by
                        providing a theoretical framework for determining the fair value of European-style options. The model is
                        grounded in the concept of a "no-arbitrage" market, where it's impossible to make a risk-free profit, and is
                        derived from the application of stochastic calculus to model the dynamics of asset prices.
                        
                        At its core, the Black-Scholes model assumes that the price of the underlying asset follows a geometric
                        Brownian motion, which implies that the asset's price changes are continuous and can be described by a normal
                        distribution with constant drift and volatility. This led to the development of a partial differential equation
                        that, when solved, provides the formula for pricing options.
                            
                        The Black-Scholes formula for the price of a European call option is:
                    
                        $$
                        C = S \cdot N(d_1) - K \cdot e^{-r \cdot (T - t)} \cdot N(d_2)
                        $$
                    
                        Where:
                        - $ C $ is the call option price.
                        - $ S $ is the spot price of the underlying asset.
                        - $ K $ is the strike price of the option.
                        - $ r $ is the risk-free interest rate.
                        - $ T - t $ is the time to expiration.
                        - $ N(d) $ is the cumulative normal distribution function.
                        - $ d_1 $ and $ d_2 $ are calculated as:
                    
                        $$
                        d_1 = \frac{\ln\left(\frac{S}{K}\right) + \left(r + \frac{\sigma^2}{2}\right)(T - t)}{\sigma \sqrt{T - t}}
                        $$
                    
                        $$
                        d_2 = \frac{\ln\left(\frac{S}{K}\right) + \left(r - \frac{\sigma^2}{2}\right)(T - t)}{\sigma \sqrt{T - t}}
                        $$
                    
                        - $ \sigma $ (sigma) is the volatility of the asset.
                        - $ \ln $ represents the natural logarithm.
                    
                        In summary, the Black-Scholes model helps to determine the fair value of an option by considering factors like
                        the underlying asset's price, the strike price, time to expiration, risk-free rate, and volatility.
                        ''')
            
with col2:
    if st.session_state.greeks_df is not None:
        st.table(st.session_state.greeks_df.style.set_properties(**{
            'background-color': '#B6C7B6',
            'color': 'black',
            'border-color': 'black'
        }))
        with st.expander("Greeks Expalined"):
            st.write('''
                Options greeks:
         
                    The Greeks are a set of risk measures used in options pricing and risk management.
                    They describe how the price of an option is expected to change with respect to
                    various factors. The main Greeks are:
                
                1. Delta (Δ): Measures the rate of change in the option price with respect to the
                    change in the underlying asset's price.
                
                2. Gamma (Γ): Measures the rate of change in Delta with respect to the change in
                    the underlying asset's price.
                
                3. Theta (Θ): Measures the rate of change in the option price with respect to
                    the passage of time, also known as time decay. In our model, Theta is divided
                    by 365 to convert the annualized Theta into a daily rate, reflecting how much the
                    option's price is expected to decay each day.
                
                4. Vega (ν): Measures the rate of change in the option price with respect to
                    the change in the underlying asset's volatility.
                
                
                 These Greeks are partial derivatives of the option pricing model (e.g., Black-Scholes)
                 with respect to the underlying parameters. They are crucial for understanding and
                 managing the risks associated with options positions.
            ''')
            
@st.cache_data
def plot_payoff_and_price(spot, strike, expiry, vol, rate, option_type):
    if time >= expiry:
        return "Time must precede the expiration date"
    s = np.arange(0.0, 2*strike, 0.1)
    p = [max(0, spot - strike) if option_type == "call" else max(0, strike - spot) for spot in s]
    payoff = np.array(p)

    s_price = np.arange(0.1, 2*strike, 0.1)
    p_price = [op.BSCall(spot, time, strike, expiry, vol, rate) if option_type == "call" else op.BSPut(spot, time, strike, expiry, vol, rate) for spot in s_price]
    prices = np.array(p_price)
        
    return s, payoff, s_price, prices

s, payoff, s_price, prices = plot_payoff_and_price(spot=spot, strike=strike, expiry=expiry, vol=vol, rate=rate, option_type=option_type)


source_payoff = ColumnDataSource(data=dict(x=s, y=payoff))
source_prices = ColumnDataSource(data=dict(x=s_price, y=prices))


plot = figure(width=800, height=400, title="Option Pricing and Payoff", tools="pan,wheel_zoom,box_zoom,reset")

line_payoff = plot.line('x', 'y', source=source_payoff, color="blue", legend_label="Payoff", line_width=2)
line_prices = plot.line('x', 'y', source=source_prices, color="red", legend_label="Option Price", line_width=2)


strike_line = Span(location=strike, dimension='height', line_color='green', line_dash='dotted', line_width=2)
spot_line = Span(location=spot, dimension='height', line_color='orange', line_dash='dotted', line_width=2)

plot.add_layout(strike_line)
plot.add_layout(spot_line)




hover_tool = HoverTool(
    tooltips=[("Price Level", "@y{0.00}"), ("Spot Price", "@x{0.00}")],
    renderers=[line_prices],
    mode='vline'
)

plot.add_tools(hover_tool)

plot.xaxis.axis_label = "Spot"
plot.yaxis.axis_label = "Value ($)"

plot.margin = (20, 20, 20, 20) #top, right, bottom, left


layout = column(plot)

st.bokeh_chart(layout, use_container_width=True)

@st.cache_data
def plot_greeks(spot, strike, expiry, vol, rate, option_type):
    if time >= expiry:
        return "Time must precede the expiration date"
        
    s = np.arange(0.1, 2 * strike, 0.1)
    deltas = np.array([op.BSCall_delta(spot, time, strike, expiry, vol, rate) if option_type == "call" else op.BSPut_delta(spot, time, strike, expiry, vol, rate) for spot in s])
    gammas = np.array([op.BSCall_gamma(spot, time, strike, expiry, vol, rate) if option_type == "call" else op.BSPut_gamma(spot, time, strike, expiry, vol, rate) for spot in s])
    vegas = np.array([op.BSCall_vega(spot, time, strike, expiry, vol, rate) if option_type == "call" else op.BSPut_vega(spot, time, strike, expiry, vol, rate) for spot in s])
    thetas = np.array([op.BSCall_theta(spot, time, strike, expiry, vol, rate) if option_type == "call" else op.BSPut_theta(spot, time, strike, expiry, vol, rate) for spot in s])
    return s, deltas, gammas, vegas, thetas

s, deltas, gammas, vegas, thetas = plot_greeks(spot=spot, strike=strike, expiry=expiry, vol=vol, rate=rate, option_type=option_type)


source_deltas = ColumnDataSource(data=dict(x=s, y=deltas))
source_gammas = ColumnDataSource(data=dict(x=s, y=gammas))
source_vegas = ColumnDataSource(data=dict(x=s, y=vegas))
source_thetas = ColumnDataSource(data=dict(x=s, y=thetas))

plot = figure(width=800, height=400, title="Option Greeks", tools="pan,wheel_zoom,box_zoom,reset")

line_deltas = plot.line('x', 'y', source=source_deltas, color="blue", legend_label="Delta", line_width=2)
line_gammas = plot.line('x', 'y', source=source_gammas, color="green", legend_label="Gamma", line_width=2)
line_vegas = plot.line('x', 'y', source=source_vegas, color="orange", legend_label="Vega", line_width=2)
line_thetas = plot.line('x', 'y', source=source_thetas, color="red", legend_label="Theta", line_width=2)


strike_line = Span(location=strike, dimension='height', line_color='green', line_dash='dotted', line_width=2)
spot_line = Span(location=spot, dimension='height', line_color='orange', line_dash='dotted', line_width=2)

plot.add_layout(strike_line)
plot.add_layout(spot_line)

hover_tool1 = HoverTool(
    tooltips=[("Value", "@y{0.0000}"), ("Spot Price", "@x{0.00}")],
    renderers=[line_deltas, line_gammas, line_vegas, line_thetas],
    mode='vline'
)

plot.add_tools(hover_tool1)

checkbox = CheckboxGroup(labels=["Delta", "Gamma", "Vega", "Theta"], active=[0, 1, 2, 3])


callback = CustomJS(args=dict(deltas=line_deltas, gammas=line_gammas, vegas=line_vegas, thetas=line_thetas, checkbox=checkbox),
                    code="""
                    deltas.visible = checkbox.active.includes(0);
                    gammas.visible = checkbox.active.includes(1);
                    vegas.visible = checkbox.active.includes(2);
                    thetas.visible = checkbox.active.includes(3);
                    """
                   )

checkbox.js_on_change('active', callback)


plot.xaxis.axis_label = "Spot"
plot.yaxis.axis_label = "Value"

plot.margin = (20, 20, 20, 20)

layout = column(checkbox, plot)


st.bokeh_chart(layout, use_container_width=True)    



