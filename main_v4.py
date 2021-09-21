#!/usr/bin/env python3

from dataclasses import dataclass
from collections.abc import Mapping
from typing import List
from enum import Enum
import datetime
import copy
import logging
import csv


DEFAULT_WORKING_HOURS_PER_MONTH = 8 * 5 * 4
DEFAULT_HOURS_PER_DAY = 8


class Tag(Enum):
    """
    docstring
    """

    WEB_DEVELOPER = 1
    WEB_DESIGNER = 2
    WEB_CONSULTANT = 3
    PROJECT_MANAGER = 4


@dataclass(frozen=True)
class Task:
    """
    docstring
    """
    idx: str
    tag: Tag

    # Mapping from Resource.idx to time for execution
    estimated_time: Mapping[str, datetime.timedelta]
    fixed_hour_price: float


@dataclass(frozen=True)
class TaskDependency:
    """
    Dataclass that describes a Dependency.

    Example: TaskDependency(Task_A, Task_B) means that A depends on B
    """
    depender: Task
    dependee: Task


@dataclass(init=False)
class Phase:
    """
    docstring
    """
    idx: int
    tasks: List[Task]
    dependencies: List[TaskDependency]

    def __init__(self, idx: int, tasks: List[Task], dependencies: List[TaskDependency]):
        self.idx = idx
        self.tasks = copy.deepcopy(tasks)

        for dep_index, dep in enumerate(dependencies):
            for task_depender in self.tasks:
                if task_depender.idx == dep.depender.idx:
                    for task_dependee in self.tasks:
                        if task_dependee.idx == dep.dependee.idx:
                            dependencies[dep_index] = TaskDependency(task_depender, task_dependee)

        self.dependencies = dependencies


@dataclass
class Project:
    """
    docstring
    """
    idx: int
    PHASES: List[Phase]
    tags: List[Tag]


@dataclass
class Resource:
    """
    docstring
    """
    idx: int
    available_time: datetime.timedelta
    fixed_hour_price: datetime.timedelta
    tags: List[Tag]
    remaining_time_per_day: datetime.timedelta


@dataclass
class Assignment:
    """
    docstring
    """
    resource: Resource
    task: Task


@dataclass
class ScheduledDay:
    """
    docstring
    """
    assigments: List[Assignment]


