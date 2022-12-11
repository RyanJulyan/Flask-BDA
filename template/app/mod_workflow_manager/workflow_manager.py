from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence, Union
from functools import wraps, partial
import inspect

import asyncio
from concurrent.futures import ThreadPoolExecutor


class to_async:
    def __init__(self, *, executor: Optional[ThreadPoolExecutor] = None):

        self.executor = executor

    def __call__(self, blocking):
        @wraps(blocking)
        async def wrapper(*args, **kwargs):

            loop = asyncio.get_event_loop()
            if not self.executor:
                self.executor = ThreadPoolExecutor()

            func = partial(blocking, *args, **kwargs)

            return await loop.run_in_executor(self.executor, func)

        return wrapper


@dataclass
class Task(ABC):
    def __getattribute__(self, name: str):
        attr = object.__getattribute__(self, name)
        if callable(attr) and (
            (name == "run")
            and (not inspect.isawaitable(attr))
            and (not asyncio.iscoroutinefunction(attr))
        ):

            @to_async(executor=None)
            def async_func(func, *args, **kwargs):
                return func(*args, **kwargs)

            def func(*args, **kwargs):
                result = async_func(attr, *args, **kwargs)
                return result

            return func
        return attr

    @abstractmethod
    def run(self, *args, **kwargs):
        """Abstract method to Run the Task! Must be included for consistency"""
        pass


class WorkflowManager:
    def __init__(self, tasks: Sequence[Union[callable, Task]] = None):
        if tasks is None:
            tasks = []
        self.tasks: Sequence[Union[callable, Task]] = tasks

    def add_task(self, task):
        self.tasks.append(task)

    async def run(self):
        for task in self.tasks:
            if str(type(task)).__contains__("function"):
                await task()
            else:
                await task.run()

    async def run_from(self, task_index: int):
        for task in self.tasks[task_index:]:
            if str(type(task)).__contains__("function"):
                await task()
            else:
                await task.run()

    def process(self):
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(self.run())
        return results

    def process_from(self, task_index: int):
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(self.run_from(task_index))
        return results


if __name__ == "__main__":
    # Sample usage
    class ExampleTask(Task):
        def run(self, *args, **kwargs):
            print("ExampleTask run")

    async def task1():
        print("Executing task 1")

    async def task2():
        print("Executing task 2")

    async def task3():
        print("Executing task 3")

    wf_manager = WorkflowManager([task1])
    wf_manager.add_task(task1)
    wf_manager.add_task(task2)
    wf_manager.add_task(task3)
    wf_manager.add_task(ExampleTask())
    print()
    print("wf_manager.process:")
    wf_manager.process()
    print()
    print()
    print("wf_manager.process_from:")
    wf_manager.process_from(2)
    print()
