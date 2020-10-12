from hypothesis import settings, Verbosity, Phase
from hypothesis.database import ExampleDatabase

"""
    Notes from the source code

    "derandomize=True implies database=None, so passing "
"""


class HypothesisProfiles:
    # Can't create examples folder thus not working as global
    db = ExampleDatabase("examples")

    def __init__(self):
        pass

    settings.register_profile(
        "bugfound",
        stateful_step_count=10,
        max_examples=10000,
        phases=[Phase.generate],
        report_multiple_bugs=True,
        derandomize=False,
        database=db,
        print_blob=True,
    )

    settings.register_profile(
        "bugfound_reuse",
        phases=[Phase.reuse],
        report_multiple_bugs=True,
        derandomize=False,
        database=db,
        print_blob=True,
    )

    settings.register_profile(
        "shrinking",
        phases=[Phase.reuse, Phase.shrink],
        report_multiple_bugs=True,
        derandomize=False,
        database=db,
        print_blob=True,
    )
