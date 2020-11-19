
def fun(arg1: int) -> str:  # comment
    """AI is creating summary for fun

    :param arg1: [description]
    :type arg1: int
    :raises FileExistsError: [description]
    :return: [description]
    :rtype: str
    """
    if arg1 > 1:
        raise FileExistsError() # comment

    return "abc" # comment
