"""
constants.py - Physical constants and NIST reference data for Experiment 3.
"""

# Universal Gas Constant (J/(mol*K))
R = 8.314

# Standard Atmospheric Pressure (Pa)
P_ATM_STD = 101325.0

# NIST Reference Data
# -----------------------------------------------------------------------------
# Cyclohexane (C6H12)
# Ref: https://webbook.nist.gov/cgi/cbook.cgi?ID=C110827&Units=SI&Mask=4#Thermo-Phase
CYCLOHEXANE_REF = {
    "name": "Cyclohexane",
    "dH_vap_ref": 32.0,       # kJ/mol at 298 K
    "Tb_ref": 353.9,          # K (Standard boiling point)
    "dS_vap_ref": 90.4        # J/(mol*K) (Trouton's rule/NIST approx)
}

# Methanol (CH3OH)
# Ref: https://webbook.nist.gov/cgi/cbook.cgi?ID=C67561&Units=SI&Mask=4#Thermo-Phase
METHANOL_REF = {
    "name": "Methanol",
    "dH_vap_ref": 37.4,       # kJ/mol at 298 K
    "Tb_ref": 337.8,          # K (Standard boiling point)
    "dS_vap_ref": 110.7       # J/(mol*K)
}

# Mapping for easy lookup
REFERENCE_DATA = {
    "cyclohexane": CYCLOHEXANE_REF,
    "methanol": METHANOL_REF
}
