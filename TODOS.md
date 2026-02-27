# Future Roadmap: Agentic Thermodynamics v4.0

## 🚀 Near-Term Scaling

- [ ] **Automated Stabilisation Detection**: Implement a rolling standard deviation check on pressure readings to automatically flag when the system has reached equilibrium (Δp/Δt < threshold).
- [ ] **Uncertainty Propagation**: Add a module to propagate error from the pressure transducer (±0.05 mbar) through the ln(P) transformation to provide error bars on ΔvapH.

## 🤖 Engineering 3.0 Integration

- [ ] **Physical-Digital Bridge**: Interface the digital pressure transducer via Serial/USB (RS232) for real-time data ingestion directly into the OLS engine.
- [ ] **Multimodal Verification**: Use computer vision (OpenCV) to monitor the liquid levels in the isoteniscope U-tube and verify "perfect leveling" autonomously.

## 🧪 Scientific Extensions

- [ ] **Azeotrope Mapping**: Extend the engine to handle binary liquid mixtures (Cyclohexane + Methanol) to calculate activity coefficients and non-ideal deviations.
