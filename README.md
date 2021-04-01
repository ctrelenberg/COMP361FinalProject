## COMP361 Final Project

*By Christian Trelenberg (300110670), Michael Bennett (300142749), and Steven Waldock (300143567)*

### Installation

This application requires Pygame to run properly. For optimal results, run:

```
# Note: We have included a working virtual environment, for your convenience!
# It should work without any of these steps.
# If it doesn't, delete .env/ and try the following steps.
# It is necessary to activate the virtual environment by sourcing the `.env/bin/activate` file,
# or (on windows) using `.env/bin/Activate.ps1` or the batch file in the same directory.
python3 -m venv .env
. .env/bin/activate # Or use the batch file if on windows
pip3 install -r requirements.txt # This will install the necessary dependencies
```

Some algorithms may require modern versions of Python. Python 3.6 is recommended for optimal results. And fewer crashes.

### Running The Program

**NodeStar** is a program that allows users to try out different algorithms and visualize their runtime performance in real-time. It currently only supports graph-based algorithms, although it is possible to implement other algorithms within the environment. 

To test out an algorithm, left click to place some number of nodes, then click and drag between them to create edges. The edges have a weight added automatically. This allows for an optimal heuristic to be created.

To remove a node, click on it. To set a node as a start or end node (or to remove its status), right click on it.

Once a start and end node have been selected, an algorithm can be ran by selecting it from the left bar, then using any of the following buttons:

`Step` - This furthers algorithm execution by one stage, allowing the user to visually inspect the full algorithm progress/status indefinitely.

`Start` - This automatically runs the algorithm, at one stage executed per second. This delay allows the user to gain an instinctive understanding of which algorithms are faster.

`Stop` - This halts algorithm execution.

`Clear` - **This removes all nodes and edges and fully resets the application!**

`Reset` - This button resets algorithm execution, but all nodes, edges, and demarcations (start/end nodes) are preserved.