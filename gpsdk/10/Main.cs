using System;

using GP;

namespace SantaFe
{
    public class SantaFe
    {
  private const int ITERATIONS = 50;
  private const int POPULATION_SIZE = 500;
  private const int MAX_ELEMENTS_COUNT = 64;
  private const int MAX_ELEMENT_INPUTS_OUTPUTS_COUNT = 3;
  private const int MAX_ANT_LENGTH=3;
  private const double MUTATION=0.8;
  private const double CROSSOVER=0.1;

        public int[,] map = new int[33, 34];//mapa
        public int[,] mapp = new int[33, 34];//mapa vyuzita pri testovani fitnes
        WGPControl control;

        int kroku = 400;
        int lastnam;

        public double fit(Explorer ex)
        {
            //zakladni fitness funkce
            int[,] tmap = new int[33, 34];
            Array.Copy(map, tmap, 33 * 34);
           
            int nkr = kroku;//citac poctu kroku
            double i = 0;

            fitc(ex,0);//orez hlubokyc vetvi
            ex = ex.ToRoot();
            lastnam = 0;

            Mravenec mr = new Mravenec(2, 2, 1);
            //smicka behu programu
            while (true)
            {
                if (nkr <= 0)
                    break;
                i += fitt(ex, mr, tmap, ref nkr);//pripocti fitness
                ex = ex.ToRoot();//ziskej koren stromu
            }
            return 90 - i - (lastnam+5) / 8000f/*- ex.Chro.WebLen(0)/1250*/;
        }
        public void fitc(Explorer ex,int det)
        {
            int c = ex.GetNFunc();
            if (c == 0)
                return;
            if (det > 6)
            {
                ex.Delete();//smeze vetev kdyz je hlubsi jak 6
                return;
            }
            if (c==2)
            {
                fitc(ex.GetNextChildren(),det+1);
                fitc(ex.GetNextChildren(), det + 1);
            }
            if (c==3)
            {
                fitc(ex.GetNextChildren(), det + 1);
                fitc(ex.GetNextChildren(), det + 1);
                fitc(ex.GetNextChildren(), det + 1);
            }

        }

        public double fitt(Explorer ex, Mravenec mr, int[,] tmap, ref int nkr)
        {
            //uzceni fitness
            if (nkr == 0)//kontrola ujdetych kroku
                return 0;
            int c = ex.GetNFunc();//zjisteny arity
            int f = ex.GetFunc();//funkce
            if (c <= 1)//arita mensi jak 2
            {
                nkr--;//odecteni poctu kroku
                f = f % 3;
                if (0 == f)//go
                {
                    mr.Go();
                    if (!mr.InMap())
                        return 0;
                    mapp[mr.X, mr.Y] = 1;
                    
                    if (tmap[mr.X, mr.Y] == 1)
                    {
                        tmap[mr.X, mr.Y] = 0;
                        lastnam = nkr;
                        return 1;
                    }
                }
                if (f == 1)//right
                {
                    mr.GoRight();
                }
                if (f == 2)//left
                {
                    mr.GoLeft();
                }
            }

            if (c == 2)
            {
                f = f % 2;
                if (f == 0)
                {
                    double bf =  fitt(ex.GetNextChildren(), mr, tmap, ref nkr) + fitt(ex.GetNextChildren(), mr, tmap, ref nkr);
                    return bf;
                }
                if (f == 1)
                {
                    mr.GoB();

                    if (mr.InMap() && tmap[mr.XB, mr.YB] == 1)
                    {
                        return fitt(ex.GetNextChildren(), mr, tmap, ref nkr)+0.00000000000000000000000001;
                    }
                    else
                    {
                        ex.GetNextChildren();
                        return fitt(ex.GetNextChildren(), mr, tmap, ref nkr)+0.00000000000000000000000001;
                    }
                }
            }
            if (c == 3)
            {
                return fitt(ex.GetNextChildren(), mr, tmap, ref nkr) + fitt(ex.GetNextChildren(), mr, tmap, ref nkr) + fitt(ex.GetNextChildren(), mr, tmap, ref nkr);
            }
            return 0;
        }


