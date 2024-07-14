from typing import Generic, TypeAlias

from snowflake.connector.cursor import SnowflakeCursor

from snowman.relation.table import GenericTable

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
    from turu.core.tag import Delete, Insert, Truncate, Update
    from turu.core.tag import Tag as TuruTag

    TuruSnowflakeCursor = turu.snowflake.Cursor
    USE_TURU = True
    Tag = TuruTag  # type: ignore
    InsertTag = Insert  # type: ignore
    UpdateTag = Update  # type: ignore
    DeleteTag = Delete  # type: ignore
    TruncateTag = Truncate  # type: ignore


except ImportError:
    TuruSnowflakeCursor = SnowflakeCursor
    USE_TURU = False

    class Tag:
        pass

    class InsertTag(Tag, Generic[GenericTable]):
        pass

    class UpdateTag(Tag, Generic[GenericTable]):
        pass

    class DeleteTag(Tag, Generic[GenericTable]):
        pass

    class TruncateTag(Tag, Generic[GenericTable]):
        pass
