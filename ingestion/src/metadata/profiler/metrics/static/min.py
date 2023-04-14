#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Min Metric definition
"""
# pylint: disable=duplicate-code


from sqlalchemy import column, func

from metadata.profiler.metrics.core import StaticMetric, _label
from metadata.profiler.orm.registry import is_date_time, is_quantifiable


class Min(StaticMetric):
    """
    MIN Metric

    Given a column, return the min value.
    """

    @classmethod
    def name(cls):
        return "min"

    @_label
    def fn(self):
        """sqlalchemy function"""
        if (not is_quantifiable(self.col.type)) and (not is_date_time(self.col.type)):
            return None
        return func.min(column(self.col.name))

    def df_fn(self, dfs=None):
        """pandas function"""
        if is_quantifiable(self.col.type) or is_date_time(self.col.type):
            return min((df[self.col.name].min() for df in dfs))
        return 0