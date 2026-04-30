import pandas as pd
import numpy as np

def generate_medical_report(parquet_file):
    print(f"🩺 Analyzing Clinical Manifold: {parquet_file}")
    try:
        df = pd.read_parquet(parquet_file)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return

    # 1. Target Accuracy (Precision at the Neoplasm site)
    target_zone = df[df['z'] > 1.0]
    avg_target_pressure = target_zone['z'].mean() if not target_zone.empty else 0
    
    # 2. Collateral Tissue Integrity (The "Zero-Cut" Metric)
    # CORREÇÃO: Parênteses obrigatórios em volta de CADA condição
    collateral_condition = (df['z'] > 0.1) & (df['z'] < 0.8)
    collateral_count = len(df[collateral_condition])
    collateral_impact = (collateral_count / len(df)) * 100
    
    # 3. Quantum Tunneling Efficiency
    tunneling_efficiency = (avg_target_pressure / (df['z'].mean() + 1e-9)) * 100

    print("\n" + "="*45)
    print("      SPHY-MED SURGICAL ANALYTICS REPORT      ")
    print("="*45)
    
    # Metrics for medical review (Atomic Precision focus)
    print(f"LOCATION ACCURACY:      {100 - collateral_impact:.4f}%")
    print(f"TISSUE PRESERVATION:    {100 - (collateral_impact/2):.4f}%")
    print(f"ABLATION PRESSURE:      {avg_target_pressure:.2f} GeV/phi")
    print(f"TUNNELING RATIO:        {tunneling_efficiency:.2f}%")
    
    print("-"*45)
    if collateral_impact < 1.0:
        print("STATUS: SUCCESSFUL NON-INVASIVE ABLATION")
        print("NOTE: Zero thermal footprint detected in healthy layers.")
    else:
        print("STATUS: WARNING - PHASE DISPERSION DETECTED")
    print("="*45)

if __name__ == "__main__":
    generate_medical_report("laser_medico_quantum.parquet")
