"""
testing_common.py
=================
"""
import os

import pytest
import process
import routing, common, router, processor
import common.config as config
from common.types import Config


def spy_on(mocker, obj) -> None:
    pieces = obj.split(".")
    module = ".".join(pieces[0:-1])
    mocker.patch(obj, new=mocker.spy(eval(module), pieces[-1]))


def spies(mocker, list_of_spies) -> None:
    for spy in list_of_spies:
        spy_on(mocker, spy)


def attach_spies(mocker) -> None:
    spies(
        mocker,
        [
            "routing.route_series.push_series_serieslevel",
            "routing.route_series.push_serieslevel_outgoing",
            "routing.generate_taskfile.create_series_task",
            "common.monitor.post",
            "common.monitor.send_event",
            "common.monitor.send_register_series",
            "common.monitor.send_register_task",
            "common.monitor.send_task_event",
            "router.route_series",
            # "process.process_series",
        ],
    )
    mocker.patch("processor.process_series", new=mocker.spy(process.process_series, "process_series"))

    # spy_on(mocker, "routing.route_series.push_series_serieslevel")
    # # mocker.patch(
    # #     "routing.route_series.push_series_serieslevel", new=mocker.spy(routing.route_series, "push_series_serieslevel")
    # # )
    # mocker.patch(
    #     "routing.route_series.push_serieslevel_outgoing",
    #     new=mocker.spy(routing.route_series, "push_serieslevel_outgoing"),
    # )
    # mocker.patch(
    #     "routing.generate_taskfile.create_series_task", new=mocker.spy(routing.generate_taskfile, "create_series_task")
    # )

    # mocker.patch("common.monitor.post", new=mocker.spy(common.monitor, "post"))
    # mocker.patch("common.monitor.send_register_series", new=mocker.spy(common.monitor, "send_register_series"))
    # mocker.patch("common.monitor.send_register_task", new=mocker.spy(common.monitor, "send_register_task"))
    # mocker.patch("common.monitor.send_event", new=mocker.spy(common.monitor, "send_event"))
    # mocker.patch("common.monitor.send_task_event", new=mocker.spy(common.monitor, "send_task_event"))
    # mocker.patch("router.route_series", new=mocker.spy(router, "route_series"))
    # mocker.patch("processor.process_series", new=mocker.spy(process.process_series, "process_series"))


@pytest.fixture(scope="function")
def mocked(mocker):
    mocker.resetall()
    attach_spies(mocker)
    return mocker


def load_config(fs, extra) -> Config:
    config_path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/data/test_config.json")
    fs.add_real_file(config_path, target_path=config.configuration_filename, read_only=False)
    for k in ["incoming", "studies", "outgoing", "success", "error", "discard", "processing"]:
        fs.create_dir(f"/var/{k}")
    config.read_config()
    config.mercure = Config(**{**config.mercure.dict(), **extra})  #   # type: ignore
    config.save_config()
    return config.mercure
