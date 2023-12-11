### Background
I'm hosting a secret santa event online where participants get to specify what type of gifts they want to gift and receive (i.e. Art, Writing etc) and I wanted to find the optimal set of allocations to maximize "happiness" (i.e. maximise the intersection between "what the sender wants to send" and "what the receiver wants to receive"). 

I have approached a similar optimisation problem (the [**Eight Queens Problem**](https://en.wikipedia.org/wiki/Eight_queens_puzzle)) using  [**Local Search**](https://en.wikipedia.org/wiki/Local_search_(optimization)) in university, and wanted to see how well it would work for my secret santa use case! 

Local search involves iteratively trying to apply *local changes* (in my case, making the best swap of recipients given a randomly selected person) to try and improve the current solution. This is good for problems with a very large amount of possible arrangements (like this one!) because it allows for an optimal solution to be found most of the time without needing to try all possible arrangements. To maximise the probability of arriving at an optimal solution, my random search allocator will perform local search multiple times and select the best set of allocations.

### Sample Use Case
```py
users = [  
    User("foo", can_give=("art", "writing"), can_receive=("art",)),  
    User("baz", can_give=("writing",), can_receive=("writing",)),  
    User("qux", can_give=("art", "writing", "music"), can_receive=("art", "writing", "music")),  
    User("quux", can_give=("art", "music"), can_receive=("art",)),  
]  
  
lsa = LocalSearchAllocator(steps=500, max_options=5, n=3)  
allocations = lsa.allocate(users)
```

### Future Work
- add support for turning excel / csv files of participant preferences into `User` objects for allocator input
- make an abstract base class `Allocator` and add other Allocator classes for different methods of optimizing allocations (i.e. not just local search)
- make a pretty UI
