""" Quick Guide using numpystyle Docstrings with pydoc!
    numpydocstring guide: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html

    Generate with "pdoc --html packagename"

    Expand Source Code if you are looking at the html version of this file.
"""

# when writing a function use type-hints: otional annotations in function signature to annotate what data Type is expected!
from typing import Any, Optional, Union
# see more at: https://docs.python.org/3.9/library/typing.html#module-typing


def function(parameter: Any, example: Union[int, float], keyword_argument_with_default: int = 0,
             complete_optional_arg: Optional[int] = None):
    """ Description of the Function.

    Make sure there is a linebreak between each section.
    Sections below are optional. If there are input parameters at least fill the Parameters section.

    .. todo:: Update this tutorial if you are missing something important.

    Parameters
    ----------
    parameter : datatype (further datatype desciptions, e.g. shape, optional, ...)
        Parameter description
    example : int, float
        second summand
    keyword_argument_with_default: int
        an optional arguement with a default value - hince it MUST have a not None value!
    complete_optional_arg: int
        an Argument that can be a None-type value
    old_param : np.array, shape=(10,2) # .. deprecated:: not sure if this should be done this way

    Returns
    -------
    result : datatype
        description of result

    Examples
    --------
    >>> function(2, 3)
    5

    """
    result = parameter + example
    return result