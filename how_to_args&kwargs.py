"""
Example function and explanation on how to use args and kwargs.
"""


def myTestFunc(a: int, b: str, c: tuple, d=None, *args, **kwargs):
    """Test function to show how args and kwargs work
    in generall, a python functions can take 2-types of arguments: \n
    - positional arguments which are only declared by name (a, b, c,...) and have to be defined when the function is called,
    - or keyword-arguments with a default value e.g.: d=None
    keyword-arguments are optional, but when used always have to be defined by there name!
    e.g.: myTestFunc(1, "2", (0,0), d="like_this")
    positional arguments can also be defined by there name when the function is called!
    e.g. myTestFunc(a=1, b="2", c=(0,0))

    with the *args, and **kwargs parameters one can set up a function to except any number of either plain
    arguments (without a name!), or any number of additional keywordarguments.


    Parameters
    ----------
    a : int
        some positional argument... positional arguments are not given by name on the function call, BUT BY theire POSITION!
        it is important to order the inputs in the same way the function expects the inputs!
    b : str
        another positional argument
    c : tuple
        and another one...
    d : Any
        Optional Argument with default value set to None... (don't use mutable data as default value. numbers, are ok!)
    *args: list
        a list of additional arguments, not given a name by the function declaration. Expects a list of plain arguments
        e.g.: 5,6,78,...
    **kwargs: dict
        a dict of kewword arguments! {'one_thing':1,'second_thing':"test"}, or just directly some key-value pairs!
        e.g.: one_thing=1, second_thing="test",...
    """
    print(f'a: {a}, b: {b}, c: {c}, d: {d})')
    print(f'args: {[arg for arg in args]}')
    print(f'kwargs: {[(kwarg, val) for (kwarg, val) in kwargs.items()]}')
    # if using kwargs there are several ways to check for them:
    #    try & except blocks - if the kwarg is necessary
    #   (but then the kwarg should be given explict as name=defaultvalue!)
    try:
        myWantedArg = kwargs['what_i_want']
        print(myWantedArg['what_i_want'])
        # then continue with what ever you want to do e.g.
        #  check for the value or do something else..!
    except KeyError:
        # either except the error if there is a standard
        # to be set or the function can continue
        # or raise an exception here!
        print('the wanted name isnt in the kwargs dict!')

    # since kwargs should only be optional and not necessary best to check for them with
    # if else statement:
    if 'what_i_want' in kwargs.keys():  # !NOTICE: don't just use: "if kwargs["what_i_want"]:" since this will throw an error if the kwarg is not set!
        # do stuff here!
        print(f"What i want is : {kwargs['what_i_want']}")
    # continue since it is purely optional!

    #another option is to define a list with supported kwargs - to filter the given kwargs first and use them later
    supported_kwargs = ['inputs', 'outputs', 'name', 'trainable', 'skip_init']
    model_kwargs = {k: kwargs[k] for k in kwargs if k in supported_kwargs}
    other_kwargs = {k: kwargs[k] for k in kwargs if k not in supported_kwargs}

