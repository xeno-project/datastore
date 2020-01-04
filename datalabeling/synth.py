# Copyright 2019 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

version = 'v1beta1'

library = gapic.py_library(
    'datalabeling',
    version,
    config_path='/google/cloud/datalabeling/'
                'artman_datalabeling_v1beta1.yaml',
    artman_output_name='datalabeling-v1beta1',
    include_protos=True,
)

s.move(
    library,
    excludes=[
        'docs/conf.py',
        'docs/index.rst',
        'google/cloud/datalabeling_v1beta1/__init__.py',
        'README.rst',
        'nox*.py',
        'setup.py',
        'setup.cfg',
    ],
)

# Fixup issues in generated code
s.replace(
    "./**/gapic/**/*client.py",
    r"operations_pb2.ImportDataOperationResponse",
    "proto_operations_pb2.ImportDataOperationResponse",
)

s.replace(
    "./**/gapic/**/*client.py",
    r"operations_pb2.ImportDataOperationMetadata",
    "proto_operations_pb2.ImportDataOperationMetadata",
)

s.replace(
    "./tests/unit/gapic/**/test*_client*.py",
    r"operations_pb2.Operation\(",
    "longrunning_operations_pb2.Operation(",
)

# Fix docstrings with no summary line
s.replace(
    "google/cloud/**/proto/*_pb2.py",
    '''__doc__ = """Attributes:''',
    '''__doc__ = """
    Attributes:''',
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=80, cov_level=80)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
