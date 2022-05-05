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

/*constraint % Ensure no overlap
  forall(i in CIRCUITS)(
    forall(j in CIRCUITS where i != j /\ x_overlapping(i,j))( % Can also have 'less than', might have impact on search
      not y_overlapping(i, j)
    )
  );

constraint % Ensure no overlap
  forall(i in CIRCUITS)(
    forall(j in CIRCUITS where i != j /\ y_overlapping(i,j))( % Can also have 'less than', might have impact on search
      not x_overlapping(i,j)
    )
  );*/
  
 constraint % Ensure no overlap
  forall(i in CIRCUITS)(
    forall(j in CIRCUITS where i != j)( % Can also have 'less than', might have impact on search
      not overlapping(i,j)
    )
  );
  
%implied constraint, no (pos_x, pos_y) can be the same
constraint
  forall(i in CIRCUITS)(
    alldifferent([pos_x[i], pos_y[i]]));

% Objective function
solve minimize l;

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
  [show(dims[i, width]) ++ " " ++ show(dims[i, height]) ++ " " ++ show(pos_x[i]) ++ " " ++ show(pos_y[i]) ++ "\n" | i in CIRCUITS];