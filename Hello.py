import streamlit as st

st.set_page_config(
    page_title="Options Calculator",
    page_icon="📟",
    layout="wide"
)



st.title("Welcome to the Options Calculator! 👋")

st.markdown("##### `Created by:`")
linkedin_url = "https://www.linkedin.com/in/josh-pala-62873a257/"
st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Josh Pala`</a>', unsafe_allow_html=True)


# Introduzione al progetto
st.markdown(
    """
    ## About the Project
    
    The **Options Calculator** is an interactive tool designed to help traders, financial analysts, and students to 
    better understand and calculate the price of options and their Greeks. This project leverages the Black-Scholes model
    to compute option prices and sensitivities, offering a robust platform for financial analysis.
    
    ### Key Features:
    
    - **Options Pricing**: Calculate the price of European call and put options.
    - **Greeks Calculation**: Explore key risk measures like Delta, Gamma, Theta, and Vega.
    - **Payoff Diagrams**: Visualize the payoff structure of options.
    - **Delta Hedging**: Implement and understand delta hedging strategies with visual aids like heatmaps.
    
    Whether you're a seasoned trader or just beginning your journey in options trading, this calculator offers a comprehensive set of tools to support your decision-making process.
    
    ### How to Navigate:
    
    - **Options Pricing & Greeks**: Calculate the price of options and explore their Greeks on the corresponding page.
    - **Delta Hedging**: Learn and implement delta hedging strategies with an intuitive heatmap.
    - **Visualization**: Dive into various plots that help in understanding the payoff, pricing, and risk measures.
    
    ---
    
    ### Why Use This Tool?
    
    - **Educational Purpose**: Learn how different factors influence option pricing and risk.
    - **Practical Application**: Use it as a tool to aid your trading decisions.
    
    ---
    
    **Ready to dive in?** Select a page from the sidebar to start exploring!
    """
)

# Link per saperne di più (opzionale)
st.markdown(
    """
    ### Want to learn more about options trading?
    
    - Check out [Investopedia's Options Guide](https://www.investopedia.com/options-basics-tutorial-4583012)
    """
)

# Footer o informazioni aggiuntive
st.markdown("© 2024 Options Calculator")

 
