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
            Economists and policymakers worldwide have faced challenges in providing timely and
            precise economic forecasts. However, the biggest issue lies in the delayed publishing of
            credible economic data. The growth of real GDP, widely used as a barometer for the health
            of the economy, is commonly published quarterly. In addition to the infrequent publishings,
            these numbers are often subject to subsequent revisions. The absence of timely updates on
            these economic indicators can have dire consequences: For example, throughout much of
            2021, the Federal Reserve downplayed concerns of rising inflation, characterising the rising
            prices as “transitory” despite clear signs of persistent inflation. As a result, inflation in the
            U.S. has worsened financial conditions for 65% of Americans in 2023, according to a report
            by CNN Business. As such, recent developments in Nowcasting, which leverage higher
            frequency and more timely released data available to predict the state of the economy, have
            the potential to bridge this gap.
            The main objective of this project is to explore nowcasting techniques to provide various
            economic agents in the United States economy – such as government, financial institutions,
            and households – with accurate and timely predictions of various economic indicators,
            enabling them to make faster and more informed decisions. Users will be able to access
            these insights through a user-friendly website. Other objectives include developing a robust
            data ecosystem that includes the extraction and processing of timely data into nowcasting
            models and linking of backend models to frontend user-friendly interface for accessibility.
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
            Our model would adopt a bridge model similar to that of the Atlanta FRED model. It would use a similar methodology of Consumption(C), Investment(I), Government(G), Nett Exports(X-M).
            We aim to predict the GDP for the current quarter as well as as past quarter that has not been released.
            We assume that data follows a 1 month lag. For example, all monthly and quarterly data would only have an initial prediction 1 month in advance.
            We aim to do 2 things, predict GDP in current quarter and past quarters. For example, in the start of M3 2024, we would want to predict Q1 2024 GDP for that quarter. However, in the start of M1 2024, we would want Q4 2023 GDP as this data is not released due to the lag in data release. For start of M1 of new quarter or end of M3 for previous quarter we want to predict the previous quarter GDP. For start of M2 or end of M1 we would know the past quarter GDP and would want to predict GDP for that whole quarter. Same for start of M3 and end of M2.
            In order to do this quarterly prediction we intend to use a quarterly bridge model which splits quarterly GDP into its various components C, I, G, X-M. For each of these components, we intend to create a bridge model and use iterative predictions to get the quarterly value
            Currently from the fred data, we have these for each component "DGDSRC1": "Consumption Expenditure Goods", Monthly "PCESC96": "Consumption Expenditure Services", Monthly "EXPGSC1": "Goods & Services Exports", Quarterly "IMPGSC1": "Goods & Services Imports", Quarterly "PNFIC1": "Real Private Nonresidential Fixed Investment", Quarterly "PRFIC1": "Real Private Residential Fixed Investment", Quarterly "GCEC1": "Real Government Consumption Expenditures and Gross Investment", Quarterly "SLEXPND": "State and Local Government Current Expenditures", Quarterly
            Dependent variable "GDP": "Gross Domestic Product", Quarterly
            Current Problems Most of these data is quarterly, not high frequency enough should consider high frequency proxies instead
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
