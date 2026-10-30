import csv, math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(r'D:\Github_codes\Flexible_Conductive_Film_CourseDesign_UESTC_24'); OUT=ROOT/'Simulation_Results'/'Extended_Design'; FIG=ROOT/'Figures'/'Extended_Design'; FIG.mkdir(parents=True,exist_ok=True)
P=[0,25,50,75,100,125,150,175,200]
def load(path):
 with path.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
 data=[]
 for r in rows:
  p=float(r.get('Pressure_kPa',r.get('pressure_kPa'))); i=float(r['Current_mA']) if 'Current_mA' in r else float(r['working_current_A'])*1e3; v=float(r['Vout_mV']) if 'Vout_mV' in r else float(r['output_voltage_V'])*1e3; data.append((p,i,v))
 if [x[0] for x in data]!=P or not all(math.isfinite(y) for x in data for y in x): raise ValueError('invalid '+str(path))
 return data
a=load(OUT/'original_2V_pressure_sweep.csv'); b=load(ROOT/'Simulation_Results'/'Original'/'original_pressure_sweep.csv')
def fit(d):
 x=np.array(P);y=np.array([q[2] for q in d]);s,c=np.polyfit(x,y,1);return s,c,1-((y-(s*x+c))**2).sum()/((y-y.mean())**2).sum()
f2,f3=fit(a),fit(b)
with (OUT/'original_2V_3V_comparison.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Pressure_kPa','Current_2V_mA','Vout_2V_mV','Power_2V_mW','Current_3V_mA','Vout_3V_mV','Power_3V_mW','Current_Ratio_2V_3V','Vout_Ratio_2V_3V','Power_Ratio_2V_3V'])
 for x,y in zip(a,b):w.writerow([x[0],x[1],x[2],2*x[1],y[1],y[2],3*y[1],x[1]/y[1],'' if abs(y[2])<1 else x[2]/y[2],2*x[1]/(3*y[1])])
with (OUT/'original_2V_3V_fit_summary.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Bias_V','Sensitivity_mV_per_kPa','Intercept_mV','R2']);w.writerow([2,*f2]);w.writerow([3,*f3])
for idx,name,ylabel in [(1,'current','Current (mA)'),(2,'voltage','Output Voltage (mV)')]:
 plt.figure(figsize=(7,4.5),dpi=300);plt.plot(P,[q[idx] for q in a],'o-',label='2 V');plt.plot(P,[q[idx] for q in b],'s-',label='3 V');plt.xlabel('Pressure (kPa)');plt.ylabel(ylabel);plt.grid(True,alpha=.3);plt.legend();plt.tight_layout();plt.savefig(FIG/f'original_2V_3V_{name}_vs_pressure.png');plt.close()
plt.figure(figsize=(7,4.5),dpi=300);plt.plot(P,[2*q[1] for q in a],'o-',label='2 V');plt.plot(P,[3*q[1] for q in b],'s-',label='3 V');plt.xlabel('Pressure (kPa)');plt.ylabel('Power (mW)');plt.grid(True,alpha=.3);plt.legend();plt.tight_layout();plt.savefig(FIG/'original_2V_3V_power_vs_pressure.png');plt.close()
ir=[x[1]/y[1] for x,y in zip(a,b)];vr=[x[2]/y[2] for x,y in zip(a,b) if abs(y[2])>=1];pr=[2*x[1]/(3*y[1]) for x,y in zip(a,b)]
with (OUT/'original_2V_3V_analysis_log.txt').open('w',encoding='utf-8') as f:f.write(f'CSV validation: 9 aligned finite points.\n2V S={f2[0]:.12g}, b={f2[1]:.12g}, R2={f2[2]:.12g}\n3V S={f3[0]:.12g}, b={f3[1]:.12g}, R2={f3[2]:.12g}\nSensitivity ratio={f2[0]/f3[0]:.12g}\nMax deviations: I {max(abs(x-2/3) for x in ir):.3g}; V(excluding |3V|<1mV) {max(abs(x-2/3) for x in vr):.3g}; P {max(abs(x-4/9) for x in pr):.3g}\n')
with (OUT/'original_2V_3V_chinese_analysis.txt').open('w',encoding='utf-8') as f:f.write('实际COMSOL数据表明，电流随压力仅小幅下降；输出电压随压力近似线性负向变化。2 V下绝对电压灵敏度约为3 V下的2/3，同时功耗约为3 V下的4/9，体现降低偏置的功耗收益与信号幅值代价。该结论不涉及噪声、SNR或最小可检测压力，不能直接概括为总体性能变差。\n')
print('SUCCESS')
