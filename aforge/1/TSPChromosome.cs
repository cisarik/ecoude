using System;
using AForge.Genetic;

namespace TSP
{
  // trieda reprezentujuca jeden chromozom problemu obchodneho cestujuceho
  public class TSPChromosome : PermutationChromosome
  {
    private double[,] map = null;

    public TSPChromosome( double[,] map ) : base( map.GetLength( 0 ) )
    {
      this.map = map;
    }

    protected TSPChromosome( TSPChromosome source ) : base( source )
    {
      this.map = source.map;
    }

  
    public override IChromosome CreateNew( )
    {
      return new TSPChromosome( map );
    }

    public override IChromosome Clone( )
    {
      return new TSPChromosome( this );
    }

    // nastavenie metody krizenia
    public override void Crossover( IChromosome pair )
    {
      TSPChromosome p = (TSPChromosome) pair;

      // kontrola spravnosti paru
      if ( ( p != null ) && ( p.length == length ) )
      {
        ushort[] child1 = new ushort[length];
        ushort[] child2 = new ushort[length];

        // vytvorenie dvoch potomkov
        CreateChildUsingCrossover( this.val, p.val, child1 );
        CreateChildUsingCrossover( p.val, this.val, child2 );

        // nahradenie rodicov potomkami
        this.val  = child1;
        p.val    = child2;
      }
    }

    // metoda vytvarajuca noveho potomka aplikovanim krizenia na dvoch rodicov
    private void CreateChildUsingCrossover( ushort[] parent1, ushort[] parent2, ushort[] child )
    {
      // deklarovanie pomocneho pola urcujuceho ci konkretny gen nie je aj v potomkovi
      bool[]  geneIsBusy = new bool[length];

      // deklarovanie predchadzajuceho gen potomka a dalsich dvaja kandidatov krizenia
      ushort  prev, next1, next2;

      // deklarovanie logickych premennych urcujucich ci su obaja kandidati krizenia vhodny 
      bool valid1, valid2;

      int j, k = length - 1;

      // prvy gen potomka je druhy gen rodica
      prev = child[0] = parent2[0];
      geneIsBusy[prev] = true;

      // cyklus na ziskanie vsetkych genov rodica
      for ( int i = 1; i < length; i++ )
      {
        // cyklus, ktory najde prvy gen po krizeni v rodicovi cislo 1
        for ( j = 0; j < k; j++ )
        {
          if ( parent1[j] == prev )
            break;
        }
        next1 = ( j == k ) ? parent1[0] : parent1[j + 1];

        // cyklus, ktory najde prvy gen po krizeni v rodicovi cislo 2
        for ( j = 0; j < k; j++ )
        {
          if ( parent2[j] == prev )
            break;
        }
        next2 = ( j == k ) ? parent2[0] : parent2[j + 1];

        // kontrola korektnosti genov
        valid1 = !geneIsBusy[next1];
        valid2 = !geneIsBusy[next2];

        // vyber genov
        if ( valid1 && valid2 )
        {
          // obaja kandidati su korektny takze vyberame jedno najblizsie mesto
          double dx1 = map[next1, 0] - map[prev, 0];
          double dy1 = map[next1, 1] - map[prev, 1];
          double dx2 = map[next2, 0] - map[prev, 0];
          double dy2 = map[next2, 1] - map[prev, 1];

          prev = ( Math.Sqrt( dx1 * dx1 + dy1 * dy1 ) < Math.Sqrt( dx2 * dx2 + dy2 * dy2 ) ) ? next1 : next2; 
        }
        else if ( !( valid1 || valid2 ) )
        {
          // ani jeden z kandidatov nie je korektny na krizenie, teda vyberame nahodny gen,
          // ktory este nie je v potomkovi
          int r = j = rand.Next( length );

          while ( ( r < length ) && ( geneIsBusy[r] == true ) )
            r++;
          if ( r == length )
          {
            r = j - 1;
            while ( geneIsBusy[r] == true )  
              r--;
          }
          prev = (ushort) r;
        }
        else
        {
          // jeden z kandidatov je vhodny
          prev = ( valid1 ) ? next1 : next2;
        }

        child[i] = prev;
        geneIsBusy[prev] = true;
      }
    }
  }
}


