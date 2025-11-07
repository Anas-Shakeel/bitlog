# Helper Functions for this application.


def create_page_range(total_pages: list[int], current_page: int, n: int):
    """
    ### Create Page Range
    Creates a page range from a given list.

    #### Assumptions:
    This method assumes that:
    - `total_pages` is a sorted list of numbers.
    - `total_pages` starts at 1
    - `total_pages` has no missing numbers
    - `n`: is an odd number (evens don't produce best results)

    #### ARGS:
    - `total_pages`: sorted list of pages (integers)
    - `current_page`: current page number
    - `n`: number of "numbers" to return (size of window)

    #### Example:
    ```
    >> array = [1, 2, 3, 4, 5, 6]
    >> create_page_range(array, current=4, n=3)
    [3, 4, 5]
    >>
    ```
    """
    last_page = total_pages[-1]
    first_page = total_pages[0]

    if n > last_page:
        return total_pages

    half_n = n // 2

    prev_page = current_page - half_n
    next_page = current_page + half_n

    # Resulting Range to Return
    new_range = None

    # CurrentPage is FirstPage?
    if current_page == first_page:
        new_range = total_pages[:n]
    elif current_page == last_page:
        new_range = total_pages[-n:]
    else:
        if (prev_page - 1) <= 0:
            new_range = total_pages[:n]
        elif next_page > last_page:
            new_range = total_pages[-n:]
        else:
            new_range = total_pages[prev_page - 1 : next_page]

    return new_range
