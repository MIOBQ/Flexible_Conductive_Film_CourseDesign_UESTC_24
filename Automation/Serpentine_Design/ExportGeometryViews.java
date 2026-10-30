import com.comsol.model.*;
import com.comsol.model.util.*;
import java.io.*;

public class ExportGeometryViews {
  static final String ROOT="D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24";
  static void export(Model m,String tag,String file) throws Exception {
    m.result().create(tag,"PlotGroup2D");
    m.result(tag).feature().create("geom","Geometry");
    m.result().export().create("img_"+tag,tag,"Image");
    m.result().export("img_"+tag).set("imagetype","png");
    m.result().export("img_"+tag).set("pngfilename",file);
    m.result().export("img_"+tag).set("width","2200");
    m.result().export("img_"+tag).set("height","1600");
    m.result().export("img_"+tag).set("resolution","200");
    m.result().export("img_"+tag).run();
    if(!new File(file).isFile()||new File(file).length()==0) throw new RuntimeException("Empty export: "+file);
    System.out.println("EXPORTED="+file);
  }
  public static void main(String[] a){boolean c=false;try{new File(ROOT+"/Figures/Serpentine_Design").mkdirs();ModelUtil.connect("localhost",2036);c=true;
    Model A=ModelUtil.load("serp_geo_A",ROOT+"/COMSOL_Models/Pressure_Sensor_Original.mph");
    export(A,"pg_serp_A",ROOT+"/Figures/Serpentine_Design/A_original_geometry.png");ModelUtil.remove("serp_geo_A");
    Model G=ModelUtil.load("serp_geo_G",ROOT+"/COMSOL_Models/Pressure_Sensor_Serpentine_Exploratory.mph");
    export(G,"pg_serp_G",ROOT+"/Figures/Serpentine_Design/G_serpentine_geometry.png");ModelUtil.remove("serp_geo_G");
    System.out.println("STATUS=SUCCESS");
  }catch(Exception e){System.out.println("STATUS=ERROR");e.printStackTrace(System.out);System.exit(1);}finally{if(c)try{ModelUtil.disconnect();}catch(Exception e){}}}
}
