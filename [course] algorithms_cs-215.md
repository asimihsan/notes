# Algorithms (CS-215) on Udacity

## Student

[Asim Ihsan](http://www.asimihsan.com)

## Unit 1: A Social Network Magic Trick

### 1.3: Eulerian Path

-    **Eulerian path**: Path that traverses through all edges once in a connected graph.
-    **Eulerian tour**: Eulerian path that starts and ends at the same node.

### 1.4: Algorithms are Cool

        def algorithm_Development(problem_spec):
            correct = False
            while not correct or not fast_enough:
                algorithm = devise_algorithm(problem_spec)
                correct = analyze_correctness(algorithm)
                running_time = analyse_efficiency(algorithm)
            return algorithm
            
### 1.6: Correctness

-    e.g. naive(a,b) = a*b.
-    *Claim*: Before or after "while" loop

        ab = xy + z
        
-    *Base case*: First time through, x=a, y=b, z=0

        ab = ab + 0
        
-    *Inductive step*
    -    If ab = xy + z before
    -    Then ab = x'y' + z' after.
    
            x' = x - 1
            y' = y
            z' = z + y
            
            x'y' + z' = (x-1)(y) + (z+y)
                      = xy-y + z + y
                      = xy + z
                      = ab
                      
-    So we know that the claim is true. So?
-    What happens when x = 0 at the end?
-    ab = z, the return value.
-    QED.

### 1.8: Russian Peasant's Algorithm

-    aka Ancient Egyptian multiplication

        def russian(a, b):
            x = a
            y = b
            z = 0
            while x > 0:
                if x % 2 == 1:
                    z = z + y
                y = y << 1
                x = x >> 1
            return z
            
        e.g. russian(14, 11), should = 154
        
        x    y    z
        14   11   0
        7    22   22
        3    44   66
        1    88   154
        0    176  154
        
### 1.10: Correctness

-    Claim:

            ab = xy + z
            
-    Base case: true, same as naive.
-    Inductive step: if ab = xy + z holds at start then ab = x'y' + z'. 
  

      
