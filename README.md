# Experiment 3: Enthalpy and Entropy of Vaporization

Automated analysis of vapour pressure data for Cyclohexane and Methanol using the Clausius-Clapeyron equation. This project follows Garry's Architecture Protocol v2.0.0.

## Mathematical Background

The temperature dependence of vapour pressure is described by the **Clausius-Clapeyron equation**:

$$\ln(P) = -\frac{\Delta_{vap}H}{R} \left(\frac{1}{T}\right) + \frac{\Delta_{vap}S}{R}$$

Where:

- $P$ is the absolute vapour pressure (Pa).
- $T$ is the absolute temperature (K).
- $\Delta_{vap}H$ is the enthalpy of vaporization (J/mol).
- $\Delta_{vap}S$ is the entropy of vaporization (J/mol·K).
- $R$ is the universal gas constant (8.314 J/mol·K).

By plotting $\ln(P)$ vs $1/T$, we can determine $\Delta_{vap}H$ from the slope and $\Delta_{vap}S$ from the intercept.

## Mission Control: Usage Guide

### 1. Prerequisites

Ensure you have the required Python packages installed:

```bash
pip install numpy matplotlib scipy
```

### 2. Project Structure

- `constants.py`: Physical constants ($R$, $P_{atm}$) and NIST reference data.
- `app.py`: Main processing script (Linearization, OLS Regression, Plotting).
- `README.md`: This documentation.

### 3. Execution

To verify the architecture with the built-in Mock Dataset, run:

```bash
python app.py
```

### 4. Analysis Features

- **Pressure Conversion**: Automatically handles $P_{abs} = P_{atm} + P_{trans}$.
- **High-DPI Plotting**: Generates a 16:9 aspect ratio plot (`vaporization_plot.png`) at 300 DPI.
- **Scientific Notation**: Trendlines are labeled using scientific notation for precision.
- **Validation**: Compares experimental results against NIST reference values stored in `constants.py`.

## Data Flow

```text
[ Raw Lab Data ] -> [ app.py: Conversion ] -> [ app.py: OLS ] -> [ Visual/Numeric Results ]
```
