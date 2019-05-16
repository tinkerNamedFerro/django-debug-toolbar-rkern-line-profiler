Django Debug Toolbar Line Profile Panel (rkern)
===============================================

This is a profiling panel for [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar)
that uses [rkern/line_profiler](https://github.com/rkern/line_profiler).

This package work slightly differently from [dmclain/django-debug-toolbar-line-profiler](https://github.com/dmclain/django-debug-toolbar-line-profiler)
which tries line profile the executed view function by default.

This package instead requires you to mark the function you'd like line profile
with the decorator `@line_profile`.

This makes it easy to line profile functions that are nested deeply in your
codebase. 

Installation
------------

Since there's a problem with the latest version fo `line_profiler` (v2.1.1),
you should first install `line_profiler` (and Cython) like this:

    pip install Cython git+https://github.com/rkern/line_profiler.git

(See: <https://github.com/rkern/line_profiler/issues/127>)

Then install this package:

    pip install git+https://github.com/peergradeio/django-debug-toolbar-rkern-line-profiler.git

In your Django settings you need to add `django_debug_toolbar_rkern_line_profiler`
to `INSTALLED_APPS` and add `django_debug_toolbar_rkern_line_profiler.panels.LineProfilerPanel`
to `DEBUG_TOOLBAR_PANELS`


        # settings.py
        INSTALLED_APPS = [
            ...
            'debug_toolbar',
            'django_debug_toolbar_rkern_line_profiler'
            ...
        ]

        DEBUG_TOOLBAR_PANELS = [
            ...
            'django_debug_toolbar_rkern_line_profiler.panels.LineProfilerPanel'
            ...
        ]



Usage
-----

Unlike the regular profile panel that comes with Django Debug Toolbar, the
line profiler will only profile functions you specifically tell it to. You can
either use it as a decorator or directly as a function:

    from django_debug_toolbar_rkern_line_profiler.profile import line_profile

    # Using it as a decorator
    @line_profile
    def profile_page(request):
        ...
        return render(request, 'profile_page.html')

    # Explicit argument
    line_profile(some_function)

In genereal, you'll want the decorator to be the innermost decorator, otherwise
you'll be profiling the decorator function following `@line_profile`

    # WRONG (profiling the `@csrf_exempt` decorator instead of the view function)
    @line_profile
    @csrf_exempt
    @cache_page(60 * 15)
    def profile_page(request):
        ...
        return render(request, 'profile_page.html')

    # CORRECT
    @csrf_exempt
    @cache_page(60 * 15)
    @line_profile
    def profile_page(request):
        ...
        return render(request, 'profile_page.html')

Similar packages and thank you
------------------------------
This package is based off:

* <https://github.com/jlfwong/flask_debugtoolbar_lineprofilerpanel>
* <https://github.com/dmclain/django-debug-toolbar-line-profiler>

Thank you to @jlfwong and @dmclain!
