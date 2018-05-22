using System;
using System.IO;
using AForge;
using AForge.Genetic;

namespace TSP
{
  // hlavna trieda programu obsahujuca staticku metodu Main, ktora sa pusta po starte
  public class TSP
  {
    // velkost populacie
    static private int POPULATION_SIZE = 40;

    // pocet iteracii genetickeho algoritmu
    static private int ITERATIONS = 100;

    // nastavenie metody selekcie
    // 0 = Elite selection
    // 1 = Rank selection
    // 2 = Roulette Wheel selection
    static private int SELECTION_METHOD = 0;

    // nastavenie krizenia 
    static private bool CROSSOVER = true;

    static private double[,] map = null;

    // hlavna metoda programu
    static void Main( string[] args) 
    {
      // otvorenie vstupneho suboru
      System.IO.StreamReader inputfile=new System.IO.StreamReader(args[0]);

      string line;
      int citycounter=0;

      while((line=inputfile.ReadLine())!= null)
      {
        if (line=="") citycounter++;
      }

      inputfile.Close();

      // deklarovanie pola koordinacii pre vsetky mesta
      map = new double[citycounter, 2];

      // otvorenie vstupneho suboru
      inputfile=new System.IO.StreamReader(args[0]);
      
      int city=0;
      line="yes";      

      while(true)
      {
        line=inputfile.ReadLine();
        if (line==null) break;
        map[city, 0]=System.Convert.ToDouble(line);
        line=inputfile.ReadLine();
        map[city, 1]=System.Convert.ToDouble(line);
        line=inputfile.ReadLine();
        city++;
      }

      inputfile.Close();

      // vytvorenie ohodnocovacej fitness funkcie
      TSPFitnessFunction fitnessFunction = new TSPFitnessFunction( map );

      // vytvorenie uvodnej populacie genetickeho algoritmu
      Population population = new Population( POPULATION_SIZE,
      ( CROSSOVER ) ? new TSPChromosome( map ) : new PermutationChromosome( citycounter ),
      fitnessFunction,
      ( SELECTION_METHOD == 0 ) ? (ISelectionMethod) new EliteSelection( ) :
      ( SELECTION_METHOD == 1 ) ? (ISelectionMethod) new RankSelection( ) :
      (ISelectionMethod) new RouletteWheelSelection( )
      );

      // poradove cislo iteracie
      int i = 1;

      // cyklus genetickeho algoritmu
      while ( true )
      {
        // prebehnutie jednej generacie
        population.RunEpoch( );

        // vypis fitness najlepsieho jedinca aktualnej generacie
        System.Console.WriteLine( System.Convert.ToInt32(fitnessFunction.PathLength( population.BestChromosome )).ToString( ));
        // inkrementacie premennej uchovavajucej poradove cislo generacie
        i++;

        // ukoncovacia podmienka
        // - dopredu znamy pocet opakovani
        if ( i > ITERATIONS ) 
          break;
      }
      string s=(string)fitnessFunction.Translate( population.BestChromosome );
      StringReader reader= new StringReader(s);
      line="yes";
      int from=0;
      int to=0;
      int first=0;

      System.IO.StreamWriter outputfile=new System.IO.StreamWriter(args[1]);
      
      outputfile.Write("<center><div id=\"canvas\" style=\"position:relative;width:700px;height:700px;background:white;float:center;\"></div></center><script type=\"text/JavaScript\">var canvasDiv=document.getElementById(\"canvas\");var gr = new jsGraphics(canvasDiv);var col = new jsColor(\"red\");var pen = new jsPen(col,1);var col2 = new jsColor(\"black\");");             

      line=reader.ReadLine();
      from=System.Convert.ToInt32(line);
      first=from;
      while(line!=null)
      {
        line=reader.ReadLine();
        to=System.Convert.ToInt32(line);
        if (line==null) to=first;
        outputfile.WriteLine("gr.drawLine(pen,new jsPoint("+map[from,0]+","+map[from,1]+"),new jsPoint("+map[to,0]+","+map[to,1]+"));");
        from=to;
      }

      for(int x=0;x<citycounter;x++)
      {
        outputfile.WriteLine("gr.fillCircle(col2,new jsPoint("+map[x,0]+","+map[x,1]+"),4);");
      }
      outputfile.Write("</script>");
      outputfile.Close();
    }
  }
}


















