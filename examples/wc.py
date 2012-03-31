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

"""Simple word count example.

The data is expected in the pycascading_data/ folder if run in local mode,
and in the pycascading_data/ folder in the user's HDFS home if run with Hadoop. 
"""

print '@@@@@@ running wc.py'

from pycascading.helpers import *
from pycascading.operators import *

def fun():
    print '*** OK!!', module_paths, jobconf, flow_process

def m():
    print 'glob func'

class C:
    def __init__(self):
        self.x = 1

    @classmethod
    def f(cls):
        print 'clsmethod'

    def m(self):
#        m()
        print 'ok m', self.x

def main():
    flow = Flow()
    input = flow.source(Hfs(TextLine(), 'pycascading_data/town.txt'))
    output = flow.tsv_sink('pycascading_data/out')

    @map(produces=['word'])
    @yields
    def split_words(tuple, field, fun, obj):
        print '&&&& fun', field, fun, fun(), obj.x
        for word in tuple.get(field).split():
            yield [word]

    @map()
    def add_one(tuple):
        yield ['a']

    @udf(produces=['count'])
    def count(group, tuple):
        print '*** count got', group.get(0)
        c = 0
        for t in tuple:
            c += 1
        yield [c]

    c = C()
    c.x = 2
    input | Map('line', split_words(0, m, c), 'word') | GroupBy('word') | count | output

    flow.run(num_reducers=2)
