# Linux Program Specification


## Objective
Develop a program for the Linux operating system.

The program should be executed under Python and efficiently utilize processor time (on each core), performing input/output operations and metric calculations.


### Requirements:
1. **Multiprocessing:**
    - Use Python `socket` and `multiprocessing` libs to solve described problem.
    - **Master Process:**
      + Aggregates information collected from all workers.
      + Computes and writes metrics based on the received data to a file at intervals of 10 seconds and 60 seconds.
    - Worker Process:
      + Should accept UDP messages in JSON format on a port with a specific number (see structure below).


### Input Message Format:
```json
{
    "A1": "<integer>",
    "A2": "<integer>",
    "A3": "<integer>"
}
```


### File Writing Format:
```json
{
    "timestamp": "<time stamp in seconds>",
    "count_type": "<'10s' or '60s' - indicating whether the record is for 10 or 60 seconds, respectively>",
    "A1_sum": "<sum of A1 values for the count_type interval>",
    "A2_max": "<maximum value of A2 for the count_type interval>",
    "A3_min": "<minimum value of A3 for the count_type interval>"
}
```

Assuming messages were received in the first 10 seconds:
```json
{"A1": 1, "A2": 10, "A3": 100}
{"A1": 2, "A2": 12, "A3": 102}
{"A1": 3, "A2": 30, "A3": 130}
```

And the next 10 seconds:
```json
{"A1": 4, "A2": 20, "A3": 200}
{"A1": 5, "A2": 13, "A3": 103}
{"A1": 6, "A2": 40, "A3": 140}
```

The resulting file would look like:
```json
{"timestamp": 123456710, "count_type": "10s", "A1_sum": 6, "A2_max": 30, "A3_min": 100}
{"timestamp": 123456720, "count_type": "10s", "A1_sum": 15, "A2_max": 40, "A3_min": 103}
{"timestamp": 123456730, "count_type": "10s", "A1_sum": 0, "A2_max": 0, "A3_min": 0}
{"timestamp": 123456740, "count_type": "10s", "A1_sum": 0, "A2_max": 0, "A3_min": 0}
{"timestamp": 123456750, "count_type": "10s", "A1_sum": 0, "A2_max": 0, "A3_min": 0}
{"timestamp": 123456760, "count_type": "10s", "A1_sum": 0, "A2_max": 0, "A3_min": 0}
{"timestamp": 123456760, "count_type": "60s", "A1_sum": 21, "A2_max": 40, "A3_min": 100}
```


### Submission:
- Implement the project according to the `PEP8` standard.
- Commit style, [click](https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/). Commits should contain small logical portions of the code being modified. A clear commit name is required, descriptions within commits are welcome. The commit header should be up to 50 characters and the description up to 72 characters, [read more](https://stackoverflow.com/questions/2290016/git-commit-messages-50-72-formatting).
- Branch style, [click](https://medium.com/@patrickporto/4-branching-workflows-for-git-30d0aaee7bf#:~:text=own%20development%20cycle.-,Git%20Flow,-The%20Git%20Flow). It is suggested to use GitFlow. Don't forget to delete merged or close branches based on PR status. Development should be done in separate branches, it is not allowed to commit or merge changes directly into _master_ or _develop_.
- Submit the codebase along with a detailed README explaining how to set up and run the monolithic application, any additional features implemented, and any challenges faced. [Here is](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) a good cheat-list how to style documentation.
- Fork this repository and do your development there.


### Note:
- Use Python 3.10 or above.
- Feel free to use any additional libraries or tools you find suitable for the task.
- Try decomposing tasks into chunks and branches as described above.
- All `highlighted` words should be read in the documentation or familiarized with what they are.
- Follow best practices in terms of code readability, structure, and documentation.


### Proposed project structure:
```
.
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── process.py
│   └── utils.py
├── README.md
└── task.md
```
