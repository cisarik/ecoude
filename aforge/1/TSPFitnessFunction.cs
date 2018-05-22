using System;
using AForge.Genetic;

namespace TSP
{
  // trieda reprezentujuca fitness funkciu pre problem obchodneho cestujuceho
  public class TSPFitnessFunction : IFitnessFunction
  {
    private double[,]  map = null;

    public TSPFitnessFunction( double[,] map )
    {
      this.map = map;
    }

    // vyhodnocovacia funkcia chromozomu
    public double Evaluate( IChromosome chromosome )
    {
      return 1 / ( PathLength( chromosome ) + 1 );
    }

    // preklad genotypu na fenotyp
    public object Translate( IChromosome chromosome )
    {
      return chromosome.ToString( ).Replace(' ','\n');
    }

    // vypocitanie dlzky trasy, ktoru reprezentuje chromozom zadany ako parameter
    public double PathLength( IChromosome chromosome )
    {
      // deklarovanie premennej ktora urcuje trasu, ktoru musi prejst obchodnik
      ushort[] path = ((PermutationChromosome) chromosome).Value;

      // kontrola dlzky trasy
      if ( path.Length != map.GetLength( 0 ) )
      {
        throw new ArgumentException( "Neboli navstivene vsetky mesta!" );
      }

      // dlzky trasy
      int prev = path[0];
      int curr = path[path.Length - 1];
      

      // vzdialenost od posledneho mesta k zaciatku
      double  dx = map[curr, 0] - map[prev, 0];
      double  dy = map[curr, 1] - map[prev, 1];
      double  pathLength = Math.Sqrt( dx * dx + dy * dy );

      // vypocitanie celej vzdialenosti medzi prvym a poslednym navstivenym mestom
      for ( int i = 1, n = path.Length; i < n; i++ )
      {
        // aktualne mesto
        curr = path[i];

        // vypocitanie vzdialenosti
        dx = map[curr, 0] - map[prev, 0];
        dy = map[curr, 1] - map[prev, 1];
        pathLength += Math.Sqrt( dx * dx + dy * dy );

        // nastavenie sucasneho mesta ako predchadzajuceho
        prev = curr;
      }

      return pathLength;
    }
  }
}



