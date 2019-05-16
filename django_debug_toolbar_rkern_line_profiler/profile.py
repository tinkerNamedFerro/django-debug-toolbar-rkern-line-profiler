functions_to_profile = []


def line_profile(f):
    """The passed function will be included in the line profile displayed by
    the line profiler panel.

    Can be used either as a decorator or called directly as a function

        # Using it as a decorator
        @line_profile
        def profile_page(request):
            ...
            return render(request, 'profile_page.html')

        # Explicit argument
        line_profile(some_function)
    """
    functions_to_profile.append(f)
    return f
