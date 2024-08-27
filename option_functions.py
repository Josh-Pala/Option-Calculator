""" 
Options calculator using the Black-Scholes method 
By Josh Pala 

""" 

from math import exp, log , sqrt, ceil 
from scipy.stats import norm 

HASNUMPY = 1
try:
    import numpy as np #checks if we have numpy
except ImportError:
    print("Plotting functions require Numpy")
    print("Plotting functions inoperable")
    HASNUMPY = 0

HASMATPLOTLIB = 1 #checks if we have matplotlib 
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Plotting functions require Matplotlib")
    print("Plotting functions inoperable")
    HASMATPLOTLIB = 0
    
"""    
Parameters
        ----------
        spot: float
            The spot price of the underlying.
        time: float
            The time when the call price is to be evaluated.
        strike: float
            The strike price of the call.
        expiry: float
            The expiration date of the call.
        vol: float
            The implied volatility to use to price the call (as a percentage).
        rate: float
            The risk free interest rate to use in the model (as a percentage).
            
    BSCall : Returns the call price evaluated using the Black-Scholes model 
    BSPut :  Returns the put price evaluated using the Black-Scholes model
"""
    
    
    
def BSCall(spot, time, strike, expiry, vol, rate):
    vol /= 100  #convert the volatility and interest rate from percentages to decimals 
    rate /= 100
    d1 = (log(spot/strike)+(rate+vol**2/2) * (expiry - time)) / vol / sqrt(expiry - time)
    d2 = (log(spot/strike)+(rate-vol**2/2) * (expiry - time)) / vol / sqrt(expiry - time)
    return spot*norm.cdf(d1)-strike * exp(-rate*(expiry - time))*norm.cdf(d2) 

"""
d₁ = [ln(S/K) + (r + σ²/2)(T - t)] / [σ√(T - t)]
d2 = [ln(S/K) + (r - σ²/2)(T - t)] / [σ√(T - t)]
Where:

ln is the natural logarithm
S is the spot price
K is the strike price
r is the risk-free interest rate
σ (sigma) is the volatility
T is the expiry time
t is the current time
√ is the square root symbol


The formula being implemented is:
C = S * N(d1) - K * e^(-r * t) * N(d2)

Where:
C is the call option price
S is the spot price
N() is the cumulative normal distribution function
K is the strike price
r is the risk-free rate
t is the time to expiration

"""

def BSPut(spot, time, strike, expiry, vol, rate): 
    vol /= 100 
    rate /= 100 
    d1 = (log(spot/strike)+(rate+vol**2/2) * (expiry - time)) / vol / sqrt(expiry - time) 
    d2 = (log(spot/strike)+(rate-vol**2/2) * (expiry - time)) / vol / sqrt(expiry - time)
    return -spot*norm.cdf(-d1)+strike*exp(-rate*(expiry - time))*norm.cdf(-d2)

"""
From the equation for put-call parity:
C + Ke^[-r(T-t)] = P + S
thus P = C - S + Ke^[-r(T-t)]
Where:

C is the price of the European call option
P is the price of the European put option

"""




"""
Options greeks
 
    The Greeks are a set of risk measures used in options pricing and risk management.
    They describe how the price of an option is expected to change with respect to
    various factors. The main Greeks are:

1. Delta (Δ): Measures the rate of change in the option price with respect to the
    change in the underlying asset's price.

2. Gamma (Γ): Measures the rate of change in Delta with respect to the change in
    the underlying asset's price.

3. Theta (Θ): Measures the rate of change in the option price with respect to
    the passage of time, also known as time decay.

4. Vega (ν): Measures the rate of change in the option price with respect to
    the change in the underlying asset's volatility.


 These Greeks are partial derivatives of the option pricing model (e.g., Black-Scholes)
 with respect to the underlying parameters. They are crucial for understanding and
 managing the risks associated with options positions.
 
 """