DEFAULT_TASKS = [
    Task("REQ1", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=43)}, 30),
    Task("REQ2", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=47)}, 30),
    Task("REQ3", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=27)}, 30),
    Task("REQ4", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=56)}, 30),
    Task("DES1", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=43)}, 30),
    Task("DES2", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=26)}, 30),
    Task("DES3", Tag.WEB_DESIGNER, {"GEO": datetime.timedelta(minutes=421), }, 30),
    Task("DES4", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=47)}, 30),
    Task("DES5", Tag.WEB_DESIGNER, {"GEO": datetime.timedelta( minutes=155)}, 30),
    Task("DES6", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=28)}, 30),
    Task("DEV1", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=46), "FLD": datetime.timedelta(minutes=58), "XDI": datetime.timedelta(minutes=92)}, 30),
    Task("DEV2", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=23), "FLD": datetime.timedelta(minutes=33), "XDI": datetime.timedelta(minutes=56)}, 30),
    Task("DEV3", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=72), "FLD": datetime.timedelta(minutes=86), "XDI": datetime.timedelta(minutes=122)}, 30),
    Task("DEV4", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=162), "FLD": datetime.timedelta(minutes=193), "XDI": datetime.timedelta(minutes=258)}, 30),
    Task("DEV5", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=77), "FLD": datetime.timedelta(minutes=99), "XDI": datetime.timedelta(minutes=133)}, 30),
    Task("DEV6", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=53), "FLD": datetime.timedelta(minutes=61), "XDI": datetime.timedelta(minutes=99)}, 30),
    Task("DEV7", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=61), "FLD": datetime.timedelta(minutes=80), "XDI": datetime.timedelta(minutes=97)}, 30),
    Task("DEV8", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=48), "FLD": datetime.timedelta(minutes=59), "XDI": datetime.timedelta(minutes=93)}, 30),
    Task("DEV9", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=51), "FLD": datetime.timedelta(minutes=60), "XDI": datetime.timedelta(minutes=84)}, 30),
    Task("DEV10", Tag.WEB_CONSULTANT, {"SGI": datetime.timedelta(minutes=310), "JMK": datetime.timedelta(minutes=366), "JIG": datetime.timedelta(minutes=450)}, 30),
    Task("DEV11", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=108), "FLD": datetime.timedelta(minutes=122), "XDI": datetime.timedelta(minutes=165)}, 30),
    Task("DEV12", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=108), "FLD": datetime.timedelta(minutes=126), "XDI": datetime.timedelta(minutes=153)}, 30),
    Task("DEV13", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=412), "FLD": datetime.timedelta(minutes=471), "XDI": datetime.timedelta(minutes=480)}, 30),
    Task("DEV14", Tag.WEB_CONSULTANT, {"SGI": datetime.timedelta(minutes=351), "JMK": datetime.timedelta(minutes=379), "JIG": datetime.timedelta(minutes=441)}, 30),
    Task("DEV15", Tag.WEB_CONSULTANT, {"SGI": datetime.timedelta(minutes=259), "JMK": datetime.timedelta(minutes=282), "JIG": datetime.timedelta(minutes=321)}, 30),
    Task("DEV16", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=119), "FLD": datetime.timedelta(minutes=134), "XDI": datetime.timedelta(minutes=198)}, 30),
    Task("DEV17", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=120), "FLD": datetime.timedelta(minutes=130), "XDI": datetime.timedelta(minutes=164)}, 30),
    Task("DEV18", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=112)}, 30),
    Task("DEV19", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=102), "FLD": datetime.timedelta(minutes=124), "XDI": datetime.timedelta(minutes=139)}, 30),
    Task("DEV20", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=32)}, 30),
    Task("TES1", Tag.WEB_CONSULTANT, {"SGI": datetime.timedelta(minutes=173), "JMK": datetime.timedelta(minutes=186), "JIG": datetime.timedelta(minutes=268)}, 30),
    Task("TES2", Tag.WEB_CONSULTANT, {"SGI": datetime.timedelta(minutes=178), "JMK": datetime.timedelta(minutes=179), "JIG": datetime.timedelta(minutes=263)}, 30),
    Task("TES3", Tag.WEB_CONSULTANT, {"SGI": datetime.timedelta(minutes=175), "JMK": datetime.timedelta(minutes=184), "JIG": datetime.timedelta(minutes=229)}, 30),
    Task("TES4", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=105), "FLD": datetime.timedelta(minutes=159), "XDI": datetime.timedelta(minutes=180)}, 30),
    Task("TES5", Tag.WEB_CONSULTANT, {"SGI": datetime.timedelta(minutes=112), "JMK": datetime.timedelta(minutes=187), "JIG": datetime.timedelta(minutes=231)}, 30),
    Task("TES6", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=85), "FLD": datetime.timedelta(minutes=112), "XDI": datetime.timedelta(minutes=167)}, 30),
    Task("TES7", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=87)}, 30),
    Task("REL1", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=47), "FLD": datetime.timedelta(minutes=63), "XDI": datetime.timedelta(minutes=107)}, 30),
    Task("REL2", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=77)}, 30),
    Task("REL3", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=88)}, 30),
    Task("REL4", Tag.WEB_DEVELOPER, {"TDS": datetime.timedelta(minutes=143), "FLD": datetime.timedelta(minutes=198), "XDI": datetime.timedelta(minutes=260)}, 30),
    Task("REL5", Tag.PROJECT_MANAGER, {"SGK": datetime.timedelta(minutes=54)}, 30),
]

DEFAULT_PHASES = [
    Phase(
        1,
        [
            DEFAULT_TASKS[0],
            DEFAULT_TASKS[1],
            DEFAULT_TASKS[2],
            DEFAULT_TASKS[3]
        ],
        []
    ),
    Phase(
        2, [
            DEFAULT_TASKS[4],
            DEFAULT_TASKS[5],
            DEFAULT_TASKS[6],
            DEFAULT_TASKS[7],
            DEFAULT_TASKS[8],
            DEFAULT_TASKS[9]
        ],
        []
    ),
    Phase(
        3,
        [
            DEFAULT_TASKS[10],
            DEFAULT_TASKS[11],
            DEFAULT_TASKS[12],
            DEFAULT_TASKS[13],
            DEFAULT_TASKS[15],
            DEFAULT_TASKS[19],
            DEFAULT_TASKS[20],
            DEFAULT_TASKS[27],
            DEFAULT_TASKS[28],
            DEFAULT_TASKS[29],

        ],
        []
    ),
    Phase(
        4,
        [
            DEFAULT_TASKS[10],
            DEFAULT_TASKS[11],
            DEFAULT_TASKS[12],
            DEFAULT_TASKS[13],
            DEFAULT_TASKS[15],
            DEFAULT_TASKS[16],
            DEFAULT_TASKS[17],
            DEFAULT_TASKS[18],
            DEFAULT_TASKS[19],
            DEFAULT_TASKS[20],
            DEFAULT_TASKS[27],
            DEFAULT_TASKS[28],
            DEFAULT_TASKS[29],
        ],
        []
    ),
    Phase(
        5,
        [
            DEFAULT_TASKS[30],
            DEFAULT_TASKS[32],
            DEFAULT_TASKS[35],
            DEFAULT_TASKS[36],
        ],
        []
    ),
     Phase(
        6,
        [
            DEFAULT_TASKS[30],
            DEFAULT_TASKS[31],
            DEFAULT_TASKS[32],
            DEFAULT_TASKS[35],
            DEFAULT_TASKS[36],
        ],
        []
    ),
    Phase(
        7,
        [
            DEFAULT_TASKS[37],
            DEFAULT_TASKS[41],
        ],
        []
    ),
]

