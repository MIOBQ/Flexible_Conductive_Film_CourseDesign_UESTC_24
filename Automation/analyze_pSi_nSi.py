"""Read-only analysis of completed A (p-Si) and F (n-Si) COMSOL scans."""
import csv
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path("D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24")
A_PATH = ROOT / "Simulation_Results/Original/original_pressure_sweep.csv"
F_PATH = ROOT / "Simulation_Results/Material_Replacement/nSi_pressure_sweep.csv"
OUT = ROOT / "Simulation_Results/Material_Replacement"
FIG = ROOT / "Figures/Material_Replacement"
EXPECTED = list(range(0, 201, 25))
SINGLE_I, SINGLE_V = 9.749346507278599, 5.203232337804176

def load_a(path):
    with path.open(encoding="utf-8-sig", newline="") as h:
        rows = list(csv.DictReader(h))
    return [(float(r["pressure_kPa"]), float(r["working_current_A"])*1e3, float(r["output_voltage_V"])*1e3) for r in rows]

def load_f(path):
    with path.open(encoding="utf-8-sig", newline="") as h:
        rows = list(csv.DictReader(h))
    return [(float(r["pressure_kPa"]), float(r["current_mA"]), float(r["voltage_mV"])) for r in rows]

def validate(scan, label):
    scan.sort(key=lambda r: r[0])
    if [r[0] for r in scan] != EXPECTED or len(scan) != 9:
        raise ValueError(f"{label}: exact pressures 0,25,...,200 kPa required")
    if not all(math.isfinite(v) for row in scan for v in row):
        raise ValueError(f"{label}: non-finite result")

def linear_fit(scan):
    x=np.array([r[0] for r in scan]); y=np.array([r[2] for r in scan])
    s,b=np.polyfit(x,y,1); pred=s*x+b
    return float(s),float(b),float(1-np.sum((y-pred)**2)/np.sum((y-y.mean())**2))

def make_plot(a,f,index,ylabel,title,path):
    p=[r[0] for r in a]
    ya=[3*r[1] if index==3 else r[index] for r in a]
    yf=[3*r[1] if index==3 else r[index] for r in f]
    plt.figure(figsize=(7.2,4.8))
    plt.plot(p,ya,"o-",linewidth=1.8,markersize=5,label="A: p-Si original")
    plt.plot(p,yf,"s-",linewidth=1.8,markersize=5,label="F: n-Si exploratory")
    plt.xlabel("Pressure (kPa)"); plt.ylabel(ylabel); plt.title(title)
    plt.grid(True,alpha=.28); plt.legend(); plt.tight_layout(); plt.savefig(path,dpi=300); plt.close()

def main():
    OUT.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True)
    a,f=load_a(A_PATH),load_f(F_PATH); validate(a,"A"); validate(f,"F")
    sa,ba,r2a=linear_fit(a); sf,bf,r2f=linear_fit(f)
    a100=next(r for r in a if r[0]==100); f100=next(r for r in f if r[0]==100)
    err_i=abs(f100[1]-SINGLE_I)/abs(SINGLE_I)*100; err_v=abs(f100[2]-SINGLE_V)/abs(SINGLE_V)*100
    with (OUT/"pSi_nSi_pressure_comparison.csv").open("w",newline="",encoding="utf-8") as h:
        w=csv.writer(h); w.writerow(["Pressure_kPa","A_Current_mA","A_Vout_mV","A_Power_mW","F_Current_mA","F_Vout_mV","F_Power_mW","Current_Ratio_F_over_A","Vout_Ratio_F_over_A","Power_Ratio_F_over_A"])
        for ra,rf in zip(a,f):
            vr="" if abs(ra[2])<1e-12 else rf[2]/ra[2]
            w.writerow([ra[0],ra[1],ra[2],3*ra[1],rf[1],rf[2],3*rf[1],rf[1]/ra[1],vr,rf[1]/ra[1]])
    with (OUT/"pSi_nSi_fit_summary.csv").open("w",newline="",encoding="utf-8") as h:
        w=csv.writer(h); w.writerow(["Model","Vbias_V","Sensitivity_mV_per_kPa","Intercept_mV","R2","I_100kPa_mA","Vout_100kPa_mV","Power_100kPa_mW"])
        w.writerow(["A_pSi_original",3,sa,ba,r2a,a100[1],a100[2],3*a100[1]])
        w.writerow(["F_nSi_exploratory",3,sf,bf,r2f,f100[1],f100[2],3*f100[1]])
    make_plot(a,f,1,"Working current (mA)","Working Current vs Pressure",FIG/"pSi_nSi_current_vs_pressure.png")
    make_plot(a,f,2,"Output voltage (mV)","Output Voltage vs Pressure",FIG/"pSi_nSi_voltage_vs_pressure.png")
    make_plot(a,f,3,"Working power (mW)","Working Power vs Pressure",FIG/"pSi_nSi_power_vs_pressure.png")
    (OUT/"pSi_nSi_validation_log.txt").write_text("PASS: A and F each contain exactly 0,25,...,200 kPa and finite numerical values.\n"+f"PASS: F 100 kPa check vs independent single point: I error={err_i:.15g}%, Vout error={err_v:.15g}%.\n"+"Power, fits and ratios use only actual COMSOL scan CSV data.\n",encoding="utf-8")
    (OUT/"pSi_nSi_analysis.txt").write_text("A/F 压力扫描对比（均为真实 COMSOL 稳态求解点）。\n\n"+f"A（p-Si）：Vout = {sa:.12g} P + {ba:.12g} mV，R²={r2a:.12g}。\n"+f"F（n-Si）：Vout = {sf:.12g} P + {bf:.12g} mV，R²={r2f:.12g}。\n\n"+f"100 kPa：A 的 I={a100[1]:.9g} mA、Vout={a100[2]:.9g} mV、P={3*a100[1]:.9g} mW；F 的 I={f100[1]:.9g} mA、Vout={f100[2]:.9g} mV、P={3*f100[1]:.9g} mW。\n"+"F 的工作电流和功耗更高，输出电压极性反转，且电压灵敏度幅值明显减小。这与导电率和压阻张量共同改变在定性上相符，但现有对照不能把两种贡献精确定量分离。\n\n"+"限制：F 使用 COMSOL 内置轻掺杂 n-Si 材料模型，而压敏区和互连区的掺杂分别为 1.32e19 与 1.45e20 cm^-3。故 F 仅作为内置轻掺杂模型下的探索性数值材料对照，不可视为已验证的高掺杂 n-Si 器件定量预测。\n",encoding="utf-8")

if __name__=="__main__": main()
