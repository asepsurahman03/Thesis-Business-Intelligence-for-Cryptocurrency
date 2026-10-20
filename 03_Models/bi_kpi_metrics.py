# ENHANCED BUSINESS INTELLIGENCE METRICS
## Financial KPIs Implementation for Bitcoin Trading Analysis

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, List

class BitcoinBIKPIs:
    """
    Comprehensive Business Intelligence KPIs for Bitcoin Trading
    """
    
    def __init__(self, prices: pd.Series, predictions: pd.Series = None):
        """
        Initialize KPI calculator
        
        Args:
            prices: Historical Bitcoin prices
            predictions: Model predictions (optional)
        """
        self.prices = prices
        self.predictions = predictions
        self.returns = self._calculate_returns()
    
    def _calculate_returns(self) -> pd.Series:
        """Calculate logarithmic returns"""
        return np.log(self.prices / self.prices.shift(1)).dropna()
    
    def sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe Ratio
        
        Args:
            risk_free_rate: Annual risk-free rate (default 2%)
            
        Returns:
            Sharpe Ratio value
        """
        # Convert annual to daily
        daily_rf = risk_free_rate / 365
        
        # Calculate excess returns
        excess_returns = self.returns - daily_rf
        
        # Annualized Sharpe Ratio
        return np.sqrt(365) * excess_returns.mean() / excess_returns.std()
    
    def value_at_risk(self, confidence_level: float = 0.05) -> float:
        """
        Calculate Value at Risk (VaR)
        
        Args:
            confidence_level: Confidence level (default 95% -> 0.05)
            
        Returns:
            VaR value
        """
        return np.percentile(self.returns, confidence_level * 100)
    
    def conditional_var(self, confidence_level: float = 0.05) -> float:
        """
        Calculate Conditional VaR (Expected Shortfall)
        
        Args:
            confidence_level: Confidence level
            
        Returns:
            CVaR value
        """
        var_threshold = self.value_at_risk(confidence_level)
        return self.returns[self.returns <= var_threshold].mean()
    
    def maximum_drawdown(self) -> Tuple[float, pd.Timestamp, pd.Timestamp]:
        """
        Calculate Maximum Drawdown
        
        Returns:
            Tuple of (max_dd, start_date, end_date)
        """
        cumulative = (1 + self.returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        
        max_dd = drawdown.min()
        end_date = drawdown.idxmin()
        start_date = cumulative[:end_date].idxmax()
        
        return max_dd, start_date, end_date
    
    def volatility(self, window: int = 30) -> pd.Series:
        """
        Calculate rolling volatility
        
        Args:
            window: Rolling window size
            
        Returns:
            Rolling volatility series
        """
        return self.returns.rolling(window=window).std() * np.sqrt(365)
    
    def beta(self, market_prices: pd.Series = None) -> float:
        """
        Calculate Beta (systematic risk)
        
        Args:
            market_prices: Market benchmark prices (optional)
            
        Returns:
            Beta value
        """
        if market_prices is None:
            # Use crypto index as proxy
            market_prices = self.prices  # Simplified
        
        market_returns = np.log(market_prices / market_prices.shift(1)).dropna()
        
        # Align returns
        aligned_returns = pd.concat([self.returns, market_returns], axis=1).dropna()
        aligned_returns.columns = ['asset', 'market']
        
        # Calculate beta
        covariance = aligned_returns.cov().iloc[0, 1]
        market_variance = aligned_returns['market'].var()
        
        return covariance / market_variance
    
    def information_ratio(self, benchmark_prices: pd.Series = None) -> float:
        """
        Calculate Information Ratio
        
        Args:
            benchmark_prices: Benchmark prices (optional)
            
        Returns:
            Information Ratio value
        """
        if benchmark_prices is None:
            return 0.0
        
        benchmark_returns = np.log(benchmark_prices / benchmark_prices.shift(1)).dropna()
        
        # Align returns
        aligned_returns = pd.concat([self.returns, benchmark_returns], axis=1).dropna()
        aligned_returns.columns = ['portfolio', 'benchmark']
        
        # Active returns
        active_returns = aligned_returns['portfolio'] - aligned_returns['benchmark']
        
        # Information Ratio
        return active_returns.mean() / active_returns.std()
    
    def sortino_ratio(self, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sortino Ratio (downside risk-adjusted return)
        
        Args:
            risk_free_rate: Annual risk-free rate
            
        Returns:
            Sortino Ratio value
        """
        daily_rf = risk_free_rate / 365
        excess_returns = self.returns - daily_rf
        
        # Downside deviation
        downside_returns = excess_returns[excess_returns < 0]
        downside_deviation = downside_returns.std()
        
        # Annualized Sortino Ratio
        return np.sqrt(365) * excess_returns.mean() / downside_deviation
    
    def calmar_ratio(self) -> float:
        """
        Calculate Calmar Ratio (return to maximum drawdown)
        
        Returns:
            Calmar Ratio value
        """
        max_dd, _, _ = self.maximum_drawdown()
        annual_return = self.returns.mean() * 365
        
        return annual_return / abs(max_dd)
    
    def prediction_metrics(self) -> Dict[str, float]:
        """
        Calculate prediction-specific metrics if predictions are available
        
        Returns:
            Dictionary of prediction metrics
        """
        if self.predictions is None:
            return {}
        
        # Directional accuracy
        actual_direction = np.diff(self.prices) > 0
        pred_direction = np.diff(self.predictions) > 0
        
        directional_accuracy = np.mean(actual_direction == pred_direction)
        
        # Prediction error metrics
        mse = np.mean((self.prices - self.predictions) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(self.prices - self.predictions))
        
        # Signal-to-noise ratio
        signal_power = np.mean(self.predictions ** 2)
        noise_power = np.mean((self.prices - self.predictions) ** 2)
        snr = 10 * np.log10(signal_power / noise_power)
        
        return {
            'directional_accuracy': directional_accuracy,
            'rmse': rmse,
            'mae': mae,
            'signal_to_noise_ratio': snr
        }
    
    def generate_kpi_report(self) -> Dict[str, any]:
        """
        Generate comprehensive KPI report
        
        Returns:
            Dictionary with all KPIs
        """
        max_dd, dd_start, dd_end = self.maximum_drawdown()
        
        report = {
            'return_metrics': {
                'total_return': (self.prices.iloc[-1] / self.prices.iloc[0] - 1) * 100,
                'annual_return': self.returns.mean() * 365 * 100,
                'volatility': self.returns.std() * np.sqrt(365) * 100
            },
            'risk_metrics': {
                'sharpe_ratio': self.sharpe_ratio(),
                'sortino_ratio': self.sortino_ratio(),
                'calmar_ratio': self.calmar_ratio(),
                'max_drawdown': max_dd * 100,
                'var_95': self.value_at_risk(0.05) * 100,
                'cvar_95': self.conditional_var(0.05) * 100
            },
            'drawdown_info': {
                'max_drawdown_start': dd_start,
                'max_drawdown_end': dd_end,
                'drawdown_duration': (dd_end - dd_start).days
            }
        }
        
        # Add prediction metrics if available
        if self.predictions is not None:
            report['prediction_metrics'] = self.prediction_metrics()
        
        return report

# Usage Example
if __name__ == "__main__":
    # Sample data
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=365, freq='D')
    prices = pd.Series(
        np.cumsum(np.random.randn(365) * 0.02) + 100,
        index=dates
    )
    
    # Initialize KPI calculator
    kpi_calculator = BitcoinBIKPIs(prices)
    
    # Generate report
    report = kpi_calculator.generate_kpi_report()
    
    print("=== BITCOIN TRADING KPI REPORT ===")
    print(f"Total Return: {report['return_metrics']['total_return']:.2f}%")
    print(f"Annual Return: {report['return_metrics']['annual_return']:.2f}%")
    print(f"Volatility: {report['return_metrics']['volatility']:.2f}%")
    print(f"Sharpe Ratio: {report['risk_metrics']['sharpe_ratio']:.3f}")
    print(f"Max Drawdown: {report['risk_metrics']['max_drawdown']:.2f}%")
    print(f"VaR (95%): {report['risk_metrics']['var_95']:.2f}%")
    print(f"CVaR (95%): {report['risk_metrics']['cvar_95']:.2f}%")
