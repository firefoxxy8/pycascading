#
# Copyright 2011 Twitter, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Various operations acting on the tuples.

* Add fields to the stream: Add
* Map fields to new fields: Map
* Select fields from the stream: Retain
* Remove fields from the stream: Discard
* Rename fields: Rename
"""

import itertools

from cascading.tuple import Fields
from cascading.operation import Identity
import cascading.pipe.assembly.Rename
import cascading.pipe.assembly.Shape

from pycascading.pipe import Apply, SubAssembly, coerce_to_fields
from pycascading.decorators import udf


def Map(*args):
    """Maps the given input fields to output fields.

    The fields specified as input will be removed from the result.
    """
    if len(args) == 2:
        input_selector = Fields.ALL
        (function, output_field) = args
    elif len(args) == 3:
        (input_selector, function, output_field) = args
    else:
        raise Exception('Map needs to be called with 2 or 3 parameters')
    df = udf(produces=output_field)(function)
    return Apply(input_selector, df, Fields.SWAP)


def Retain(*fields_to_keep):
    """Retain only the given fields.

    The fields can be given in array or by separate parameters.
    """
    if len(fields_to_keep) > 1:
        fields_to_keep = list(itertools.chain(fields_to_keep))
    else:
        fields_to_keep = fields_to_keep[0]
    return Apply(fields_to_keep, Identity(Fields.ARGS), Fields.RESULTS)


def Discard(fields_to_discard):
    # In 2.0 there's a builtin function this, Discard
    # In 1.2 there is nothing for this
    return Apply(fields_to_discard, Identity(), Fields.REPLACE)


def Rename(fields_from, fields_to):
    return SubAssembly(cascading.pipe.assembly.Rename, \
                       coerce_to_fields(fields_from), \
                       coerce_to_fields(fields_to))
