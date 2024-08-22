# coding=utf-8
# Copyright 2024 The Google Research Authors.
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

"""Helpers to define experiments and models for xmanager runs.
"""

import dataclasses
import sys
import tensorflow.compat.v1 as tf

from google.protobuf import text_format
from models import model_config_pb2


if "gfile" not in sys.modules:
  gfile = tf.io.gfile


@dataclasses.dataclass(frozen=True)
class ExperimentConfig:
  name: str
  update_mem: bool
  warmstart: bool
  warmstart_batch_fraction: float
  warmstart_update_model: bool
  reset_memory: bool
  reset_nbd_loader: bool


EXPERIMENTS = [
    ExperimentConfig(
        name="transductive",
        update_mem=True,
        warmstart=True,
        warmstart_batch_fraction=0.2,
        warmstart_update_model=True,
        reset_memory=False,
        reset_nbd_loader=False,
    ),
    ExperimentConfig(
        name="transfer_no_warmstart",
        update_mem=True,
        warmstart=False,
        warmstart_batch_fraction=0.0,
        warmstart_update_model=False,
        reset_memory=True,
        reset_nbd_loader=True,
    ),
    ExperimentConfig(
        name="transfer_warmstart",
        update_mem=True,
        warmstart=True,
        warmstart_batch_fraction=0.2,
        warmstart_update_model=False,
        reset_memory=True,
        reset_nbd_loader=True,
    )
]


_MODEL_CONFIG_PATHS = [
    "models/configs/tgn.pbtxt",
    "models/configs/tgn_structmap.pbtxt",
    "models/configs/tgn_structmap_alpha10.pbtxt",
    "models/configs/tgn_structmap_alpha100.pbtxt",
    "models/configs/edgebank.pbtxt",
]


def get_model_config(model_name):
  """Returns a model config from the specified model name."""
  model_configs = {}
  for model_config_path in _MODEL_CONFIG_PATHS:
    model_config = model_config_pb2.TlpModelConfig()
    filepath = str(model_config_path)
    with gfile.GFile(filepath, "r") as f:
      text_format.Parse(f.read(), model_config)
    if model_config.model_name in model_configs:
      raise ValueError(
          f"Duplicate model name: {model_config.model_name}"
      )
    model_configs[model_config.model_name] = model_config
  return model_configs[model_name]
