# This Repo is for 300K Interview

The problem description is in the [link](https://gist.github.com/z-hao-wang/5b1a1b360b57a3f4c725b990be0ced51)

For the sake of simplicity, I did not create a full python project, which would be something like this:

```shell
my_project/
├── my_project
│   ├── __init__.py
│   ├── main
│   │   ├── __init__.py
│   │   └── main.py
│   ├── moduleX.py
│   ├── package
├── resources
│   ├── data
│   │   └── example_data.csv
│   └── config
│       └── config.yaml
├── static
│   ├── css
│   │...
├── tests
│   ...
├── .gitignore
├── README.md
├── setup.py
└── requirements.txt
```

Instead, I only have a `calculate_std.py` file that includes all the method and a `tf-binance-BTC_ETH-2022-07-21.gz` given by the problem. After running the `calculate_std.py`, you are expected to get an `output.csv` file, as the final result.

I randomly selected 3 test case and the program passed the test.

## Solution description:

I spent about 40 min on the problem:

- 5 minutes searching and recalling what standard deviation is
- 20 minutes on coding, including searching for libraries and syntaxes.
- 15 minutes exploring any improvement for the task and denied some of them

I used a simple way to calculate the standard deviation: read the input file line by line, store the price, if the time passes 10 second, calculate a standard deviation and write it to the output file.

The overall time complexity would be $O(n)$, where $n$ is the number of rows in the input file.

### Some improvement I explored:

I tried to use multi-thread for this problem. My approach is create a thread and execute it every 100 second and thus I can calculate the standard deviation while reading the file.

Problem:

- The input file might not be fixed size, which means the file could be a infinite length stream data. In this case, it might be hard to calculate the bunch of the thread.
- The multi-thread method is actually costing longer time in this problem (7s). One possible explanation is the time to create and execute a thread is longer can calculating the standard deviation.
- Multi-thread cannot reserve order. I found the output of multi-thread method is different from the output of single-thread, this might be because threads are running asynchronously. If an ordered file is needed (highly possible), then we have to sort it, which also increase the time complexity.

I also asked ChatGPT about how to further increase the speed, here is the answer:

> To further increase the speed of the program, you can consider the following optimizations:
>
> 1. Use multiprocessing: Instead of using multi-threading, you can use the **`multiprocessing`** library, which allows you to create separate processes, each with its own interpreter and memory space. This can help bypass the Global Interpreter Lock (GIL) in Python and better utilize the available CPU cores.
> 2. Efficient data storage: Instead of storing prices as a list, you can use an efficient data structure such as a **`deque`** (double-ended queue) from the **`collections`** module. This allows for more efficient insertions and deletions when processing data in a sliding window.
> 3. Process data in larger chunks: Instead of processing data for every 10-second window separately, you can split the input file into larger chunks, each containing multiple 10-second windows. Each chunk can be processed by a separate worker in the multiprocessing pool. This can help in reducing the overhead of creating and managing multiple processes or threads.
> 4. Use a more efficient file format: Reading and parsing JSON data can be slow. If you have control over the input data format, you can consider using a more efficient file format like Parquet, which is designed for high-performance I/O operations.
> 5. Use a different Python interpreter: By default, Python uses the CPython interpreter, which has the GIL limitation. You can try using a different Python interpreter, such as PyPy, which is designed for better performance and can offer substantial speed improvements for certain workloads.

I let GPT to provide a version with the improvement mentioned above, the it ended up with longer time—9s.

The suggestion by GPT might be helpful when the database is large enough, but for the purpose of this question, the linear way is satisfactory. (0.87s)
