import line_profiler
import functools
import inspect
import linecache
import collections

from debug_toolbar.panels import Panel

from .profile import functions_to_profile


def process_line_stats(line_stats):
    "Converts line_profiler.LineStats instance into something more useful"

    profile_results = []

    if not line_stats:
        return profile_results

    # We want timings in ms (instead of CPython's microseconds)
    multiplier = line_stats.unit / 1e-3

    for key, timings in sorted(line_stats.timings.items()):
        if not timings:
            continue

        filename, start_lineno, func_name = key

        all_lines = linecache.getlines(filename)
        sublines = inspect.getblock(all_lines[start_lineno - 1 :])
        end_lineno = start_lineno + len(sublines)

        line_to_timing = collections.defaultdict(lambda: (-1, 0))

        for (lineno, nhits, time) in timings:
            line_to_timing[lineno] = (nhits, time)

        padded_timings = []
        total_time = sum([time for _, _, time in timings])

        for lineno in range(start_lineno, end_lineno):
            nhits, time = line_to_timing[lineno]
            perc = 100 * (time / total_time)
            padded_timings.append((lineno, nhits, time, perc))

        profile_results.append(
            {
                "filename": filename,
                "start_lineno": start_lineno,
                "func_name": func_name,
                "timings": [
                    (lineno, all_lines[lineno - 1], time * multiplier, nhits, perc)
                    for (lineno, nhits, time, perc) in padded_timings
                ],
                "total_time": total_time * multiplier,
            }
        )

    return profile_results


class LineProfilerPanel(Panel):
    """
    Panel that displays line profiling information.
    """

    title = "Line Profiler"

    template = "django_debug_toolbar_rkern_line_profiler/panels/content.html"

    def process_request(self, request):
        self.profiler = line_profiler.LineProfiler()

        for f in functions_to_profile:
            self.profiler.add_function(f)

        self.stats = None

    def process_view(self, request, view_func, view_args, view_kwargs):
        return self.profiler.runcall(view_func, request, *view_args, **view_kwargs)

    def process_response(self, request, response):
        self.stats = self.profiler.get_stats()

        processed_line_stats = process_line_stats(self.stats)
        self.record_stats({"stats": processed_line_stats})

        return response