DEFAULT_RESOURCES = [
    Resource("TDS", datetime.timedelta(hours=DEFAULT_WORKING_HOURS_PER_MONTH), 15,
             [Tag.WEB_DEVELOPER], datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY)),
    Resource("FLD", datetime.timedelta(hours=DEFAULT_WORKING_HOURS_PER_MONTH), 13,
             [Tag.WEB_DEVELOPER], datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY)),
    Resource("XDI", datetime.timedelta(hours=DEFAULT_WORKING_HOURS_PER_MONTH), 10,
             [Tag.WEB_DEVELOPER], datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY)),
    Resource("GEO", datetime.timedelta(hours=DEFAULT_WORKING_HOURS_PER_MONTH), 10,
             [Tag.WEB_DESIGNER], datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY)),
    Resource("SGI", datetime.timedelta(hours=DEFAULT_WORKING_HOURS_PER_MONTH), 10,
             [Tag.WEB_CONSULTANT], datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY)),
    Resource("JMK", datetime.timedelta(hours=DEFAULT_WORKING_HOURS_PER_MONTH), 9,
             [Tag.WEB_CONSULTANT], datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY)),
    Resource("JIG", datetime.timedelta(hours=DEFAULT_WORKING_HOURS_PER_MONTH), 7,
             [Tag.WEB_CONSULTANT], datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY)),
    Resource("SGK", datetime.timedelta(hours=DEFAULT_WORKING_HOURS_PER_MONTH), 13,
             [Tag.PROJECT_MANAGER], datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY))
]


