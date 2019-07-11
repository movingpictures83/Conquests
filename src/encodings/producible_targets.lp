% inputs from the met_net
% reaction(R).
% reactant(M,R).
% product(M,R).
% seed(M).
% initial_target(M).


% what is producible by all reactions

  pscope(M) :- seed(M).

  pscope(M) :- product(M,R), reaction(R,N), pscope(M2) : reactant(M2,R).

  pscope(M) :- reactant(M,R), reaction(R,N), reversible(R), pscope(M2) : product(M2,R).


% show interesting predicates

  target(M) :- initial_target(M), pscope(M).


%Display
#show target/1.


