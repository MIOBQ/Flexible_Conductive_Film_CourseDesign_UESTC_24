import com.comsol.model.*;
import com.comsol.model.physics.*;
import com.comsol.model.util.*;
import java.io.*;
import java.util.*;

public class AuditOriginalGeometry {
  static String arr(String[] x) { return Arrays.toString(x); }
  static String arr(int[] x) { return Arrays.toString(x); }
  static void line(PrintWriter out, String s) { out.println(s); System.out.println(s); }
  static void props(PrintWriter out, String prefix, GeomFeature f) {
    line(out, prefix+" tag="+f.tag()+" type="+f.getType()+" label="+f.label());
    for (String p : f.properties()) {
      try { line(out, prefix+" PROP "+p+"="+f.getString(p)); }
      catch (Exception e1) {
        try { line(out, prefix+" PROP "+p+"="+arr(f.getStringArray(p))); }
        catch (Exception e2) { line(out, prefix+" PROP "+p+"=<unreadable>"); }
      }
    }
  }
  static void phys(PrintWriter out, Model m, String phy, String tag) {
    try {
      PhysicsFeature f=m.component("comp1").physics(phy).feature(tag);
      line(out,"PHYSICS "+phy+"/"+tag+" type="+f.getType()+" entities="+arr(f.selection().entities()));
      for(String p:f.properties()) {
        try { line(out,"PHYSICS_PROP "+phy+"/"+tag+" "+p+"="+f.getString(p)); }
        catch(Exception e) { }
      }
    } catch(Exception e) { line(out,"PHYSICS "+phy+"/"+tag+" ERROR="+e.getClass().getSimpleName()+":"+e.getMessage()); }
  }
  public static void main(String[] args) {
    String root="D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24";
    File outdir=new File(root+"/Simulation_Results/Serpentine_Design"); outdir.mkdirs();
    boolean connected=false;
    PrintWriter out=null;
    try {
      out=new PrintWriter(new OutputStreamWriter(new FileOutputStream(new File(outdir,"original_geometry_audit.txt")),"UTF-8"),true);
      ModelUtil.connect("localhost",2036); connected=true;
      Model m=ModelUtil.load("serpentine_audit_A",root+"/COMSOL_Models/Pressure_Sensor_Original.mph");
      line(out,"AUDIT_MODEL="+m.label());
      line(out,"GEOM_TOP_TAGS="+arr(m.component("comp1").geom("geom1").feature().tags()));
      GeomFeature wp=m.component("comp1").geom("geom1").feature("wp1");
      line(out,"WP1_TYPE="+wp.getType()+" WP1_CHILD_TAGS="+arr(wp.geom().feature().tags()));
      for(String t:wp.geom().feature().tags()) props(out,"WP_FEATURE",wp.geom().feature(t));
      for(String t:m.component("comp1").geom("geom1").feature().tags()) {
        if(!t.equals("wp1")) props(out,"GEOM_FEATURE",m.component("comp1").geom("geom1").feature(t));
      }
      for(String t:m.component("comp1").material().tags()) {
        Material mat=m.component("comp1").material(t);
        line(out,"MATERIAL tag="+t+" label="+mat.label()+" domains="+arr(mat.selection().entities()));
      }
      line(out,"PHYSICS_TAGS="+arr(m.component("comp1").physics().tags()));
      for(String t:new String[]{"cucn1","pzrm1","term1","term2","term3","gnd1"}) phys(out,m,"ecs",t);
      for(String t:new String[]{"fl1","fix1","fix2"}) phys(out,m,"shell",t);
      try { line(out,"MULTIPHYSICS_TAGS="+arr(m.multiphysics().tags())); } catch(Exception e) { line(out,"MULTIPHYSICS_ERROR="+e.getMessage()); }
      try { line(out,"SYS2_TYPE="+m.component("comp1").coordSystem("sys2").getType()+" LABEL="+m.component("comp1").coordSystem("sys2").label()); } catch(Exception e) { line(out,"SYS2_ERROR="+e.getMessage()); }
      line(out,"PARAMETERS:");
      for(String p:m.param().varnames()) line(out,"PARAM "+p+"="+m.param().get(p));
      line(out,"STATUS=SUCCESS_READ_ONLY");
      ModelUtil.remove("serpentine_audit_A");
    } catch(Exception e) {
      e.printStackTrace();
      System.exit(1);
    } finally { if(out!=null) out.close(); if(connected) try {ModelUtil.disconnect();}catch(Exception e){} }
  }
}
