import inspect
from typing import Dict, Sequence


class PrePostHooks:
    """A class that lets you register pre and post hooks onto a method of a class.
    You can create a function and then register the function.

    """

    def __init__(self):
        """Register the dictionary for methods and callable pre and post hooks.
        The add_pre_hook method is used to create a logger on every method of the child
        Class this means every class uses the pre hook as a way to log out what was called
        """
        self.pre_hooks: Dict[str, callable] = {}
        self.post_hooks: Dict[str, callable] = {}

        methods = [func for func in self.__class__.__dict__.values() if callable(func)]
        for method in methods:
            # Add a logger pre-hook for each method
            self.add_pre_hook(method.__name__, self.logger)

    def logger(self, *args, **kwargs):
        print(
            f"Called method {self.__class__.__name__}.{inspect.stack()[2].code_context[0].strip()}"
        )

    def add_pre_hook(self, method_name: str, hook_func: callable):
        """Add a callable function to a named function that will run before a method

        Args:
            method_name (str): the name of the function to add the function to
            hook_func (callable): the callable function to call
        """
        if method_name not in self.pre_hooks:
            self.pre_hooks[method_name]: Sequence = []
        self.pre_hooks[method_name].append(hook_func)

    def add_post_hook(self, method_name: str, hook_func: callable):
        """Add a callable function to a named function that will run after a method

        Args:
            method_name (str): the name of the function to add the function to
            hook_func (callable): the callable function to call
        """
        if method_name not in self.post_hooks:
            self.post_hooks[method_name]: Sequence = []
        self.post_hooks[method_name].append(hook_func)

    def __getattribute__(self, name: str):
        """get and return a specific attribute with pre and post hooks

        Args:
            name (str): the name of the method being called

        Returns:
            _type_: runs the called attribute
        """
        attr = object.__getattribute__(self, name)
        if callable(attr) and ((name in self.pre_hooks) or (name in self.post_hooks)):

            def hooks(*args, **kwargs):
                """Run all the pre hooks registered against the attribute name,
                then run the attribute, then run all the post hooks registered against
                the attribute name

                Returns:
                    _type_: the originally requested attribute
                """
                for hook in self.pre_hooks.get(name, []):
                    hook(*args, **kwargs)
                result = attr(*args, **kwargs)
                for hook in self.post_hooks.get(name, []):
                    hook(*args, **kwargs)
                return result

            return hooks
        return attr


if __name__ == "__main__":

    class MyClass(PrePostHooks):
        def __init__(self):
            super().__init__()
            self.data = {}

        def add_data(self, key, value):
            self.data[key] = value
            self.print_data()

        def print_data(self):
            print(self.data)

    my_obj = MyClass()

    # Add pre-hook that logs the arguments passed to the add_data method
    def pre_hooks(key, value):
        print(f"Additional function pre_hooks")

    def log_args(key, value):
        print(f"Pre Hook Called add_data with arguments: key:{key} value:{value}")

    my_obj.add_pre_hook("add_data", pre_hooks)
    my_obj.add_pre_hook("add_data", log_args)

    # Add post-hook that logs the data after it's added
    def log_data(key, value):
        print(f"Post Hook Added data: {key} {value}")

    my_obj.add_post_hook("add_data", log_data)

    # Call add_data and print_data methods
    my_obj.add_data("foo", "bar")
    # my_obj.print_data()
