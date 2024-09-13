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

    TuruSnowflakeCursor = turu.snowflake.Cursor  # type: ignore
    USE_TURU = True
    Tag = TuruTag  # type: ignore
    InsertTag = Insert  # type: ignore
    UpdateTag = Update  # type: ignore
    DeleteTag = Delete  # type: ignore
    TruncateTag = Truncate  # type: ignore


except ImportError:
    TuruSnowflakeCursor = SnowflakeCursor  # type: ignore
    USE_TURU = False

    class Tag:  # type: ignore
        pass

    class InsertTag(Tag, Generic[GenericTable]):  # type: ignore
        pass

    class UpdateTag(Tag, Generic[GenericTable]):  # type: ignore
        pass

    class DeleteTag(Tag, Generic[GenericTable]):  # type: ignore
        pass

    class TruncateTag(Tag, Generic[GenericTable]):  # type: ignore
        pass
