from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

get_date = "2007-12-01"
df = get_most_recent_series_of_date("HOUST", get_date, fred)
df = df[df.index<=pd.to_datetime("2007-06-01")]

pct_chg_housing_units_started = transform_series(df, 4)

import numpy as np
import pymc3 as pm
import arviz as az

# Fit Bayesian ARMA(1,1) with PyMC3
with pm.Model() as arma_model:
    # Priors
    phi = pm.Normal("phi", mu=0, sigma=0.5)  # AR(1)
    theta = pm.Normal("theta", mu=0, sigma=0.5)  # MA(1)
    sigma = pm.InverseGamma("sigma", alpha=2, beta=1)  # Noise
    
    # Likelihood
    likelihood = pm.AR(
        "y", 
        ar=[1, -phi],  # Lag polynomial: 1 - phi*L
        ma=[1, theta], # Lag polynomial: 1 + theta*L
        sigma=sigma,
        observed=df
    )
    
    # Sample
    trace = pm.sample(2000, tune=1000, chains=4)

# Summary
az.summary(trace, var_names=["phi", "theta", "sigma"])

# Plot posteriors
az.plot_posterior(trace, var_names=["phi", "theta"])

# Forecast next step
with arma_model:
    pm.sample_posterior_predictive(trace, extend_inferencedata=True)
    forecasts = az.extract(trace.posterior_predictive)["y"].values
    print(np.percentile(forecasts[:, -1], [2.5, 97.5]))  # 95% PI