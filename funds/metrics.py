



import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt




class Metrics():


    def sharpe_ratio(self, fund):
        # Assuming you have two pandas Series or DataFrames: prices and nav
        # Replace 'your_prices' and 'your_nav' with the actual column names from your data

        # Calculate daily returns from historical prices
        returns = fund.history["pDrCotVal"].pct_change()

        # Assuming risk-free rate is 0 for simplicity (replace with appropriate risk-free rate if needed)
        risk_free_rate = 0

        # Calculate excess daily returns by subtracting the risk-free rate
        excess_returns = returns - risk_free_rate

        # Calculate the standard deviation of excess returns
        volatility = np.std(excess_returns)

        # Calculate the average daily excess return
        average_excess_return = np.mean(excess_returns)

        # Calculate the annualized Sharpe Ratio
        sharpe_ratio = (average_excess_return / volatility) * np.sqrt(252)  # Assuming 252 trading days in a year

        return sharpe_ratio
    
    def sortino_ratio(self, fund):

        # Assuming you have two pandas Series or DataFrames: prices and nav
        # Replace 'your_prices' and 'your_nav' with the actual column names from your data

        # Calculate daily returns from historical prices
        returns = fund.history["pDrCotVal"].pct_change()

        # Assuming risk-free rate is 0 for simplicity (replace with appropriate risk-free rate if needed)
        risk_free_rate = 0

        # Calculate downside deviation using only negative returns
        downside_returns = np.minimum(returns, 0)
        downside_deviation = np.std(downside_returns)

        # Calculate the average daily return
        average_return = np.mean(returns)

        # Calculate the Sortino Ratio
        sortino_ratio = (average_return - risk_free_rate) / downside_deviation

        return sortino_ratio

    def alpha(self, fund, benchmark):
        # Assuming you have two pandas Series or DataFrames: prices and nav
        # Replace 'your_prices' and 'your_nav' with the actual column names from your data

        # Calculate daily returns from historical prices
        returns = fund.history["pDrCotVal"].pct_change()

        # Assuming you have a benchmark index returns, replace 'your_benchmark' with the actual column from your data
        benchmark_returns = benchmark.history["xNivInuClMresIbs"].pct_change()

        # Combine returns and benchmark_returns into a DataFrame
        data = pd.DataFrame({'ETF': returns, 'Benchmark': benchmark_returns})

        # Drop missing values
        data = data.dropna()

        # Add a constant to the independent variable for the intercept term
        X = sm.add_constant(data['Benchmark'])

        # Fit the linear regression model
        model = sm.OLS(data['ETF'], X).fit()

        # Get the alpha (intercept) from the model
        alpha = model.params['const']

        return alpha

    def r_squared(self, fund, benchmark):
        # Assuming you have two pandas Series or DataFrames: prices and nav
        # Replace 'your_prices' and 'your_nav' with the actual column names from your data

        # Calculate daily returns from historical prices
        returns = fund.history["pDrCotVal"].pct_change()

        # Assuming you have a benchmark index returns, replace 'your_benchmark' with the actual column from your data
        benchmark_returns = benchmark.history["xNivInuClMresIbs"].pct_change()

        # Combine returns and benchmark_returns into a DataFrame
        data = pd.DataFrame({'ETF': returns, 'Benchmark': benchmark_returns})

        # Drop missing values
        data = data.dropna()

        # Add a constant to the independent variable for the intercept term
        X = sm.add_constant(data['Benchmark'])

        # Fit the linear regression model
        model = sm.OLS(data['ETF'], X).fit()

        # Get the R-squared value from the model
        r_squared = model.rsquared

        return r_squared

    def treynor_ratio(self, fund, risk_free_rate):

        # Assuming you have two pandas Series or DataFrames: prices and nav
        # Replace 'your_prices' and 'your_nav' with the actual column names from your data

        # Calculate daily returns from historical prices
        returns = fund.history["pDrCotVal"].pct_change()

        # Assuming you have a risk-free rate, replace 'your_risk_free_rate' with the actual rate from your data
        # risk_free_rate = your_risk_free_rate / 100  # Convert to decimal

        # Combine returns and risk-free rate into a DataFrame
        data = pd.DataFrame({'ETF': returns, 'RiskFreeRate': risk_free_rate})

        # Drop missing values
        data = data.dropna()

        # Calculate excess returns by subtracting the risk-free rate
        excess_returns = data['ETF'] - data['RiskFreeRate']

        # Calculate the average excess return
        average_excess_return = np.mean(excess_returns)

        # Calculate the beta of the ETF using linear regression
        covariance_matrix = np.cov(data['ETF'], data['RiskFreeRate'])
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]

        # Calculate the Treynor Ratio
        treynor_ratio = average_excess_return / beta

        return treynor_ratio

    def jensens_alpha(self, fund, benchmark):
        # Assuming you have two pandas Series or DataFrames: prices and nav
        # Replace 'your_prices' and 'your_nav' with the actual column names from your data

        # Calculate daily returns from historical prices
        returns = fund.history["pDrCotVal"].pct_change()

        # Assuming you have a benchmark index returns, replace 'your_benchmark' with the actual column from your data
        benchmark_returns = benchmark.history["xNivInuClMresIbs"].pct_change()

        # Combine returns and benchmark_returns into a DataFrame
        data = pd.DataFrame({'ETF': returns, 'Benchmark': benchmark_returns})

        # Drop missing values
        data = data.dropna()

        # Add a constant to the independent variable for the intercept term
        X = sm.add_constant(data['Benchmark'])

        # Fit the linear regression model
        model = sm.OLS(data['ETF'], X).fit()

        # Get the alpha (intercept) from the model
        alpha = model.params['const']

        # Calculate the expected return based on the beta and benchmark return
        expected_return = model.params['Benchmark'] * data['Benchmark']

        # Calculate Jensen's Alpha
        jensens_alpha = np.mean(data['ETF'] - (expected_return + alpha))

        return jensens_alpha

    def capture_ratio(self, fund, benchmark):

        # Assuming you have two pandas Series or DataFrames: prices and nav
        # Replace 'your_prices' and 'your_nav' with the actual column names from your data

        # Calculate daily returns from historical prices
        returns = fund.history["pDrCotVal"].pct_change()

        # Assuming you have a benchmark index returns, replace 'your_benchmark' with the actual column from your data
        benchmark_returns = benchmark.history["xNivInuClMresIbs"].pct_change()

        # Combine returns and benchmark_returns into a DataFrame
        data = pd.DataFrame({'ETF': returns, 'Benchmark': benchmark_returns})

        # Drop missing values
        data = data.dropna()

        # Calculate Up Capture Ratio
        up_capture_ratio = np.sum(np.maximum(data['ETF'], 0) / np.maximum(data['Benchmark'], 0)) / np.sum(np.maximum(data['Benchmark'], 0))

        # Calculate Down Capture Ratio
        down_capture_ratio = np.sum(np.minimum(data['ETF'], 0) / np.minimum(data['Benchmark'], 0)) / np.sum(np.minimum(data['Benchmark'], 0))

        return {"up_capture_ratio" : up_capture_ratio, "down_capture_ratio": down_capture_ratio}


    def drawdown_analysis(self, fund):
        # Assuming you have a pandas DataFrame with historical prices or NAV
        # Replace 'your_data' with the actual DataFrame from your data

        # Calculate daily returns from historical prices
        returns = fund.history["pDrCotVal"].pct_change()

        # Calculate cumulative returns
        cumulative_returns = (1 + returns).cumprod()

        # Calculate cumulative maximum value (rolling maximum)
        cumulative_max = cumulative_returns.cummax()

        # Calculate drawdowns
        drawdowns = (cumulative_returns / cumulative_max - 1) * 100  # Convert to percentage

        # Plot drawdowns over time
        plt.figure(figsize=(10, 6))
        drawdowns.plot(title='Drawdown Analysis', ylabel='Drawdown (%)')
        plt.show()

    def portfolio_turnover():
        # Assuming you have a pandas DataFrame with historical prices or NAV
        # Replace 'your_data' with the actual DataFrame from your data

        # Calculate daily returns
        returns = your_data['Close'].pct_change()

        # Identify trading days (you may need to customize this based on your criteria)
        trading_days = returns.abs() > 0.01  # Example threshold of 1%

        # Estimate total purchases and sales
        total_purchases = returns[returns > 0].sum()
        total_sales = returns[returns < 0].sum()

        # Calculate average portfolio value
        average_portfolio_value = (your_data['Open'] + your_data['Close']) / 2

        # Calculate Portfolio Turnover
        portfolio_turnover = (total_purchases + total_sales) / average_portfolio_value.mean()

        print(f"Portfolio Turnover: {portfolio_turnover}")

    def information_ratio():
        # Assuming you have two pandas Series or DataFrames: prices and nav
        # Replace 'your_etf' and 'your_benchmark' with the actual column names from your data

        # Calculate daily returns
        returns_etf = your_etf['Close'].pct_change()
        returns_benchmark = your_benchmark['Close'].pct_change()

        # Calculate excess returns
        excess_returns = returns_etf - returns_benchmark

        # Calculate tracking error
        tracking_error = np.std(excess_returns)

        # Calculate Information Ratio
        information_ratio = np.mean(excess_returns) / tracking_error

        print(f"Information Ratio: {information_ratio}")







