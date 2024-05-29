from typing import TypeAlias

try:
    import pandas as pd  # type: ignore[import]

    PandasDataFrame: TypeAlias = pd.DataFrame  # type: ignore
    USE_PANDAS = True

except ImportError:

    class DataFrame:
        pass

    PandasDataFrame: TypeAlias = DataFrame  # type: ignore
    USE_PANDAS = False
