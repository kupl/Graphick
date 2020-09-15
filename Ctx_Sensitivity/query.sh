#!/bin/bash
 
  bloxbatch -db doop/last-analysis -query CandidateHeap2obj | sort > CandidateHeap2obj.facts
  python process.py CandidateHeap2obj.facts > doop/CanHeap2obj.facts

  bloxbatch -db doop/last-analysis -query CandidateHeap2type | sort > CandidateHeap2type.facts
  python process.py CandidateHeap2type.facts > doop/CanHeap2type.facts
 
  bloxbatch -db doop/last-analysis -query CandidateHeap1type | sort > CandidateHeap1type.facts
  python process.py CandidateHeap1type.facts > doop/CanHeap1type.facts
  
