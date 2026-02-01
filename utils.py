def safe_int(input):
    if input is not None:
        try:
            return int(input)
        except ValueError:
            return None
    else:
        return None