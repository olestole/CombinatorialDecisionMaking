include "globals.mzn";

int: w;
int: n;

int: width = 1;
int: height = 2;

set of int: CIRCUITS = 1..n;
array[CIRCUITS, 1..2] of int: dims;

int: upper_bound = sum(i in CIRCUITS)(dims[i, height]);

%lower_bound
array[CIRCUITS] of int: sorted_heights = sort(dims[.., height]);
int: n_rows = ceil((sum(i in CIRCUITS)(dims[i, width])) / w);
set of int: number_of_rows = 1..n_rows;
int: lower_bound = sum(i in number_of_rows)(sorted_heights[i]);


array[CIRCUITS] of var 0..w: pos_x; % Could let w = w - 1, since we're zero-indexing.
array[CIRCUITS] of var 0..upper_bound: pos_y;
array[CIRCUITS] of var 0..1: rotation;

% Objective variable
var lower_bound..upper_bound: l;

constraint
  l = max(i in CIRCUITS)(
    pos_y[i] + dims[i, 2-rotation[i]]
  );

constraint % Ensure max width
  forall(i in CIRCUITS)(
    pos_x[i] + dims[i, rotation[i]+1] <= w
  );

% Global constraint no overlap 
constraint diffn(pos_x, pos_y, [ dims[i, rotation[i]+1] | i in CIRCUITS ], [ dims[i, 2-rotation[i]] | i in CIRCUITS ]);
    
% Break symmetry vertically and horizontal flip  
constraint
  lex_lesseq(pos_x, [ pos_x[i] | i in reverse(CIRCUITS) ]) /\ lex_lesseq(pos_y, [ pos_y[i] | i in reverse(CIRCUITS) ]);

% Break symmetry of flipping squares  
constraint
  forall(i in CIRCUITS)
    (dims[i, width]=dims[i, height] -> rotation[i] = 0);
    
% Objective function
solve minimize l;

output 
  ["\(w) \(l)\n"] ++
  ["\(n)\n"] ++
  [show(dims[i, rotation[i]+1]) ++ " " ++ show(dims[i, 2-rotation[i]]) ++ " " ++ show(pos_x[i]) ++ " " ++ show(pos_y[i]) ++ "\n" | i in CIRCUITS]++ 
  [show(rotation[i]) ++ " " | i in CIRCUITS]; 