namespace AjGa.Tsp
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel;
    using System.Linq;
    using System.Text;

    public class Tsp
    {
        public static void Main(string[] args)
        {
            short populationsize = 100;
            short noruns = 100;
            
            System.IO.StreamReader inputfile=new System.IO.StreamReader(args[0]);

            string line;
            string line2;
            int citycounter=0;

            while((line=inputfile.ReadLine())!= null)
            {
                if (line=="") citycounter++;
            }
            inputfile.Close();
            inputfile=new System.IO.StreamReader(args[0]);
      
            List<Position> positions = new List<Position>();
            Evaluator evaluator = new Evaluator(positions);
            int city=0;
            line="yes";  
            line2="yes";    
            while(city<citycounter)
            {
                line=inputfile.ReadLine();
                line2=inputfile.ReadLine();
                positions.Add(new Position(System.Convert.ToInt32(line), System.Convert.ToInt32(line2)));
                line=inputfile.ReadLine();
                city++;
            }

            inputfile.Close();
            

            Population population = new Population(populationsize, positions.Count);
            List<IGenomeFactory<int, int>> operators = new List<IGenomeFactory<int, int>>();

            for (int k = 0; k < 20 * populationsize / 100; k++)
            {
                operators.Add(new GradientMutator(evaluator));
            }

            for (int k = 0; k < 50 * populationsize / 100; k++)
            {
                operators.Add(new Mutator());
            }

            Evolution evolution = new Evolution(new Evaluator(positions), operators);
            
            Genome best=null;

            try
            {
                for (int n = 0; n < noruns; n++)
                {
                    Population newpopulation = (Population)evolution.RunGeneration(population);
                    best = (Genome)population.Genomes[0];
                    Console.WriteLine(best.Value.ToString());
                    population = newpopulation;
                }
                Position p1 = null;
                Position p2 =null;
                System.IO.StreamWriter outputfile=new System.IO.StreamWriter(args[1]);
      
                outputfile.Write("<center><div id=\"canvas\" style=\"position:relative;width:700px;height:700px;background:white;float:center;\"></div></center><script type=\"text/JavaScript\">var canvasDiv=document.getElementById(\"canvas\");var gr = new jsGraphics(canvasDiv);var col = new jsColor(\"red\");var pen = new jsPen(col,1);var col2 = new jsColor(\"black\");");

                foreach (int pos in best.Genes)
                {
                    if (p1 == null)
                    {
                        p1 = positions[pos];
                    }
                    else
                    {
                        p2 = positions[pos];
                        outputfile.WriteLine("gr.drawLine(pen,new jsPoint("+p1.X.ToString()+","+p1.Y.ToString()+"),new jsPoint("+p2.X.ToString()+","+p2.Y.ToString()+"));");
                        p1 = p2;
                    }
                }
                Position p0 = positions[best.Genes[0]];
                outputfile.WriteLine("gr.drawLine(pen,new jsPoint("+p2.X.ToString()+","+p2.Y.ToString()+"),new jsPoint("+p0.X.ToString()+","+p0.Y.ToString()+"));");
                foreach (Position position in positions)
                {
                    outputfile.WriteLine("gr.fillCircle(col2,new jsPoint("+position.X+","+position.Y+"),4);");
                }
                outputfile.WriteLine("</script>");
                outputfile.Close();
            }
            catch
            {
            }
        }
    }
}