def BSCall_delta(spot, time, strike, expiry, vol, rate): 
    vol /=100 
    rate /=100 
    d1 = (log(spot/strike) + (rate + vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time) 
    return norm.cdf(d1) 

def BSPut_delta(spot, time, strike, expiry, vol, rate): 
    vol /=100 
    rate /=100
    d1 = (log(spot/strike) + (rate + vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    return -norm.cdf(-d1) 




def BSCall_gamma(spot, time, strike, expiry, vol, rate): 
    vol /=100
    rate /=100 
    d1 = (log(spot/strike) + (rate + vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    return norm.pdf(d1)/spot/vol/sqrt(expiry - time) 

def BSPut_gamma(spot, time, strike, expiry, vol, rate): 
    vol /=100
    rate /=100 
    d1 = (log(spot/strike) + (rate + vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    return norm.pdf(d1)/spot/vol/sqrt(expiry - time) 



def BSCall_vega(spot, time, strike, expiry, vol, rate): 
    vol /=100
    rate /=100 
    d1 = (log(spot/strike) + (rate + vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    return spot*sqrt(expiry - time)*norm.pdf(d1) / 100

def BSPut_vega(spot, time, strike, expiry, vol, rate): 
    vol /=100
    rate /=100 
    d1 = (log(spot/strike) + (rate + vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    return spot*sqrt(expiry - time)*norm.pdf(d1) / 100

# we divide vega by 100 because in our model, the input volatility (vol) is expressed as a percentage (e.g., 20%) rather than a decimal (e.g., 0.20). Additionally, the result is divided by 100 to scale Vega appropriately, as Vega is typically expressed per 1% change in volatility.


def BSCall_theta(spot, time, strike, expiry, vol, rate): 
    vol /=100
    rate /=100 
    d1 = (log(spot/strike) + (rate + vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    d2 = (log(spot/strike) + (rate - vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    theta = -(spot*norm.pdf(d1)*vol/2/sqrt(expiry - time)) - rate*strike*exp(-rate*(expiry - time))*norm.cdf(d2)
    return  theta/365 

def BSPut_theta(spot, time, strike, expiry, vol, rate): 
    vol /=100
    rate /=100 
    d1 = (log(spot/strike) + (rate + vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    d2 = (log(spot/strike) + (rate - vol**2/2)*(expiry - time)) / vol / sqrt(expiry - time)
    theta = -(spot*norm.pdf(d1)*vol/2/sqrt(expiry - time)) + rate*strike*exp(-rate*(expiry - time))*norm.cdf(-d2)
    return  theta/365 




class option: 
    def __init__(self, strike=0.0, expiry=0.0, type="call"):
        self.strike = strike
        self.expiry = expiry
        self.type = type
                
    def price(self, spot, time, vol, rate): 
        
        if time>=self.expiry:
            return "ERROR! Time must precede the expiration date"
        
        if self.type == "call": 
            return round(BSCall(spot, time, self.strike, self.expiry, vol, rate),2)
        else: 
            return round(BSPut(spot, time, self.strike, self.expiry, vol, rate),2)         
        
                  
    def delta(self, spot, time, vol, rate): 
        
        if time>=self.expiry:
            return "ERROR! Time must precede the expiration date" 
        
        if self.type == "call": 
            return BSCall_delta(spot, time, self.strike, self.expiry, vol, rate)
        else: 
            return BSPut_delta(spot, time, self.strike, self.expiry, vol, rate) 
                  
    def gamma(self, spot, time, vol, rate): 
        
        if time>=self.expiry:
            return "ERROR! Time must precede the expiration date" 
        
        if self.type == "call": 
            return BSCall_gamma(spot, time, self.strike, self.expiry, vol, rate)
        else: 
            return BSPut_gamma(spot, time, self.strike, self.expiry, vol, rate) 
                  
    def vega(self, spot, time, vol, rate): 
        
        if time>=self.expiry:
            return "ERROR! Time must precede the expiration date"
        
        if self.type == "call": 
            return BSCall_vega(spot, time, self.strike, self.expiry, vol, rate)
        else: 
            return BSPut_vega(spot, time, self.strike, self.expiry, vol, rate) 
                  
    def theta(self, spot, time, vol, rate): 
        
        if time>=self.expiry:
            return "ERROR! Time must precede the expiration date" 
        
        if self.type == "call": 
            return BSCall_theta(spot, time, self.strike, self.expiry, vol, rate)
        else: 
            return BSPut_theta(spot, time, self.strike, self.expiry, vol, rate) 
        
    def delta_hedging(self, spot, time, vol, rate, num_options):
        
        if time>=self.expiry:
            return "ERROR! Time must precede the expiration date"

        if self.type == "call":
            delta = BSCall_delta(spot, time, self.strike, self.expiry, vol, rate)
            action = "short"  # For call options, we need to short the stock
        else: 
            delta = BSPut_delta(spot, time, self.strike, self.expiry, vol, rate)
            action = "long"  # For put options, we need to long the stock
        
        hedge_position = ceil(abs(num_options * delta)) # math.ceil() rounds up to the nearest integer
        
        if action == "short":
            action_message = f"Take a short position in {hedge_position} shares"
        else:
            action_message = f"Take a long position in {hedge_position} shares"
            
        return action_message   
    """
    Delta Hedging Calculation: This function will calculate the number of shares to short or long to achieve a 
    delta-neutral portfolio based on the parameters provided.
    Note that for call options, the delta ranges between 0 and 1, while on put options, it ranges between -1 and 0. This is why in
    order to give a positive amount of shares to buy or to short I took the absolute value of the hedge position. 
    """
    def calculate_pnl(self, spot, time, vol, rate, num_options, current_spot, current_time, current_vol):
                #current time represents the new time after which you want to evaluate your position
        if time>=self.expiry:
            return "ERROR! Time must precede the expiration date"
            
        if current_time>=self.expiry:
            return "ERROR! The new time selected must precede the expiration date"
            
        if self.type == "call":
            initial_option_value = BSCall(spot, time, self.strike, self.expiry, vol, rate)           
            initial_delta = BSCall_delta(spot, time, self.strike, self.expiry, vol, rate)
        else:
            initial_option_value = BSPut(spot, time, self.strike, self.expiry, vol, rate)
            initial_delta = BSPut_delta(spot, time, self.strike, self.expiry, vol, rate)

        if self.type == "call":
            final_option_value = BSCall(current_spot, current_time, self.strike, self.expiry, current_vol, rate)
        else:
            final_option_value = BSPut(current_spot, current_time, self.strike, self.expiry, current_vol, rate)

        
        option_pnl = num_options * (final_option_value - initial_option_value)

        
        hedge_pnl = ceil(num_options * initial_delta) * (current_spot - spot)

        
        total_pnl = option_pnl - hedge_pnl

        return total_pnl, option_pnl, -hedge_pnl

  
    def plot_payoff(self, ax=None, color = "Purple"):
                         
        if not HASMATPLOTLIB:
            print("Plotting functions require Matplotlib")
            return None
        
        
        if ax is None:
            fig, ax = plt.subplots()
                  
        """
        fig, ax = ...: The function plt.subplots() returns two objects:

        fig (short for figure): This object represents the entire figure, which can contain multiple subplots, titles, labels, legends,
        etc. Think of it as the canvas on which all your plots are drawn.

        ax (short for axes): This object represents an individual plot or graph within the figure. The term "axes" here refers to the
        coordinate system of the plot, including the x and y axes.

        subplots(): This is a function from pyplot that creates a figure and a grid of subplots. If you don’t specify the number of
        rows and columns, it defaults to a single subplot (one plot).

        fig, axs = plt.subplots(2, 2)  # Creates a 2x2 grid of subplots

        """
        s = np.arange(0.0, 2*self.strike, 0.1)
        p = []

        """
        np.arange(0.0, 2*self.strike, 0.1): This function generates an array of spot prices starting from 0.0 up to 2 * self.strike in
        increments of 0.1

        p = []: Initializes an empty list p to store the calculated payoff values
        """
                  
        for spot in s:
            if self.type == "call":
                price = max(0, spot - self.strike)
            else:
                price = max(0, self.strike - spot)
            p.append(price)
        
                  
        payoff = np.array(p)
                  
        ax.plot(s, payoff, color=color, label="Payoff")

        ax.set(xlabel="spot", ylabel="payoff",
            title = "Option Payoff")
        
        return ax
                  
        """
        p.append(price): Adds the calculated payoff for each spot price to the list p

        np.array(p): Converts the list p into a Numpy array payoff

        ax.plot(s, payoff): Plots the payoff values against the spot prices. s is on the x-axis (spot prices), and payoff is on the 
        y-axis (payoff values).

        plt.show(block=False): Displays the plot in a window. The block=False argument makes the window non-blocking, meaning the rest
        of your code can continue running while the plot is displayed.
        """
                  
    def plot_price(self, time, vol, rate, ax=None, color="blue"):
                  
        if not HASMATPLOTLIB:
            print("Plotting require matplotlib") 
            return None 
                
        if time >= self.expiry:
            return "ERROR! Time must precede the expiration date"
        
        if ax is None:          
            fig, ax = plt.subplots() 
        
        s = np.arange(0.1, 2*self.strike, 0.1)
                  
        p = []
        
        for spot in s:                   
            if self.type == "call": 
                price = BSCall(spot, time, self.strike, self.expiry, vol, rate)
            else: 
                price = BSPut(spot, time, self.strike, self.expiry, vol, rate) 
            p.append(price)
                  
        prices = np.array(p) 
        
        ax.plot(s, prices, color=color, label = "Price")
        
        ax.set(xlabel="spot" , ylabel="price", title="Option Price") 
        return ax
    
    def plot_delta(self, time, vol, rate): 
        
        if not HASMATPLOTLIB:
            print("Plotting require matplotlib")
            return None 
        
        if time > self.expiry:
            print("Time must precede the expiration date")
            return None
        
        fig, ax = plt.subplots()
                  
        s = np.arange(0.1, 2*self.strike, 0.1)         
        d = []
        
        for spot in s:    
            if self.type == "call": 
                delta = BSCall_delta(spot, time, self.strike, self.expiry, vol, rate) 
            else: 
                delta = BSPut_delta(spot, time, self.strike, self.expiry, vol, rate)
            d.append(delta)
        
        deltas = np.array(d) 
        
        ax.plot(s, deltas) 
        ax.set(xlabel= "spot" , ylabel="delta", title="Option Greek Delta")
        
        plt.show(block=False) 
        
    def plot_gamma(self, time, vol, rate): 
        
        if not HASMATPLOTLIB: 
            print("Plotting require matplotlib") 
            return None 
        if time > self.expiry: 
            print("Time must precede the expiration date") 
            return None 
        
        fig, ax = plt.subplots()
        
        s = np.arange(0.1, 2*self.strike, 0.1) 
        g = []
        
        for spot in s: 
            if self.type == "call": 
                gamma = BSCall_gamma(spot, time, self.strike, self.expiry, vol, rate)
            else: 
                gamma = BSPut_gamma(spot, time, self.strike, self.expiry, vol, rate) 
            g.append(gamma)
            
        gammas = np.array(g) 
        
        ax.plot(s, gammas) 
        ax.set(xlabel="spot", ylabel="gamma", title="Option Greek Gamma") 
        
        plt.show(block=False) 
        
    def plot_vega(self, time, vol, rate): 
        
        if not HASMATPLOTLIB: 
            print("Plotting require matplotlib") 
            return None 
        if time > self.expiry: 
            print("Time must precede the expiration date") 
            return None 
        
        fig, ax = plt.subplots()
        
        s = np.arange(0.1, 2*self.strike, 0.1) 
        v = []
        
        for spot in s: 
            if self.type == "call": 
                vega = BSCall_vega(spot, time, self.strike, self.expiry, vol, rate)
            else: 
                vega = BSPut_vega(spot, time, self.strike, self.expiry, vol, rate) 
            v.append(vega)
            
        vegas = np.array(v) 
        
        ax.plot(s, vegas) 
        ax.set(xlabel="spot", ylabel="vega", title="Option Greek Vega") 
        
        plt.show(block=False) 
        
    def plot_theta(self, time, vol, rate): 
        
        if not HASMATPLOTLIB: 
            print("Plotting require matplotlib") 
            return None 
        if time > self.expiry: 
            print("Time must precede the expiration date") 
            return None 
        
        fig, ax = plt.subplots()
        
        s = np.arange(0.1, 2*self.strike, 0.1) 
        t = []
        
        for spot in s: 
            if self.type == "call": 
                theta = BSCall_theta(spot, time, self.strike, self.expiry, vol, rate)
            else: 
                theta = BSPut_theta(spot, time, self.strike, self.expiry, vol, rate) 
            t.append(theta)
            
        thetas = np.array(t) 
        
        ax.plot(s, thetas) 
        ax.set(xlabel="spot", ylabel="theta", title="Option Greek Theta") 
        
        plt.show(block=False) 
        
                  
 

    
    
    
    
    
    
    
    
    
    
    