def main():
    """
    docstring
    """

    project_input = [
        Project(
            1,
            [
                copy.deepcopy(DEFAULT_PHASES[0]),
                copy.deepcopy(DEFAULT_PHASES[1]),
                copy.deepcopy(DEFAULT_PHASES[2]),
                copy.deepcopy(DEFAULT_PHASES[4]),
                copy.deepcopy(DEFAULT_PHASES[6]),
            ],
            []
        ),
        Project(
            2,
            [
                copy.deepcopy(DEFAULT_PHASES[0]),
                copy.deepcopy(DEFAULT_PHASES[1]),
                copy.deepcopy(DEFAULT_PHASES[3]),
                copy.deepcopy(DEFAULT_PHASES[5]),
                copy.deepcopy(DEFAULT_PHASES[6]),
            ],
            []
        ),
        Project(
            3,
            [
                copy.deepcopy(DEFAULT_PHASES[0]),
                copy.deepcopy(DEFAULT_PHASES[1]),
                copy.deepcopy(DEFAULT_PHASES[3]),
                copy.deepcopy(DEFAULT_PHASES[5]),
                copy.deepcopy(DEFAULT_PHASES[6]),
            ],
            []
        ),
         Project(
            4,
            [
                copy.deepcopy(DEFAULT_PHASES[0]),
                copy.deepcopy(DEFAULT_PHASES[1]),
                copy.deepcopy(DEFAULT_PHASES[2]),
                copy.deepcopy(DEFAULT_PHASES[4]),
                copy.deepcopy(DEFAULT_PHASES[6]),
            ],
            []
        ),
                Project(
            5,
            [
                copy.deepcopy(DEFAULT_PHASES[0]),
                copy.deepcopy(DEFAULT_PHASES[1]),
                copy.deepcopy(DEFAULT_PHASES[3]),
                copy.deepcopy(DEFAULT_PHASES[5]),
                copy.deepcopy(DEFAULT_PHASES[6]),
            ],
            []
        ),
        Project(
            6,
            [
                copy.deepcopy(DEFAULT_PHASES[0]),
                copy.deepcopy(DEFAULT_PHASES[1]),
                copy.deepcopy(DEFAULT_PHASES[2]),
                copy.deepcopy(DEFAULT_PHASES[4]),
                copy.deepcopy(DEFAULT_PHASES[6]),
            ],
            []
        ),

    ]

    tasks: List[Task] = []
    deps: List[TaskDependency] = []
    reverse_finder: Mapping[int, Project] = {}
    for project in project_input:
        last_task_of_prev_Phase: Task = None
        for Phase in project.PHASES:
            for task_index, task in enumerate(Phase.tasks):
                tasks.append(task)
                reverse_finder[id(task)] = project

                # Always add dependency between last element of Phase with next Phase
                if task_index == 0:
                    if last_task_of_prev_Phase:
                        deps.append(TaskDependency(task, last_task_of_prev_Phase))

                # Add dependencies until last - 1 element
                if len(Phase.tasks) > task_index + 1:
                    deps.append(TaskDependency(Phase.tasks[task_index+1], task))

            # TODO: This is not used because of super linear deps
            # deps.extend(Phase.dependencies)

            last_task_of_prev_Phase = Phase.tasks[-1]

    logging.info(f"Tasks to process {[(task.idx, id(task)) for task in tasks]}")
    logging.info(
        f"Dependencies to process {[(id(dep.depender), dep.depender.idx, dep.dependee.idx, id(dep.dependee)) for dep in deps]}")

    schedule: List[ScheduledDay] = []
    day = ScheduledDay([])

    while True:
        assigned = False

        for task in list(tasks):
            logging.debug(f"Handling Task {id(task)} with id={task.idx}")

            if len(tasks) > 1 and task_has_deps(task, deps):
                logging.debug("Can't handle Task because it has dependencies")
                continue

            for resource in DEFAULT_RESOURCES:
                if task.tag in resource.tags:
                    possible_remaining_time_per_day = resource.remaining_time_per_day - \
                        task.estimated_time[resource.idx]
                    if possible_remaining_time_per_day.total_seconds() >= 0:
                        assignment = Assignment(resource, task)

                        logging.debug(f"Task handled by resource {resource.idx}")
                        day.assigments.append(assignment)
                        assigned = True
                        resource.remaining_time_per_day = possible_remaining_time_per_day
                        logging.debug(f"Updated resource {resource}")

                        # Remove item from the list
                        tasks.remove(task)

                        # Remove dependencies that no longer exist
                        logging.debug(f"Dependencies before removals{deps}")
                        if tasks:
                            for dep_index, dep in enumerate(deps):
                                if dep.dependee is task:
                                    del deps[dep_index]
                        logging.debug(f"Dependencies after removals{deps}")

                        break
                if assigned:
                    break
            if assigned:
                break

        logging.debug(f"Number of tasks left {len(tasks)}")
        if len(tasks) == 0:
            schedule.append(day)
            break

        if not assigned:
            logging.debug("Changing day")
            schedule.append(day)
            day = ScheduledDay([])
            for resource in DEFAULT_RESOURCES:
                resource.remaining_time_per_day = datetime.timedelta(hours=DEFAULT_HOURS_PER_DAY)

    with open('output.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        csv_header = ['day', 'assignment_id', 'resource_id', 'task_id', 'project_id', 'estimated_time']
        writer.writerow(csv_header)

        for day_index, day in enumerate(schedule):
            logging.info(f"Day {day_index+1}")
            current_day = day_index+1
            for assignment_index, assignment in enumerate(day.assigments):
                logging.info(f"Assignment {assignment_index} -> Resource {assignment.resource.idx} does Task: "
                             f"{assignment.task.idx} of Project {reverse_finder[id(assignment.task)].idx} "
                             f"in {assignment.task.estimated_time[assignment.resource.idx]}")
                writer.writerow([current_day,
                                 assignment_index,
                                 assignment.resource.idx,
                                 assignment.task.idx,
                                 reverse_finder[id(assignment.task)].idx,
                                 assignment.task.estimated_time[assignment.resource.idx]
                                 ])


def task_has_deps(task: Task, deps: List[TaskDependency]) -> bool:
    for dep in deps:
        if dep.depender is task:
            return True

    return False


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    main()
