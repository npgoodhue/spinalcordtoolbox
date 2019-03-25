#!/usr/bin/env python
# -*- coding: utf-8
# pytest unit tests for spinalcordtoolbox.process_seg

# TODO: add dummy image with different resolution to check impact of input res
# TODO: add test with known angle (i.e. not found with fitting)
# TODO: test empty slices and slices with two objects
# TODO: figure out why some metrics need float() for assertion

from __future__ import absolute_import
import pytest
import numpy as np
from spinalcordtoolbox import process_seg
from sct_process_segmentation import Param

from create_test_data import dummy_segmentation


# Define global variables
PARAM = Param()
VERBOSE = 0

# Generate a list of fake segmentation for testing: (dummy_segmentation(params), dict of expected results)
im_segs = [
    (dummy_segmentation(size_arr=(128, 128, 5), shape='ellipse', a=50.0, b=30.0),
     {'area': 47.01, 'angle_AP': 0.0, 'angle_RL': 0.0, 'diameter_AP': 6.0, 'diameter_RL': 10.0, 'eccentricity': 0.8,
      'orientation': 0.0, 'solidity': 1.0}),
    (dummy_segmentation(size_arr=(128, 128, 5), pixdim=(0.5, 0.5, 5), shape='rectangle', a=10.0, b=6.0),
     {'area': 68.25, 'angle_RL': 0.0}),
    (dummy_segmentation(size_arr=(128, 128, 5), pixdim=(0.5, 0.5, 5), shape='rectangle', angle_IS=15, a=10.0, b=6.0),
     {'area': 68.25, 'angle_RL': 0.0}),
    (dummy_segmentation(size_arr=(128, 128, 50), shape='ellipse', angle_RL=15, a=50.0, b=30.0),
     {'area': 47.01, 'angle_AP': 0.0, 'angle_RL': 15.0}),
    ]


# noinspection 801,PyShadowingNames
@pytest.mark.parametrize('im_seg,expected', im_segs)
def test_compute_shape_without_angle(im_seg, expected):
    # If input image has a tilted spinal cord about RL axis, then correct for angle while calling the function
    if expected['angle_RL'] == 0.0:
        angle_corr = False
    else:
        angle_corr = True
    metrics = process_seg.compute_shape(im_seg,
                                        algo_fitting=PARAM.algo_fitting,
                                        angle_correction=angle_corr,
                                        verbose=VERBOSE)
    for key in expected.keys():
        assert np.mean(metrics[key].data) == pytest.approx(expected[key], rel=0.03)