  public void Run(string[] args)
  {
    kroku = 400;
            control = new WGPControl(POPULATION_SIZE, fit);
            Chromozom.TermPrefer = new int[3];
            Chromozom.TermPrefer[0] = 0;
            Chromozom.TermPrefer[1] = 8;
            Chromozom.TermPrefer[2] = 12;

  // otvorenie vstupneho suboru
    System.IO.StreamReader inputfile=new System.IO.StreamReader(args[0]);
    string line="yes"; 
    string line2="yes";
    string line3="yes";
    int x=0;
    int y=0;
    while(true)
    {
      line=inputfile.ReadLine();
      if (line==null) break;
      line2=inputfile.ReadLine();
      if (line2==null) break;
      line3=inputfile.ReadLine();
      x=System.Convert.ToInt32(line);
      y=System.Convert.ToInt32(line2);
      map[x,y]=1;
    }
    inputfile.Close();

  control.StartRun(MAX_ELEMENTS_COUNT,MAX_ELEMENT_INPUTS_OUTPUTS_COUNT,MAX_ANT_LENGTH);
  for(int i=0;i<ITERATIONS;i++)
  {
  control.StepRun(MUTATION, CROSSOVER);
  System.Console.WriteLine(System.Convert.ToInt32(control.Chro[0].Fitness).ToString());
  }
        
   
    System.IO.StreamWriter outputfile=new System.IO.StreamWriter(args[1]);
    
    outputfile.WriteLine("<center><div id=\"canvas\" style=\"position:relative;width:700px;height:700px;background:white;\"></div>");
outputfile.WriteLine("<form>");
    outputfile.WriteLine("<input type=\"button\" value=\"Go!\" style=\"float:center\" onclick=\"Start()\"></form></center>");
outputfile.WriteLine("<script type=\"text/JavaScript\">var canvasDiv=document.getElementById(\"canvas\");var gr = new jsGraphics(canvasDiv);var ie=false;var col = new jsColor(\"black\");var pen = new jsPen(col,1);var steps=10;");
outputfile.WriteLine("var map = new Array(33);");
outputfile.WriteLine("var i=0;");
outputfile.WriteLine("for (i = 0; i < map.length; i++)");
outputfile.WriteLine("{");
outputfile.WriteLine("map [i] = new Array(33);");
outputfile.WriteLine("}");
outputfile.WriteLine("var j=0;");
outputfile.WriteLine("for (i = 0; i < map.length; i++)");
outputfile.WriteLine("{");
outputfile.WriteLine("for (j = 0; j < map[i].length; j++)");
outputfile.WriteLine("{");
outputfile.WriteLine("map[i][j]=0;");
outputfile.WriteLine("}");
outputfile.WriteLine("}");  
    
for (int u = 0; u < 33; u++)
for (int v = 0; v < 34; v++)
{
if (map[u, v] == 1) outputfile.WriteLine("map["+u+"]["+v+"]=1");
}
    
outputfile.WriteLine("for (i = 0; i < map.length; i++)");
outputfile.WriteLine("{");
outputfile.WriteLine("for (j = 0; j < map[i].length; j++)");
outputfile.WriteLine("{");
outputfile.WriteLine("if (map[i][j]==1)");
outputfile.WriteLine("{");
outputfile.WriteLine("map[i][j]=gr.fillRectangle(new jsColor(\"red\"),new jsPoint(26+i*20,26+j*20),9,9);");
outputfile.WriteLine("}");
outputfile.WriteLine("}");
outputfile.WriteLine("}");
outputfile.WriteLine("var direction=0;");
outputfile.WriteLine("var posX=0;");
outputfile.WriteLine("var posY=0;");
outputfile.WriteLine("var x=0;");
outputfile.WriteLine("for(x=0;x<34;x++)");
outputfile.WriteLine("{");
outputfile.WriteLine("gr.drawLine(pen,new jsPoint(x*20+20,20),new jsPoint(x*20+20,700));");
outputfile.WriteLine("}");
outputfile.WriteLine("var y=0;");
outputfile.WriteLine("for(y=0;y<35;y++)");
outputfile.WriteLine("{");
outputfile.WriteLine("gr.drawLine(pen,new jsPoint(20,20+y*20),new jsPoint(680,20+y*20));");
outputfile.WriteLine("}");
outputfile.WriteLine("canvasDiv.onmousemove = getMouseXY;");
outputfile.WriteLine("canvasDiv.onclick=putAnt;");
outputfile.WriteLine("if(document.all)");
outputfile.WriteLine("ie=true;");
outputfile.WriteLine("if (!ie)");
outputfile.WriteLine("{");
outputfile.WriteLine("canvasDiv.captureEvents(Event.MOUSEMOVE)");
outputfile.WriteLine("canvasDiv.captureEvents(Event.CLICK)");
outputfile.WriteLine("}");
outputfile.WriteLine("var mouseX = 0");
outputfile.WriteLine("var mouseY = 0");
outputfile.WriteLine("function getMouseXY(e)");
outputfile.WriteLine("{");
outputfile.WriteLine("if (ie)");
outputfile.WriteLine("{");
outputfile.WriteLine("mouseX = event.clientX + document.body.parentElement.scrollLeft;");
outputfile.WriteLine("mouseY = event.clientY + document.body.parentElement.scrollTop;");
outputfile.WriteLine("} else {");
outputfile.WriteLine("mouseX = e.pageX");
outputfile.WriteLine("mouseY = e.pageY");
outputfile.WriteLine("}");
outputfile.WriteLine("if (mouseX < 0){mouseX = 0}");
outputfile.WriteLine("if (mouseY < 0){mouseY = 0}");
outputfile.WriteLine("mouseX =mouseX - canvasDiv.offsetLeft;");
outputfile.WriteLine("mouseY =mouseY - canvasDiv.offsetTop;");
outputfile.WriteLine("return true;");
outputfile.WriteLine("}");
outputfile.WriteLine("function Go()");
outputfile.WriteLine("{");
outputfile.WriteLine("gr.fillCircle(new jsColor(\"black\"), new jsPoint(31+posX*20,31+posY*20), 3);");
outputfile.WriteLine("if (direction==0)//doprava");
outputfile.WriteLine("{");
outputfile.WriteLine("if (posX==32)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=1;");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("{");
outputfile.WriteLine("steps=steps-1;");                     
outputfile.WriteLine("posX+=1;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant0.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");                  
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==1)//dolava");
outputfile.WriteLine("{");
outputfile.WriteLine("if (posX==1)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=0;");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("{");  
outputfile.WriteLine("steps=steps-1;");                     
outputfile.WriteLine("posX-=1;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant1.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("}");                   
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==2)//hore");
outputfile.WriteLine("{");
outputfile.WriteLine("if (posY==1)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=3;");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("{");
outputfile.WriteLine("steps=steps-1;");                     
outputfile.WriteLine("posY-=1;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant2.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("}");                     
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==3)//dole");
outputfile.WriteLine("{");
outputfile.WriteLine("if (posY==32)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=2;");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("{");    
outputfile.WriteLine("steps=steps-1;");                    
outputfile.WriteLine("posY+=1;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant3.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("}");                     
outputfile.WriteLine("if (map[posX][posY]!=0)");
outputfile.WriteLine("{");
outputfile.WriteLine("canvasDiv.removeChild(map[posX][posY]);");
outputfile.WriteLine("}");
outputfile.WriteLine("}");
outputfile.WriteLine("function Right()");
outputfile.WriteLine("{");
outputfile.WriteLine("if (direction==0)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=3;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant3.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==1)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=2;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant2.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==2)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=0;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant0.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==3)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=1;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant1.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("}");
outputfile.WriteLine("function Food()");
outputfile.WriteLine("{");
outputfile.WriteLine("if (direction==0)");
outputfile.WriteLine("{");
outputfile.WriteLine("if (map[posX+1][posY]!=0) return true;");
outputfile.WriteLine("else return false;");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==1)");
outputfile.WriteLine("{");
outputfile.WriteLine("if (map[posX-1][posY]!=0) return true;");
outputfile.WriteLine("else return false;");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==2)");
outputfile.WriteLine("{");
outputfile.WriteLine("if (map[posX][posY-1]!=0) return true;");
outputfile.WriteLine("else return false;");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==3)");
outputfile.WriteLine("{");
outputfile.WriteLine("if (map[posX][posY+1]!=0) return true;");
outputfile.WriteLine("else return false;");
outputfile.WriteLine("}");
outputfile.WriteLine("}");
outputfile.WriteLine("function Left()");
outputfile.WriteLine("{");
outputfile.WriteLine("if (direction==0)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=2;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant2.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==1)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=3;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant3.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==2)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=1;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant1.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==3)");
outputfile.WriteLine("{");
outputfile.WriteLine("direction=0;");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant0.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("}");
outputfile.WriteLine("function Start()");
outputfile.WriteLine("{");
outputfile.WriteLine("steps=1000;");
outputfile.WriteLine("while (steps>0){");
                     
