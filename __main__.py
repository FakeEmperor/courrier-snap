from courier_snap.courier.base import CourierPlanner
from courier_snap.models.base import YobaParser, TimeRange
from courier_snap.utils import get_project_path

import logging

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    parser = YobaParser()
    task = parser.from_input_json(get_project_path() / "task-data/data/contest_input.json")
    print(sum([order.payment for order in task.orders.values()]))
    planner = CourierPlanner(TimeRange(360, 1439), couriers=task.couriers)
    actions = planner.solve(task.orders)
    parser.to_output_json(actions, get_project_path() / "output.json")
