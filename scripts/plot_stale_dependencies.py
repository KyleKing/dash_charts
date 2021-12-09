"""Plot the release date of all dependencies."""

from pathlib import Path
from typing import Any, Dict

import pandas as pd
import plotly.express as px
from calcipy.doit_tasks.packaging import _PATH_PACK_LOCK, _read_cache

path_pack_lock = Path.cwd().parent / 'calcipy' / _PATH_PACK_LOCK.name
cache = _read_cache(path_pack_lock)


def unwrap_attr(item: Any) -> Dict[str, Any]:
    return {
        attrib: item.__getattribute__(attrib)
        for attrib in dir(item) if not attrib.startswith('_')
    }


df_dep = pd.DataFrame(map(unwrap_attr, cache.values()))

# > fig = px.histogram(df_dep, x='datetime')
fig = px.scatter(df_dep, x='datetime', hover_name='name')
fig.show()

breakpoint()
