import pytest

import core.metadata.task as task


@pytest.fixture
def pipeline():
    return task.Pipeline()

def test_pipeline_process(pipeline):
    pass


def test_pipline_task__create_pipeline():
    pass

def test_pipeline_task__process_monitor():
    pass


def test_analyzer_task__create_pipeline():
    pass

def test_analyzer_task_from_source_and_destinations():
    pass

def test_analyzer_task__process_monitor():
    pass

def test_analyzer_task_run():
    pass


def test_run_monitor_task_from_workspace():
    pass

def test_run_monitor_task__process_monitor():
    pass

def test_run_monitor_task_run():
    pass


def test_run_monitors_task_from_source_and_destinations():
    pass

def test_run_and_analyze_task_run():
    pass


