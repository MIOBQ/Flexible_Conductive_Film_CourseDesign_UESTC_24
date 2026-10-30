from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path('D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24')
FIG=ROOT/'Figures'/'Serpentine_Design'
A=Image.open(FIG/'A_original_COMSOL_geometry_local.png').convert('RGB')
G=Image.open(FIG/'G_serpentine_COMSOL_geometry_local.png').convert('RGB')

def font(size,bold=False):
    names=['C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf']
    for n in names:
        try:return ImageFont.truetype(n,size)
        except OSError:pass
    return ImageFont.load_default()

# Preserve every pixel of each supplied COMSOL screenshot. Only surrounding layout is added.
margin=50; gap=44; header=135; footer=180
w=A.width+G.width+gap+2*margin; h=max(A.height,G.height)+header+footer
out=Image.new('RGB',(w,h),'white');d=ImageDraw.Draw(out)
d.text((margin,26),'A/G Geometry Comparison',fill='#111111',font=font(38,True))
d.text((margin,80),'Original COMSOL Geometry Graphics screenshots; panel pixels are unmodified.',fill='#333333',font=font(21))
ay=header+(max(A.height,G.height)-A.height)//2; gy=header+(max(A.height,G.height)-G.height)//2
ax=margin; gx=margin+A.width+gap
out.paste(A,(ax,ay));out.paste(G,(gx,gy))
d.rectangle((ax-2,ay-2,ax+A.width+1,ay+A.height+1),outline='#222222',width=3)
d.rectangle((gx-2,gy-2,gx+G.width+1,gy+G.height+1),outline='#222222',width=3)
d.text((ax,header-37),'A: Original geometry',fill='#111111',font=font(27,True))
d.text((gx,header-37),'G: Serpentine geometry',fill='#111111',font=font(27,True))
y=h-footer+22
d.text((margin,y),'A: original r2 straight/X-shaped conductive structure.',fill='#111111',font=font(22))
d.text((margin,y+38),'G: r2 retains the original end Layers and has three alternating 2.5 x 16 um Difference slots.',fill='#111111',font=font(22))
d.text((margin,y+78),'Note: different displayed axis extents are retained from the original COMSOL screenshots; no rescaling or geometric alteration was applied.',fill='#555555',font=font(18))
out.save(FIG/'A_G_geometry_comparison.png',dpi=(300,300))
