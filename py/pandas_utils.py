import pandas as pd
import numpy as np


def series_from_ndim_array(array, index_names=None):
    iterables = [range(dim_size) for dim_size in array.shape]
    multi_index = pd.MultiIndex.from_product(iterables, names=index_names)

    series_from_array = pd.Series(data=array.reshape(array.size), index=multi_index)

    return series_from_array

#
# ar3d = np.array([[[1, 2, 3],
#                   [2, 3, 4],
#                   [3, 4, 5],
#                   [4, 5, 6]],
#                  [[1, 2, 3],
#                   [2, 3, 4],
#                   [3, 4, 5],
#                   [4, 5, 6]]])
# #
# iterables = [range(dim_size) for dim_size in ar3d.shape]
# df = series_from_ndim_array(ar3d, index_names=['l1', 'l2', 'lag'])
#
# for i in iterables[0]:
#     for j in iterables[1]:
#         for k in iterables[2]:
#             print(df.loc[i, j, k] == ar3d[i, j, k])
