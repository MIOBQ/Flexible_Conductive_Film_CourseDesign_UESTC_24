import com.comsol.model.*;
import com.comsol.model.physics.*;
import com.comsol.model.util.*;
import java.io.*;
import java.util.*;

/* First bounded G design: preserve r2 plus its Layers, then cut three alternating slots. */
public class BuildSerpentineGeometry {
  static String a(int[] x){return Arrays.toString(x);}
  static void log(PrintWriter o,String s){o.println(s);System.out.println(s);}
  static double[] xy(double x,double y) { // local r2 axes rotated -45 degrees about its center
    double t=-Math.PI/4.0; return new double[]{x*Math.cos(t)-y*Math.sin(t),x*Math.sin(t)+y*Math.cos(t)};
  }
  static void cutter(GeomFeatureList g,String tag,double x,double y,PrintWriter o) {
    double[] p=xy(x,y); GeomFeature f=g.create(tag,"Rectangle");
    f.set("base","center"); f.set("pos",new String[]{Double.toString(p[0]),Double.toString(p[1])});
    f.set("lx","2.5"); f.set("ly","16"); f.set("rot","-45");
    log(o,"CUTTER "+tag+" local_center_um=("+x+","+y+") global_center_um=("+p[0]+","+p[1]+") local_size_um=(2.5,16)");
  }
  static void ph(PrintWriter o,Model m,String phy,String tag){try{PhysicsFeature f=m.component("comp1").physics(phy).feature(tag);log(o,"PHYS "+phy+"/"+tag+"="+a(f.selection().entities()));}catch(Exception e){log(o,"PHYS "+phy+"/"+tag+" ERROR="+e.getClass().getSimpleName()+":"+e.getMessage());}}
  public static void main(String[] args) {
    String root="D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24";
    String source=root+"/COMSOL_Models/Pressure_Sensor_Original.mph";
    String target=root+"/COMSOL_Models/Pressure_Sensor_Serpentine_Exploratory.mph";
    File result=new File(root+"/Simulation_Results/Serpentine_Design"); result.mkdirs();
    PrintWriter o=null; boolean c=false;
    try {
      o=new PrintWriter(new OutputStreamWriter(new FileOutputStream(new File(result,"geometry_and_physics_validation.txt")),"UTF-8"),true);
      ModelUtil.connect("localhost",2036);c=true;
      Model m=ModelUtil.load("serpentine_G_build",source);
      GeomFeatureList g=m.component("comp1").geom("geom1").feature("wp1").geom().feature();
      log(o,"SOURCE="+source);log(o,"TARGET="+target);
      log(o,"DESIGN=retain Rectangle r2, its 11.25 um left/right Layers, and r2 endpoints; Difference removes three alternating central slots.");
      // r2 local spans x=-31.25..31.25, y=-10..10. Slots keep alternating 4 um bridges.
      cutter(g,"sgcut1",-14, 2,o); // top-to-near-bottom: lower bridge remains
      cutter(g,"sgcut2",  0,-2,o); // bottom-to-near-top: upper bridge remains
      cutter(g,"sgcut3", 14, 2,o); // second lower bridge
      GeomFeature dif=g.create("sgdif1","Difference");
      dif.selection("input").set(new String[]{"r2"});
      dif.selection("input2").set(new String[]{"sgcut1","sgcut2","sgcut3"});
      dif.set("keep","off");
      log(o,"DIFFERENCE input=[r2] input2=[sgcut1,sgcut2,sgcut3] keep=off");
      m.component("comp1").geom("geom1").run();
      log(o,"GEOMETRY_BUILD=SUCCESS");
      // Do not assume preserved entity numbers; report them for subsequent spatial verification.
      for(String t:new String[]{"mat1","mat2"}) log(o,"MATERIAL "+t+" domains="+a(m.component("comp1").material(t).selection().entities()));
      for(String t:new String[]{"cucn1","pzrm1","term1","term2","term3","gnd1"}) ph(o,m,"ecs",t);
      for(String t:new String[]{"fl1","fix1","fix2"}) ph(o,m,"shell",t);
      try {m.component("comp1").mesh("mesh1").run();log(o,"MESH_BUILD=SUCCESS");}
      catch(Exception me){log(o,"MESH_BUILD=ERROR "+me.getClass().getSimpleName()+":"+me.getMessage());throw me;}
      m.save(target);
      log(o,"SAVED="+target);log(o,"STATUS=SUCCESS_GEOMETRY_AND_MESH_ONLY");
      ModelUtil.remove("serpentine_G_build");
    } catch(Exception e) {if(o!=null){log(o,"STATUS=ERROR");e.printStackTrace(o);}e.printStackTrace();System.exit(1);}
    finally {if(o!=null)o.close();if(c)try{ModelUtil.disconnect();}catch(Exception e){}}
  }
}
