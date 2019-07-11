%metabolite(M) :- seed(M).
%metabolite(M) :- target(M).
%metabolite(M) :- product(M,N).
%metabolite(M) :- reactant(M,N).


% Accessibility 
scope(M,N) :- seed(M), draft(N).
scope(M,N) :- seed(M), subgraph(N).
scope(M,N) :- product(M,R), reaction(R,N), scope(M2,N) : reactant(M2,R).
scope(M,N) :- reactant(M,R), reaction(R,N), reversible(R), scope(M2,N) : product(M2,R).

%definition 2 characteristic crossroads 
defcross(M) :- scope(M,N), reaction(R,N), reactant(M,R), draft(N), not seed(M), not target(M).
defcross(M) :- scope(M,N), reaction(R,N), product(M,R), reversible(R), draft(N), not seed(M), not target(M).
%defcross(M) :- scope(M,N), reaction(R,N), reactant(M,R), N=="repairnet", not seed(M), not target(M).
%defcross(M) :- scope(M,N), reaction(R,N), product(M,R), reversible(R), N=="repairnet", not seed(M), not target(M).


metabolite(M) :- reactant(M,_), not target(M), not seed(M).
metabolite(M) :- product(M,_), not target(M), not seed(M).

subgraph(M) :- metabolite(M).
reaction(R,M) :- subgraph(M), reaction(R,N), not reactant(M,R), not reversible(R).
reaction(R,M) :- subgraph(M), reaction(R,N), not reactant(M,R), reversible(R), not product(M,R).
defgraph(M) :- target(T), subgraph(M), not scope(T,M), draft(N).
subtarget(T,C) :- target(T), crossroad(C), subgraph(C), not scope(T,C), draft(N).

crossroad(M) :- defcross(M), defgraph(M).

%Display
#show subtarget/2.
#show crossroad/1.
