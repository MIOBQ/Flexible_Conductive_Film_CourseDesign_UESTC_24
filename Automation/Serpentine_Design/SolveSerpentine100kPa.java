import com.comsol.model.*;
import com.comsol.model.util.*;
import java.io.*;

public class SolveSerpentine100kPa {
  public static void main(String[] a) {
    String r="D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24";
    String source=r+"/COMSOL_Models/Pressure_Sensor_Serpentine_Exploratory.mph";
    String target=r+"/COMSOL_Models/Pressure_Sensor_Serpentine_100kPa.mph";
    String log=r+"/Simulation_Results/Serpentine_Design/serpentine_100kPa_validation.txt";
    boolean c=false; PrintWriter o=null;
    try {
      o=new PrintWriter(new FileWriter(log));
      ModelUtil.connect("localhost",2036);c=true;
      Model m=ModelUtil.load("serpentine_100kPa",source);
      m.save(target); // preserve the geometry-only exploratory model before solving
      m.param().set("p1","100[kPa]");
      boolean active=m.study("std1").feature("param").isActive();
      m.study("std1").feature("param").active(false);
      o.println("SETTINGS p1=100[kPa], term1_V0="+m.component("comp1").physics("ecs").feature("term1").getString("V0"));
      o.println("START_STATIONARY"); o.flush();
      m.study("std1").run();
      m.result().numerical().create("ev_serp100","EvalGlobal");
      m.result().numerical("ev_serp100").set("expr",new String[]{"ecs.I0_1","ecs.V0_2-ecs.V0_3"});
      double[][] v=m.result().numerical("ev_serp100").getReal();
      double i=v[0][v[0].length-1]*1e3, u=v[1][v[1].length-1]*1e3;
      if(Double.isNaN(i)||Double.isInfinite(i)||Double.isNaN(u)||Double.isInfinite(u)) throw new RuntimeException("Non-finite electrical result");
      o.println("OK current_mA="+i);o.println("OK voltage_mV="+u);o.println("OK power_mW="+(3*i));
      m.study("std1").feature("param").active(active);
      m.save(target);o.println("SAVED="+target);o.println("STATUS=SUCCESS");o.flush();
      ModelUtil.remove("serpentine_100kPa");
    } catch(Exception e) { if(o!=null){o.println("STATUS=ERROR");e.printStackTrace(o);o.flush();} e.printStackTrace();System.exit(1); }
    finally {if(o!=null)o.close();if(c)try{ModelUtil.disconnect();}catch(Exception e){}}
  }
}
