import com.comsol.model.*;
import com.comsol.model.util.*;
import java.io.*;
public class ExportSerpentineCurrentDensity {
 public static void main(String[] a){String r="D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24",mfile=r+"/COMSOL_Models/Pressure_Sensor_Serpentine_100kPa.mph",log=r+"/Simulation_Results/Serpentine_Design/current_density_export_log.txt",png=r+"/Figures/Serpentine_Design/G_current_density_100kPa.png";boolean c=false;PrintWriter o=null;
  try{o=new PrintWriter(new FileWriter(log));ModelUtil.connect("localhost",2036);c=true;Model m=ModelUtil.load("serp_j",mfile);o.println("DATASETS="+java.util.Arrays.toString(m.result().dataset().tags()));o.println("RESULTS="+java.util.Arrays.toString(m.result().tags()));
   m.result().create("pg_serp_j","PlotGroup2D");m.result("pg_serp_j").feature().create("surf_j","Surface");m.result("pg_serp_j").feature("surf_j").set("expr","ecs.normJ");
   m.result().export().create("img_serp_j","pg_serp_j","Image");m.result().export("img_serp_j").set("imagetype","png");m.result().export("img_serp_j").set("pngfilename",png);m.result().export("img_serp_j").set("width","1800");m.result().export("img_serp_j").set("height","1200");m.result().export("img_serp_j").set("resolution","200");m.result().export("img_serp_j").run();
   File f=new File(png);if(!f.isFile()||f.length()==0)throw new RuntimeException("empty image");o.println("SUCCESS png="+png+" bytes="+f.length());o.flush();ModelUtil.remove("serp_j");
  }catch(Exception e){if(o!=null){o.println("ERROR");e.printStackTrace(o);o.flush();}e.printStackTrace();System.exit(1);}finally{if(o!=null)o.close();if(c)try{ModelUtil.disconnect();}catch(Exception e){}}
 }
}
