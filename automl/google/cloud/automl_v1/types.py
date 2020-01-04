# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import
import sys

from google.api_core.protobuf_helpers import get_messages

from google.cloud.automl_v1.proto import annotation_payload_pb2
from google.cloud.automl_v1.proto import annotation_spec_pb2
from google.cloud.automl_v1.proto import classification_pb2
from google.cloud.automl_v1.proto import data_items_pb2
from google.cloud.automl_v1.proto import dataset_pb2
from google.cloud.automl_v1.proto import detection_pb2
from google.cloud.automl_v1.proto import geometry_pb2
from google.cloud.automl_v1.proto import image_pb2
from google.cloud.automl_v1.proto import io_pb2
from google.cloud.automl_v1.proto import model_evaluation_pb2
from google.cloud.automl_v1.proto import model_pb2
from google.cloud.automl_v1.proto import operations_pb2 as proto_operations_pb2
from google.cloud.automl_v1.proto import prediction_service_pb2
from google.cloud.automl_v1.proto import service_pb2
from google.cloud.automl_v1.proto import text_extraction_pb2
from google.cloud.automl_v1.proto import text_pb2
from google.cloud.automl_v1.proto import text_segment_pb2
from google.cloud.automl_v1.proto import text_sentiment_pb2
from google.cloud.automl_v1.proto import translation_pb2
from google.longrunning import operations_pb2 as longrunning_operations_pb2
from google.protobuf import any_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2
from google.rpc import status_pb2


_shared_modules = [
    longrunning_operations_pb2,
    any_pb2,
    field_mask_pb2,
    timestamp_pb2,
    status_pb2,
]

_local_modules = [
    annotation_payload_pb2,
    annotation_spec_pb2,
    classification_pb2,
    data_items_pb2,
    dataset_pb2,
    detection_pb2,
    geometry_pb2,
    image_pb2,
    io_pb2,
    model_evaluation_pb2,
    model_pb2,
    proto_operations_pb2,
    prediction_service_pb2,
    service_pb2,
    text_extraction_pb2,
    text_pb2,
    text_segment_pb2,
    text_sentiment_pb2,
    translation_pb2,
]

names = []

for module in _shared_modules:  # pragma: NO COVER
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)
for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = "google.cloud.automl_v1.types"
        setattr(sys.modules[__name__], name, message)
        names.append(name)


__all__ = tuple(sorted(names))
