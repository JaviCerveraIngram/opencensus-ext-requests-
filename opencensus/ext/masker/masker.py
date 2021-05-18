# Copyright 2021, CloudBlue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from copy import deepcopy
from typing import Any, Dict, List, Tuple, Union

__masked_fields: Tuple[str] = tuple()
__masked_params: Tuple[str] = tuple()


def masked_fields(fields: Union[List[str], Tuple[str]]) -> None:
    global __masked_fields
    __masked_fields = tuple(fields)


def mask_fields(data: Union[Dict, List, Tuple]) -> str:
    return json.dumps(__mask_fields(data))


def __mask_fields(data: Union[Dict, List, Tuple]) -> Union[Dict, List, Tuple]:
    if isinstance(data, dict):
        return __mask_dict(data)
    elif isinstance(data, (list, tuple)):
        return [__mask_fields(x) for x in data]
    else:
        return data


def __mask_dict(data: Dict) -> Dict:
    data = deepcopy(data)
    for k in data.keys():
        if k in __masked_fields:
            data[k] = '*' * len(str(data[k]))
    for k in data.keys():
        data[k] = __mask_fields(data[k])
    return data


def masked_params(params: Union[List[str], Tuple[str]]) -> None:
    global __masked_params
    __masked_params = tuple(params)


def mask_params(data: Union[Dict, List, Tuple]) -> str:
    return json.dumps(__mask_params(data))


def __mask_params(data: Union[Dict, List, Tuple]) -> Union[Dict, List, Tuple]:
    if isinstance(data, dict):
        return __mask_params_dict(data)
    elif isinstance(data, (list, tuple)):
        return [__mask_params(x) for x in data]
    else:
        return data


def __mask_params_dict(data: Dict) -> Dict:
    data = deepcopy(data)
    for k in data.keys():
        value = data[k]
        if k == 'params' and isinstance(value, list):
            data[k] = __mask_params_list(value)
        elif k == 'parameter' and 'value' in data:
            data[k] = __mask_config_param(data, value)
        elif isinstance(value, (dict, list, tuple)):
            data[k] = __mask_params(value)
    for k in data.keys():
        data[k] = __mask_params(data[k])
    return data


def __mask_params_list(params: List) -> List:
    return [__mask_param(p) for p in params]


def __mask_param(param: Any) -> Any:
    if isinstance(param, dict) and 'id' in param and 'value' in param:
        is_password = param['type'] == 'password' if 'type' in param else False
        if is_password or str(param['id']) in __masked_params:
            param['value'] = '*' * len(str(param['value']))
    return param


def __mask_config_param(parent: Dict, param: Any) -> Any:
    if isinstance(param, dict) and 'id' in param:
        is_password = param['type'] == 'password' if 'type' in param else False
        if is_password or str(param['id']) in __masked_params:
            if 'value' in parent:
                parent['value'] = '*' * len(str(parent['value']))
            if 'value' in param:
                param['value'] = '*' * len(str(param['value']))
    return param
