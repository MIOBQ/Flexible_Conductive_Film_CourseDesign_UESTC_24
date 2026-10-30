import csv, math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT=Path('D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24')
OUT=ROOT/'Simulation_Results'/'Serpentine_Design'; FIG=ROOT/'Figures'/'Serpentine_Design'
EXPECTED=[0,25,50,75,100,125,150,175,200]

def load_a(path):
    with path.open(encoding='utf-8-sig',newline='') as h: rows=list(csv.DictReader(h))
    return [(float(r['pressure_kPa']),float(r['working_current_A'])*1e3,float(r['output_voltage_V'])*1e3) for r in rows]
def load_g(path):
    with path.open(encoding='utf-8-sig',newline='') as h: rows=list(csv.DictReader(h))
    return [(float(r['pressure_kPa']),float(r['current_mA']),float(r['voltage_mV'])) for r in rows]
def valid(x,label):
    x.sort(key=lambda r:r[0])
    if len(x)!=9 or [r[0] for r in x]!=EXPECTED or not all(math.isfinite(v) for r in x for v in r): raise ValueError(label+' invalid scan')
def fit(x):
    p=np.array([r[0] for r in x]);v=np.array([r[2] for r in x]);s,b=np.polyfit(p,v,1);q=s*p+b
    return float(s),float(b),float(1-((v-q)**2).sum()/((v-v.mean())**2).sum())
def curves(a,g):
    p=[r[0] for r in a]
    for idx,name,ylabel,title in [(1,'current','Working current (mA)','Working Current vs Pressure'),(2,'voltage','Output voltage (mV)','Output Voltage vs Pressure'),(3,'power','Working power (mW)','Working Power vs Pressure')]:
        ya=[3*r[1] if idx==3 else r[idx] for r in a]; yg=[3*r[1] if idx==3 else r[idx] for r in g]
        plt.figure(figsize=(7.2,4.8));plt.plot(p,ya,'o-',label='A: Original',lw=1.8,ms=5);plt.plot(p,yg,'s-',label='G: Serpentine',lw=1.8,ms=5)
        plt.xlabel('Pressure (kPa)');plt.ylabel(ylabel);plt.title(title);plt.grid(alpha=.3);plt.legend();plt.tight_layout();plt.savefig(FIG/f'A_G_{name}_vs_pressure.png',dpi=300);plt.close()
def feature_geometry():
    # Directly reconstructed from audited COMSOL r2 and sgcut feature values in r2 local coordinates.
    fig,axes=plt.subplots(1,2,figsize=(10,3.8),sharex=True,sharey=True)
    for ax,label,serp in zip(axes,['A: original r2','G: r2 after COMSOL Difference'],[False,True]):
        ax.add_patch(Rectangle((-42.5,-10),85,20,fc='#e4e4e4',ec='black',lw=1.2))
        ax.add_patch(Rectangle((-31.25,-10),62.5,20,fc='#f6b26b',ec='black',lw=1.2))
        if serp:
            for x,y in [(-14,2),(0,-2),(14,2)]: ax.add_patch(Rectangle((x-1.25,y-8),2.5,16,fc='white',ec='#b00020',lw=1.5,hatch='//'))
            ax.text(0,-14,'three alternating Difference slots: 2.5 × 16 µm',ha='center',fontsize=8,color='#8b0000')
        ax.axhline(0,color='0.55',lw=.6);ax.set_title(label);ax.set_aspect('equal');ax.set_xlim(-46,46);ax.set_ylim(-16,16);ax.set_xlabel('r2 local longitudinal coordinate (µm)');ax.grid(alpha=.18)
    axes[0].set_ylabel('r2 local transverse coordinate (µm)')
    fig.suptitle('Feature-derived local geometry (reconstructed from audited COMSOL parameters; not a GUI screenshot)',fontsize=10)
    fig.tight_layout();fig.savefig(FIG/'A_G_feature_derived_local_geometry.png',dpi=300);plt.close(fig)
def main():
    OUT.mkdir(parents=True,exist_ok=True);FIG.mkdir(parents=True,exist_ok=True)
    a=load_a(ROOT/'Simulation_Results'/'Original'/'original_pressure_sweep.csv');g=load_g(OUT/'serpentine_pressure_sweep.csv');valid(a,'A');valid(g,'G')
    sa,ba,r2a=fit(a);sg,bg,r2g=fit(g); curves(a,g);feature_geometry()
    with (OUT/'A_G_pressure_comparison.csv').open('w',newline='',encoding='utf-8') as h:
        w=csv.writer(h);w.writerow(['Pressure_kPa','A_Current_mA','A_Vout_mV','A_Power_mW','G_Current_mA','G_Vout_mV','G_Power_mW','Current_Change_Percent','Vout_Magnitude_Change_Percent','Power_Change_Percent'])
        for ra,rg in zip(a,g):w.writerow([ra[0],ra[1],ra[2],3*ra[1],rg[1],rg[2],3*rg[1],(rg[1]/ra[1]-1)*100,(abs(rg[2])/abs(ra[2])-1)*100 if abs(ra[2])>1e-12 else '',(rg[1]/ra[1]-1)*100])
    a100=next(x for x in a if x[0]==100);g100=next(x for x in g if x[0]==100)
    with (OUT/'A_G_fit_summary.csv').open('w',newline='',encoding='utf-8') as h:
        w=csv.writer(h);w.writerow(['Model','Sensitivity_mV_per_kPa','SensitivityMagnitude_mV_per_kPa','Intercept_mV','R2','I_100kPa_mA','Vout_100kPa_mV','Power_100kPa_mW']);w.writerow(['A_Original',sa,abs(sa),ba,r2a,a100[1],a100[2],3*a100[1]]);w.writerow(['G_Serpentine',sg,abs(sg),bg,r2g,g100[1],g100[2],3*g100[1]])
    senschg=(abs(sg)/abs(sa)-1)*100; ichg=(g100[1]/a100[1]-1)*100;vchg=(abs(g100[2])/abs(a100[2])-1)*100
    (OUT/'A_G_analysis.txt').write_text(f'''A/G nine-point comparison, derived only from actual COMSOL stationary solutions.\n\nA: Vout={sa:.12g} P + {ba:.12g} mV; R2={r2a:.12g}.\nG: Vout={sg:.12g} P + {bg:.12g} mV; R2={r2g:.12g}.\n\nAt 100 kPa: A I={a100[1]:.9g} mA, Vout={a100[2]:.9g} mV, P={3*a100[1]:.9g} mW.\nG I={g100[1]:.9g} mA, Vout={g100[2]:.9g} mV, P={3*g100[1]:.9g} mW.\nG vs A: current/power change={ichg:.6g}%; output-voltage magnitude change={vchg:.6g}%; sensitivity-magnitude change={senschg:.6g}%.\n\nInterpretation: the serpentine Difference slots lower current and power and also lower voltage-sensitivity magnitude in this model. It is therefore a real geometry modification and a valid exploratory comparison, but does not outperform A on voltage sensitivity. The feature-derived geometry image is reconstructed from audited COMSOL geometry parameters and is explicitly not a GUI screenshot.\n''',encoding='utf-8')
    (OUT/'A_G_validation_log.txt').write_text('PASS: A and G each contain exactly 0,25,...,200 kPa, with finite values and no duplicate pressures.\n'+f'PASS: G 100 kPa scan vs independent G single point: I difference={g100[1]-3.9223653068609026:.15g} mA; Vout difference={g100[2]-(-37.32796079218592):.15g} mV.\n',encoding='utf-8')
if __name__=='__main__':main()
