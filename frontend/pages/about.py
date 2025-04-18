import dash
from dash import html, dcc, Input, Output
from shared.default_pagelayout import get_default_layout 
import dash_bootstrap_components as dbc
from assets.meettheteam import create_team_layout, team_members

dash.register_page(__name__, path="/about", name="About")

about_content = html.Div(
    id="main-content",
    style={
       'height': '100vh',
       'overflowY': 'scroll',
       'paddingTop': "50px",   # Leave space on top for nav bar 
       'paddingBottom': '200px' # bottom padding
   },
    children=[
        # Header text container
        html.Div(
            children=[
                html.H1(
                    "Our Goal",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "32px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                )
            ],
            style={"textAlign": "center"}
        ),
        html.Br(),
        html.P("""
            Currently, economists and policymakers are facing challenges in receiving up-to-date information about Gross Domestic Product (GDP). 
            As data on GDP is only available quarterly, there is a lag in which the GDP estimate of the quarter will be available. This lag, often up to 4 months, creates substantial challenges for timely decision making. 
            Thus, 6se3nse is our one-stop solution for staying ahead of the economy. 6se3nse provides economists and policymakers with more timely estimates of quarterly GDP growth through monthly updated nowcast. 
            For example, in early November, economists can access a nowcast for Quarter 4 (Q4), 
            instead of waiting till late January for the official Q4 GDP release. In addition, users can stay abreast of the latest economic news from top financial sources and explore latest 
            economic data so users can focus on work that truly matters. 6se3nse leverages a Python and Flask framework backend with the Dash framework for its front-end interactive components.
            """, style={"color": "lightgrey", "fontSize": "18px", "fontFamily": "Montserrat, sans-serif", 
                        "marginLeft": "10%", "marginRight": "10%", "textAlign": "justify"}
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            children=[
                html.H1(
                    "Our Methodology",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "32px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                )
            ],
            style={"textAlign": "center"}
        ),
        html.Br(),
        html.P("""
            6se3nse uses FRED-MD monthly and FRED-QD quarterly data (https://www.stlouisfed.org/research/economists/mccracken/fred-databases). Logarithmic differences were mainly used for data transformation, supplemented by publicly available transformation code from GitHub (https://fg-research.com/blog/general/posts/fred-md-overview.html). To provide a structured framework for GDP analysis, we employ the standard GDP expenditure approach which decomposes GDP into its core components: Consumption Spending (C), Investments (I), Government Expenditure (G), and Net Exports (X-M). Other economic indicators such as Sahm’s Rule will also be employed. For our models we mainly explored an ARMA-Bridge model, a U-MIDAS model, an RF model, using Elastic Net (EN) for both the ARMA-bridge and U-MIDAS model as well as Prophet.

            """, 
            style={"color": "lightgrey", "fontSize": "18px", "fontFamily": "Montserrat, sans-serif",
                        "marginLeft": "10%", "marginRight": "10%", "textAlign": "justify"}
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            children=[
                html.H1(
                    "Meet the team",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "32px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                )
            ],
            style={"textAlign": "center"}
        ),
        html.Div(
            children=[
                create_team_layout(team_members)
            ]
        )
        

        
    ]
)

layout = get_default_layout(main_content=about_content)
