

def path_level(path,delimiter='/'):
    """
        path level will return the remaining chartars of a string excluding a specific delimiter string.

        Example:
        path = '/1/2/3/'
        delimiter='/'

        level = path_level(path,delimiter)

        print("level:", level) 
        ## level: 3

    """
    return len(path) - path.count(delimiter)

