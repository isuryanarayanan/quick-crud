def to_url(string):
    """
    This function transforms a string to url format

    Example:
    to_url("Introduction to Deep Learning")

    "Introduction%20to%20Deep%20Learning"
    """

    return "%20".join(string.split(" "))