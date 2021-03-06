# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In each unit, if there are two boxes that share the same candidates of length 2, then it's known for sure that these two digits, call them digit X, Y, will occupy both boxes. The only unknown is which box gets assigned which digit. For every naked twins, there are two boxes, call them box A and box B. Let set A be the peers belonging to box A and set B be the peers beloning to box B. Set C is the set intersection of set A and set B. Now the constraint will propagate in set C by removing digit X and Y from the correponding candidates in each boxes in set C.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Two additional constriant units are added, the diagonal constriant and anti-diagonal constriant, which restrict the assignment along the unit to be a permutation of digits 1 to 9, without repeatition. The problem solving involves applying constriant propagation and backtracking recursively. First, the problem will be reduced by propagating the constriants in three ways. Eliminate: go through every box and if there is a box containing an complete assignment (with only 1 digit in its domain), this digit can be eliminated from the domains of its peers. Only Choice: go throught every box in each unit, if there is a digit that only appears once, the corresponding box is solved automatically. Naked Twins: as described in Q1 above. Next, the heuristic selects a box with the least number of available digits in its domain, this helps pruning the search tree early. After the constriant propagation step (reduce), the algorithm will check to see if there is a box with empty value, which implies an invalid solution. If there is an invalid step, return false and the caller will backtrack by trying another assignment. Recursively applying the recursive backtracking algorithm (constriant propagation + search) in a depth first search manner until the problem is solved.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

