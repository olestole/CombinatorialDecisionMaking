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

array[CIRCUITS] of var 0..upper_bound+w*1000: pos = [pos_x[i]*1000+pos_y[i] | i in CIRCUITS];

% Objective variable
var lower_bound..upper_bound: l;

constraint
  l = max(i in CIRCUITS)(
    pos_y[i] + dims[i, 2-rotation[i]]
  );

constraint % Ensure max width
  forall(i in CIRCUITS)(
    pos_x[i] + dims[i, width] <= w
  );
  
  
%implied constraint, no (pos_x, pos_y) can be the same
constraint
  alldifferent(pos);

constraint % Ensure no overlap
  forall(i in CIRCUITS)(
    forall(j in CIRCUITS where i < j)(
      (not overlapping(i, j) /\ rotation[j] = 0) \/ (not overlapping(i, j) /\ rotation[j]=1) % changing input dir rotates the circuit
    )
  );

% Objective function
solve minimize l;

%overlapping x-direction predicate
predicate x_overlapping(var int:i, var int:j) = 
   pos_x[i] + dims[i, rotation[i]+1] > pos_x[j] /\ pos_x[j] + dims[j, rotation[j]+1] > pos_x[i];
   
%overlapping y-direction predicate
predicate y_overlapping(var int:i, var int:j) = 
   pos_y[i] + dims[i, 2-rotation[i]] > pos_y[j] /\ pos_y[j] + dims[j, 2-rotation[j]] > pos_y[i];
   
predicate overlapping(var int:i, var int:j) = 
   x_overlapping(i, j) /\ y_overlapping(i, j);
   
output 
  ["\(w) \(l)\n"] ++
  ["\(n)\n"] ++
  [show(dims[i, rotation[i]+1]) ++ " " ++ show(dims[i, 2-rotation[i]]) ++ " " ++ show(pos_x[i]) ++ " " ++ show(pos_y[i]) ++ "\n" | i in CIRCUITS]++ 
  [show(rotation[i]) ++ " " | i in CIRCUITS];