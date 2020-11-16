### Instructions:
Included in this directory is a profiler wrapper which will allow you to gain more insight on how your code runs. The wrapper uses cProfile to profile your python script(s), and takes advantage of 2 open-source tools, Snakeviz and gprof2dot, to provide you with different visualiztions of profiling output. 

As with most python projects, I highly suggest using a virtual environment when installing any dependencies.

Building and running the wrapper is simple. Clone the repository, run `make` to install all python dependencies, and then use:
  - `./profile [filename] [optional_parameters]* ` to run your program.
  - As of 11/13/2020, the optional parameters include:
    - `snake` Interactive, detailed browser view of profiling data. Exit webserver by using Control-C in terminal when finished.
    - `simple` Generates a image visualiztion of profiling data.
  - Regardless of parameters, a detailed cProfile dumpfile will be generated and can be found in `profiling_dumps`

#### Dependencies:
  - see dependencies.txt for list of dependencies
  - graphviz in order to use gprof2dot. This can be installed with `brew install graphviz`. Additionally, you can choose not to use this visualization tool and take advantage of the other ones available in this wrapper.