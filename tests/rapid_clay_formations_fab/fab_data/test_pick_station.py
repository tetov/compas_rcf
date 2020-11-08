from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest
from compas.geometry import Frame

from rapid_clay_formations_fab.fab_data import FabricationElement
from rapid_clay_formations_fab.robots import PickStation


@pytest.fixture
def frame_list():
    return [
        Frame([0, 0, 0], [1, 0, 0], [0, 1, 0]),
        Frame([1, 0, 0], [1, 0, 0], [0, 1, 0]),
        Frame([2, 0, 0], [1, 0, 0], [0, 1, 0]),
        Frame([3, 0, 0], [1, 0, 0], [0, 1, 0]),
        Frame([4, 0, 0], [1, 0, 0], [0, 1, 0]),
    ]


@pytest.fixture
def station1(frame_list):
    return PickStation(
        frame_list,
        elem_height=200,
        elem_egress_distance=250,
        station_egress_distance=300,
    )


@pytest.fixture
def station2_data():
    return {
        "pick_frames": [
            {"point": [0, 1, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
            {"point": [0, 2, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
        ],
        "elem_height": 150,
        "elem_egress_distance": 200,
        "station_egress_distance": 250,
    }


@pytest.fixture
def station2(station2_data):
    return PickStation.from_data(station2_data)


@pytest.fixture
def pick_elements(station1, frame_list):
    kwargs = {
        "height": station1.elem_height,
        "egress_frame_distance": station1.elem_egress_distance,
    }
    elements = []
    for frame in frame_list:
        elem = FabricationElement(frame, "pick_elem", **kwargs)
        elements.append(elem)
    return elements


def test_frame_iter(station2_data):
    station = PickStation.from_data(station2_data)
    frame_list = station.pick_frames
    for n in range(12):
        frame = station._get_next_pick_frame()
        assert frame == frame_list[n % len(frame_list)]


def test_pick_element_generator(station1, pick_elements):
    assert station1.get_next_pick_elem().location == pick_elements[0].location
    for _ in range(len(pick_elements) - 1):
        station1.get_next_pick_elem()
    assert station1.get_next_pick_elem().location == pick_elements[0].location
    assert station1.get_next_pick_elem().location == pick_elements[1].location


def test_station_egress_frame(station1):
    assert station1.station_egress_frame == Frame(
        [0, 0, -station1.station_egress_distance], [1, 0, 0], [0, 1, 0]
    )


def test_from_data(station2, station2_data):
    assert station2.elem_height == station2_data["elem_height"]


def test_to_from_data(station2_data):
    station = PickStation.from_data(station2_data)
    assert station2_data == station.to_data()
