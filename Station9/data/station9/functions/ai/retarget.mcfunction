# idle on a node: route now. Otherwise the next node recomputes the route on arrival.
execute if score #hnext s9 matches ..-1 run function station9:ai/route
