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
    forall(j in CIRCUITS where i != j /\ x_overlapping(i,j, width))( % Can also have 'less than', might have impact on search
      not y_overlapping(i, j, height) \/ not y_overlapping(i, j, width) \/ not x_overlapping(i,j, height) % changing input dir rotates the circuit
    )
  );

/*constraint % Ensure no overlap
  forall(i in CIRCUITS)(
    forall(j in CIRCUITS where i != j /\ y_overlapping(i,j, height))( % Can also have 'less than', might have impact on search
      not x_overlapping(i,j, width)
    )
  );
*/
% Objective function
solve minimize l;

%overlapping x-direction predicate
predicate x_overlapping(var int:i, var int:j, var int: dir) = 
   pos_x[i] + dims[i, dir] > pos_x[j] /\ pos_x[j] + dims[j, dir] > pos_x[i];
   
%overlapping y-direction predicate
predicate y_overlapping(var int:i, var int:j, var int: dir) = 
   pos_y[i] + dims[i, dir] > pos_y[j] /\ pos_y[j] + dims[j, dir] > pos_y[i];

output 
  ["\(w) \(l)\n"] ++
  ["\(n)\n"] ++
  [show(dims[i, width]) ++ " " ++ show(dims[i, height]) ++ " " ++ show(pos_x[i]) ++ " " ++ show(pos_y[i]) ++ "\n" | i in CIRCUITS];