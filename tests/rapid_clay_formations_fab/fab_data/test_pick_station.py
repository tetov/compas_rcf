from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest
from compas.geometry import Frame

from rapid_clay_formations_fab.fab_data import PickStation


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
def station(frame_list):
    return PickStation(
        frame_list,
        elem_height=200,
        elem_egress_distance=250,
        station_egress_distance=300,
    )


@pytest.fixture
def station_data(frame_list):
    return {
        "pick_frames": [
            {"point": [0, 1, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
            {"point": [0, 2, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
        ],
        "elem_height": 150,
        "elem_egress_distance": 200,
        "station_egress_distance": 250,
    }


def test_generator(station, frame_list):
    for n in range(12):
        frame = next(station.frame_gen)
        assert frame == frame_list[n % len(frame_list)]


def test_station_egress_frame(station):
    assert station.station_egress_frame == Frame(
        [0, 0, station.station_egress_distance], [1, 0, 0], [0, 1, 0]
    )


def test_from_data(station_data):
    station = PickStation.from_data(station_data)
    assert station.elem_height == station_data["elem_height"]


def test_to_from_data(station_data):
    station = PickStation.from_data(station_data)
    print(station.to_data())
    assert station_data == station.to_data()
