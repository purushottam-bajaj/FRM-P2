import math

class CreditAsset:
    """
    Represents a single credit asset (loan) with risk parameters.
    """
    def __init__(self, name, ead, pd, lgd, sigma_pd, sigma_lgd):
        self.name = name
        self.ead = ead          # Exposure at Default ($)
        self.pd = pd            # Probability of Default (decimal)
        self.lgd = lgd          # Loss Given Default (decimal)
        self.sigma_pd = sigma_pd    # Std Dev of PD
        self.sigma_lgd = sigma_lgd  # Std Dev of LGD

    def calculate_expected_loss(self):
        """EL = EAD * PD * LGD"""
        return self.ead * self.pd * self.lgd

    def calculate_unexpected_loss(self):
        """
        UL = EAD * sqrt( (PD * sigma_LGD^2) + (LGD^2 * sigma_PD^2) )
        This formula captures the variability of loss.
        """
        term1 = self.pd * (self.sigma_lgd ** 2)
        term2 = (self.lgd ** 2) * (self.sigma_pd ** 2)
        return self.ead * math.sqrt(term1 + term2)

def calculate_portfolio_metrics(asset1, asset2, correlation, capital_multiplier=3.0):
    """
    Calculates Portfolio EL, UL, and Economic Capital.
    """
    # 1. Portfolio Expected Loss (Sum of individuals)
    el1 = asset1.calculate_expected_loss()
    el2 = asset2.calculate_expected_loss()
    portfolio_el = el1 + el2

    # 2. Portfolio Unexpected Loss (Square root of variance formula)
    ul1 = asset1.calculate_unexpected_loss()
    ul2 = asset2.calculate_unexpected_loss()
    
    # Variance_p = UL1^2 + UL2^2 + 2 * rho * UL1 * UL2
    portfolio_ul_variance = (ul1**2) + (ul2**2) + (2 * correlation * ul1 * ul2)
    portfolio_ul = math.sqrt(portfolio_ul_variance)

    # 3. Risk Contributions (RC)
    # How much of the Portfolio UL is caused by each asset?
    rc1 = (ul1 * (ul1 + correlation * ul2)) / portfolio_ul
    rc2 = (ul2 * (ul2 + correlation * ul1)) / portfolio_ul

    # 4. Economic Capital
    # Capital needed to cover losses at a high confidence level
    economic_capital = portfolio_ul * capital_multiplier

    return {
        "Individual ELs": (el1, el2),
        "Individual ULs": (ul1, ul2),
        "Portfolio EL": portfolio_el,
        "Portfolio UL": portfolio_ul,
        "Risk Contributions": (rc1, rc2),
        "Economic Capital": economic_capital
    }

def run_simulation():
    # Example from your text: XYZ Bank Loan
    # EAD: 1.8M, PD: 1%, LGD: 40%, Sigma_PD: 10%, Sigma_LGD: 30%
    loan_a = CreditAsset("Loan A", 1800000, 0.01, 0.40, 0.10, 0.30)
    
    # Let's create a second loan for a portfolio
    loan_b = CreditAsset("Loan B", 2000000, 0.02, 0.50, 0.12, 0.35)

    print("--- Single Asset Analysis (Loan A) ---")
    print(f"Expected Loss (EL): ${loan_a.calculate_expected_loss():,.2f}")
    print(f"Unexpected Loss (UL): ${loan_a.calculate_unexpected_loss():,.2f}")
    print(f"UL as % of Exposure: {(loan_a.calculate_unexpected_loss()/loan_a.ead)*100:.2f}%")

    print("\n--- Portfolio Analysis (Loan A + Loan B) ---")
    corr = 0.3  # Correlation factor
    results = calculate_portfolio_metrics(loan_a, loan_b, correlation=corr)

    print(f"Correlation: {corr}")
    print(f"Portfolio EL: ${results['Portfolio EL']:,.2f}")
    print(f"Portfolio UL: ${results['Portfolio UL']:,.2f}")
    print(f"Economic Capital (at 3x multiplier): ${results['Economic Capital']:,.2f}")
    print(f"Risk Contribution Loan A: ${results['Risk Contributions'][0]:,.2f}")
    print(f"Risk Contribution Loan B: ${results['Risk Contributions'][1]:,.2f}")

    # Demonstrate Effect of Correlation
    print("\n--- Effect of Diversification ---")
    low_corr_results = calculate_portfolio_metrics(loan_a, loan_b, correlation=0.1)
    print(f"Portfolio UL at 0.1 Correlation: ${low_corr_results['Portfolio UL']:,.2f}")
    print(f"Reduction in UL due to diversification: ${results['Portfolio UL'] - low_corr_results['Portfolio UL']:,.2f}")

if __name__ == "__main__":
    run_simulation()