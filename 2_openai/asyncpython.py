import asyncio
import time

async def taskA():
    print("taskA started")
    await asyncio.sleep(3)  # simulate API call delay
    print("taskA finished")
    return "A done"

async def taskB():
    print("taskB started and finished immediately")
    return "B done"

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(taskA(), taskB())
    end = time.perf_counter()
    print("Total time:", round(end - start, 2), "s")
    print(results)

asyncio.run(main())

"""
- When `.run(main())` is called, `asyncio` creates a new event loop
- Internally:
    1. Create a new event loop `loop = asyncio.new_event_loop()`
    2. Register and run main() `loop.run_until_complete(main())`
    3. Run until completion, loop will keep switching between `main`, `taskA`, `taskB`
    4. Close and clean up `loop.close()`
- When `main()` starts running, it calls `gather`.
- `gather` create coroutine objects for both `taskA` and `taskB`
- The event loop starts the tasks in order, first task takes control
- When the task in control hits `await`, it yields control to the event loop
- Event loop gives control to other ready tasks while the task is waiting, to leverage the waiting time
- When all tasks are finished, `gather` will return a list of outputs to `main`.
- `main` prints results and finishes.
- Loop is closed and cleaned
"""