from typing import TypeAlias

from snowflake.connector.cursor import SnowflakeCursor

try:
    import pandas as pd  # type: ignore[import]

    PandasDataFrame: TypeAlias = pd.DataFrame  # type: ignore
    USE_PANDAS = True

except ImportError:

    class DataFrame:
        pass

    PandasDataFrame: TypeAlias = DataFrame  # type: ignore
    USE_PANDAS = False


try:
    import turu.snowflake  # type: ignore[import]

    TuruSnowflakeCursor = turu.snowflake.Cursor
    USE_TURU = True

except ImportError:
    TuruSnowflakeCursor = SnowflakeCursor
    USE_TURU = False
