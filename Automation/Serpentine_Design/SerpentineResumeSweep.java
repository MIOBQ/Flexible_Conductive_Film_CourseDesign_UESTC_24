import com.comsol.model.*;
import com.comsol.model.util.*;
import java.io.*;
import java.util.*;
public class SerpentineResumeSweep {
 public static void main(String[] a)throws Exception{
  String r="D:/Github_codes/Flexible_Conductive_Film_CourseDesign_UESTC_24", p=r+"/COMSOL_Models/Pressure_Sensor_Serpentine_Exploratory.mph", q=r+"/COMSOL_Models/Pressure_Sensor_Serpentine_Sweep.mph", d=r+"/Simulation_Results/Serpentine_Design";
  new File(d).mkdirs(); TreeMap<Integer,String>x=new TreeMap<Integer,String>(); File c=new File(d,"serpentine_pressure_sweep.csv");
  if(c.exists()){BufferedReader b=new BufferedReader(new FileReader(c));b.readLine();String s;while((s=b.readLine())!=null&&!s.trim().equals(""))x.put(Integer.parseInt(s.split(",")[0]),s);b.close();}
  PrintWriter l=new PrintWriter(new FileWriter(new File(d,"serpentine_pressure_sweep_solver_log.txt"),true)); boolean connected=false;
  try{ModelUtil.connect("localhost",2036);connected=true;Model m=ModelUtil.load("serpentine_scan",p);m.save(q);boolean z=m.study("std1").feature("param").isActive();m.study("std1").feature("param").active(false);
   for(String u:a){int k=Integer.parseInt(u);if(x.containsKey(k)){l.println("SKIP,"+k);l.flush();continue;}m.param().set("p1",k+"[kPa]");l.println("START,"+k);l.flush();
    try{m.study("std1").run();String t="evs"+k;m.result().numerical().create(t,"EvalGlobal");m.result().numerical(t).set("expr",new String[]{"ecs.I0_1","ecs.V0_2-ecs.V0_3"});double[][]v=m.result().numerical(t).getReal();double i=v[0][v[0].length-1]*1e3,w=v[1][v[1].length-1]*1e3;if(Double.isNaN(i)||Double.isInfinite(i)||Double.isNaN(w)||Double.isInfinite(w))throw new RuntimeException("Nonfinite result");x.put(k,k+","+i+","+w+","+(3*i));PrintWriter zc=new PrintWriter(new FileWriter(c));zc.println("pressure_kPa,current_mA,voltage_mV,power_mW");for(String e:x.values())zc.println(e);zc.close();l.println("OK,"+x.get(k));l.flush();}
    catch(Exception e){l.println("ERROR,"+k+","+e.getClass().getName()+","+e.getMessage());l.flush();throw e;}
   }m.study("std1").feature("param").active(z);m.save(q);
  }finally{l.close();if(connected)try{ModelUtil.disconnect();}catch(Exception e){}}
 }
}