Explorer ex = control.Chro[0].GetExplorer();
outputfile.WriteLine(fittp(ex,""));
                     
outputfile.WriteLine("}");                     
outputfile.WriteLine("}");
outputfile.WriteLine("function putAnt()");
outputfile.WriteLine("{");
outputfile.WriteLine("try{");
outputfile.WriteLine("if(AntDiv)");
outputfile.WriteLine("canvasDiv.removeChild(AntDiv);}");
outputfile.WriteLine("catch(e){}");
outputfile.WriteLine("var x=Math.round(parseInt(mouseX/20)-1);");
outputfile.WriteLine("var y=Math.round(parseInt(mouseY/20)-1);");
outputfile.WriteLine("if ((x<0) || (x>33) || (y<0) || (y>34))");
outputfile.WriteLine("{");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("{");
outputfile.WriteLine("posX=x;");
outputfile.WriteLine("posY=y;");
outputfile.WriteLine("if (direction==0)");
outputfile.WriteLine("{");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant0.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==1)");
outputfile.WriteLine("{");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant1.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==2)");
outputfile.WriteLine("{");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant2.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("else");
outputfile.WriteLine("if (direction==3)");
outputfile.WriteLine("{");
outputfile.WriteLine("AntDiv=gr.drawImage(\"http://dl.dropbox.com/u/2902284/ant3.gif\", new jsPoint(22+posX*20,21+posY*20),18,18);");
outputfile.WriteLine("}");
outputfile.WriteLine("}");
outputfile.WriteLine("}");
outputfile.WriteLine("</script>");
outputfile.Close();                   
                     
  }

        public static void Main(string[] args)
        {
            new SantaFe().Run(args);
  }

        public string fittp(Explorer ex, string m)
        {

            string s = m;
            
            int c = ex.GetNFunc();
            int f = ex.GetFunc();

            if (c <= 1)
            {
               
                f = f % 3;
                if (0 == f)
                {
                    s += "Go();\n";
                }
                if (f == 1)
                {
                    s += "Right();\n";
                }
                if (f == 2)
                {
                    s += "Left();\n";
                }
            }

            if (c == 2)
            {
                f = f % 2;
                if (f == 0)
                {
                    s +="{\n"+fittp(ex.GetNextChildren(),m+"   ") + fittp(ex.GetNextChildren(),m+"   ")+"}\n";
          
                    return s;
                }
                if (f == 1)
                {
                    s += "if(Food())\n"+m+"{\n" + fittp(ex.GetNextChildren(), m + "   ") +m+"}\n"+m+"else\n"+m+"{\n" + fittp(ex.GetNextChildren(), m + "   ") +m+ "}\n";
                }
            }
            if (c == 3)
            {
                s += "{\n" + fittp(ex.GetNextChildren(), m + "   ") + fittp(ex.GetNextChildren(), m + "   ")+ fittp(ex.GetNextChildren(), m + "   ") +m+ "}\n";
            }
            return s;
        }
    }

    public class Mravenec
    {
        public int X, Y, Smer, XB, YB;//0-nahoru 1 - doprava 2-dolu 3-doleva
        public int Score;
        public Mravenec(int x, int y, int s)
        {
            X = x;
            Y = y;
            Smer = s;
        }

        public bool InMap()
        {
            if (X < 0)
                return false;
            if (X > 32)
                return false;
            if (Y < 0)
                return false;
            if (Y > 33)
                return false;

            if (XB < 0)
                return false;
            if (XB > 32)
                return false;
            if (YB < 0)
                return false;
            if (YB > 33)
                return false;
            return true;

        }
        public void GoB()
        {
            XB = X;
            YB = Y;

            switch (Smer)
            {
                case 0:
                    YB--;
                    break;
                case 1:
                    XB++;
                    break;
                case 2:
                    YB++;
                    break;
                case 3:
                    XB--;
                    break;
                default:
                    break;
            }
        }

        public void Go()
        {
            switch (Smer)
            {
                case 0:
                    Y--;
                    break;
                case 1:
                    X++;
                    break;
                case 2:
                    Y++;
                    break;
                case 3:
                    X--;
                    break;
                default:
                    break;
            }

        }
        public void GoLeft()
        {
            Smer--;
            if (Smer < 0)
                Smer = 3;
        }
        public void GoRight()
        {
            Smer++;
            if (Smer > 3)
                Smer = 0;
        }

    }

}
























