"""
app.py - Main analysis script for Experiment 3: Enthalpy and Entropy of Vaporization.
Leverages Scipy and Numpy for OLS regression on linearized vapour pressure data.
"""

import numpy as np  # pyre-ignore[21]
import matplotlib.pyplot as plt  # pyre-ignore[21]
from scipy.stats import linregress  # pyre-ignore[21]
from constants import R, P_ATM_STD, REFERENCE_DATA  # pyre-ignore[21]

# ASCII DATA FLOW DIAGRAM
# -----------------------------------------------------------------------------
# [ INPUT: T_c (Celsius), P_trans (Pa) ]
#      |
#      v  (T_k = T_c + 273.15)
# [ CONVERSION: T_k (Kelvin), P_abs (Pa) ]  <-- P_abs = P_atm + P_trans
#      |
#      v  (x = 1/T_k, y = ln(P_abs))
# [ LINEARIZATION ]
#      |
#      v  (Slope = -dH/R, Intercept = dS/R)
# [ OLS REGRESSION ]
#      |
#      v
# [ RESULTS & PLOT (16:9) ]
# -----------------------------------------------------------------------------

# ASCII STATE TRANSITION DIAGRAM
# -----------------------------------------------------------------------------
# [ IDLE ] --(load)--> [ INGESTING ] --(invalid data)--> [ WARNING/HALT ]
#                          |
#                   (valid conversion)
#                          v
# [ SOLVING ] <--(OLS)-- [ LINEARIZED ]
#      |
#      v
# [ REPORTING ] <--(save)--> [ DONE ]
# -----------------------------------------------------------------------------

# ASCII FAILURE MODES
# -----------------------------------------------------------------------------
# [ T <= 0 K ]      -->  (1/T) Divergence / Physical Error
# [ P_abs <= 0 ]    -->  ln(P) Undefined / Vacuum Error
# [ N < 2 points ]  -->  Regression Underdetermined
# -----------------------------------------------------------------------------

def pressure_conversion(p_trans_pa, p_atm_pa=P_ATM_STD):
    """
    Explicit conversion from transducer pressure to absolute pressure.
    """
    # Vectorized check for bulk safety
    p_abs = p_atm_pa + p_trans_pa
    
    if np.any(p_abs <= 0):
        print("WARNING: Non-positive absolute pressure detected. Physics.exe has stopped.")
        
    return p_abs

def analyze_vaporization(temp_c, p_trans_pa, label="Compound"):
    """
    Performs Clausius-Clapeyron analysis using OLS regression.
    """
    # 1. Convert Units
    temp_k = temp_c + 273.15
    p_abs = pressure_conversion(p_trans_pa)
    
    # 2. Linearize Data
    # ln(P) = -dH/R * (1/T) + (dS/R + ln(P_std))
    x = 1.0 / temp_k
    y = np.log(p_abs)
    
    # 3. OLS Regression
    res = linregress(x, y)
    slope = float(res.slope)
    intercept = float(res.intercept)
    r_squared = float(res.rvalue**2)
    
    # 4. Extract Physical Constants
    # dH_vap = -slope * R
    dh_vap = (-1.0 * slope * R) / 1000.0  # kJ/mol
    
    # dS_vap (Standard State at P_ATM_STD)
    # intercept = dS/R + ln(P_std) => dS = (intercept - ln(P_std)) * R
    ds_vap = (intercept - np.log(P_ATM_STD)) * R
    
    # Normal Boiling Point (P = P_atm_std)
    # ln(P_atm) = slope * (1/Tb) + intercept
    x_b = (np.log(P_ATM_STD) - intercept) / slope
    t_b = 1.0 / x_b
    
    return {
        "label": label,
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_squared,
        "dH_vap": dh_vap,
        "dS_vap": ds_vap,
        "Tb": t_b,
        "x": x,
        "y": y
    }

def plot_results(results_list):
    """
    Generates a 16:9, high-DPI plot of the Clausius-Clapeyron regression.
    """
    plt.figure(figsize=(16, 9), dpi=300)
    
    for res in results_list:
        plt.scatter(res["x"], res["y"], label=f"{res['label']} Data")
        
        # Plot trendline
        x_fitted = np.linspace(min(res["x"]), max(res["x"]), 100)
        y_fitted = res["slope"] * x_fitted + res["intercept"]
        
        # Scientific notation for trendline label
        trend_label = f"{res['label']} Fit: y = {res['slope']:.4e}x + {res['intercept']:.4e}"
        plt.plot(x_fitted, y_fitted, '--', label=trend_label)
        
    plt.xlabel("1/T (K⁻¹)")
    plt.ylabel("ln(P/Pa)")
    plt.title("Clausius-Clapeyron Analysis: ln(P) vs 1/T")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig("vaporization_plot.png")
    print("\nPlot saved as 'vaporization_plot.png' (16:9, 300 DPI)")

def main():
    """
    Mission Control: Mock Dataset Verification.
    """
    print("--- Experiment 3: Enthalpy and Entropy of Vaporization ---")
    
    # Mock Data: Cyclohexane (approximate values for vibe check)
    # T (C): 20, 30, 40, 50, 60
    mock_t_c = np.array([20.0, 30.0, 40.0, 50.0, 60.0])
    
    # Generating mock transducer pressures based on NIST reference
    # P_abs = exp(-dH/(RT) + dS/R)
    ref = REFERENCE_DATA["cyclohexane"]
    slope_mock = -ref["dH_vap_ref"] * 1000 / R
    intercept_mock = ref["dS_vap_ref"] / R + np.log(P_ATM_STD) # dummy intercept roughly near atm
    
    p_abs_mock = np.exp(slope_mock / (mock_t_c + 273.15) + intercept_mock)
    p_trans_mock = p_abs_mock - P_ATM_STD # Back to transducer pressure
    
    # Run Analysis
    results = analyze_vaporization(mock_t_c, p_trans_mock, label="Cyclohexane (Mock)")
    
    # Print Summary
    print(f"\nResults for {results['label']}:")
    print(f"R² Value: {results['r_squared']:.6f}")
    print(f"ΔvapH:   {results['dH_vap']:.2f} kJ/mol  (NIST Ref: {ref['dH_vap_ref']} kJ/mol)")
    print(f"ΔvapS:   {results['dS_vap']:.2f} J/(mol*K)")
    print(f"Tb:      {results['Tb']:.2f} K           (NIST Ref: {ref['Tb_ref']} K)")
    
    # Generate Plot
    plot_results([results])

if __name__ == "__main__":
    main()
