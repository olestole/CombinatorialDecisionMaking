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
array[CIRCUITS] of var lower_bound..upper_bound: pos_y;

array[CIRCUITS] of var 0..upper_bound+w*1000: pos = [pos_x[i]*1000+pos_y[i] | i in CIRCUITS];

% Objective variable
var 0..upper_bound: l;

constraint
  l = max(i in CIRCUITS)(
    pos_y[i] + dims[i, height]
  );

constraint % Ensure max width
  forall(i in CIRCUITS)(
    pos_x[i] + dims[i, width] <= w
  );
  
% Global constraint no overlap 
constraint diffn(pos_x, pos_y, dims[..,width], dims[..,height]);

%implied constraint, no (pos_x, pos_y) can be the same
constraint
    alldifferent(pos);
    
% Break symmetry vertically and horizontal flip    
constraint
    lex_lesseq(pos_x, [ pos_x[i] | i in reverse(CIRCUITS) ]) /\ lex_lesseq(pos_y, [ pos_y[i] | i in reverse(CIRCUITS) ]);

% Objective function
solve minimize l;

output 
  ["\(w) \(l)\n"] ++
  ["\(n)\n"] ++
  [show(dims[i, width]) ++ " " ++ show(dims[i, height]) ++ " " ++ show(pos_x[i]) ++ " " ++ show(pos_y[i]) ++ "\n" | i in CIRCUITS];