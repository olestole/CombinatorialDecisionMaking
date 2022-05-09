include "globals.mzn";

int: w;
int: n;

int: width = 1;
int: height = 2;

set of int: CIRCUITS = 1..n;
array[CIRCUITS, 1..2] of int: dims;


int: upper_bound = sum(i in CIRCUITS)(dims[i, height]);

array[CIRCUITS] of var 0..w: pos_x; % Could let w = w - 1, since we're zero-indexing.
array[CIRCUITS] of var 0..upper_bound: pos_y;
array[1..w] of var 0..n: lower_x_row;
array[1..upper_bound] of var 0..n: left_y_row; % Problem. Pos_y can be upper

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

 constraint % Ensure no overlap
  forall(i in CIRCUITS)(
    forall(j in CIRCUITS where i != j)( % Can also have 'less than', might have impact on search
      not overlapping(i,j)
    )
  );
/*
% Break symmetry vertically
constraint forall (c in 1..n, i in 1..w) (( pos_y[c]=0 /\ pos_x[c]=i ) <-> (lower_x_row[i]=c));

constraint
    lex_lesseq(lower_x_row, [ lower_x_row[i] | i in reverse(1..n) ]);

% Break symmetry horizontally
constraint forall (c in 1..n, i in 1..l) (( pos_x[c]=0 /\ pos_y[c]=i ) <-> (left_y_row[i]=c)); % Problem: has to be length upperbound

constraint
    lex_lesseq(left_y_row, [ left_y_row[i] | i in reverse(1..n) ]);
*/    
constraint
    lex_lesseq(pos_x, [ pos_x[i] | i in reverse(CIRCUITS) ]) /\ lex_lesseq(pos_y, [ pos_y[i] | i in reverse(CIRCUITS) ]);
 
/*constraint
    lex_lesseq(pos_y, [ pos_y[i] | i in reverse(CIRCUITS) ]);*/

% Objective function
solve minimize l;

% constraint l=8;
% solve satisfy;

%overlapping x-direction predicate
predicate x_overlapping(var int:i, var int:j) = 
   pos_x[i] + dims[i, width] > pos_x[j] /\ pos_x[j] + dims[j, width] > pos_x[i];
   
%overlapping y-direction predicate
predicate y_overlapping(var int:i, var int:j) = 
   pos_y[i] + dims[i, height] > pos_y[j] /\ pos_y[j] + dims[j, height] > pos_y[i];
   
predicate overlapping(var int:i, var int:j) = 
   x_overlapping(i, j) /\ y_overlapping(i, j);

output 
  ["\(w) \(l)\n"] ++
  ["\(n)\n"] ++
  [show(dims[i, width]) ++ " " ++ show(dims[i, height]) ++ " " ++ show(pos_x[i]) ++ " " ++ show(pos_y[i]) ++ "\n" | i in CIRCUITS] ++
  [show(pos_x) ++ "\n" ] ++
  [show(pos_y)];