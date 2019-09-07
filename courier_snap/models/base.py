import json
import pprint
from enum import Enum
from typing import List, Optional, Tuple, Dict
from pathlib import Path
import attr
import logging

from courier_snap.utils import get_project_path


logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True, repr=False)
class Location:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


@attr.s(repr=False, auto_attribs=True)
class TimeRange:
    start: int
    end: int

    def __repr__(self) -> str:
        return f"start={self.start // 60:02d}:{self.start % 60:02d}, end={self.end // 60:02d}:{self.end % 60:02d}"


@attr.s(auto_attribs=True)
class Order:
    id: int
    pickup_point_id: int
    pickup_location: Location
    pickup_time: TimeRange
    dropoff_point_id: int
    dropoff_location: Location
    dropoff_time: TimeRange
    payment: int

    @classmethod
    def from_json(cls, order: dict) -> 'Order':
        return cls(id=order['order_id'],
                   pickup_location=Location(order["pickup_location_x"], order["pickup_location_y"]),
                   pickup_time=TimeRange(order["pickup_from"], order["pickup_to"]),
                   dropoff_location=Location(order["dropoff_location_x"], order["dropoff_location_y"]),
                   dropoff_time=TimeRange(order["dropoff_from"], order["dropoff_to"]),
                   payment=order["payment"],
                   dropoff_point_id=order["dropoff_point_id"],
                   pickup_point_id=order["pickup_point_id"]
                   )


@attr.s(auto_attribs=True)
class Courier:
    # TODO: more fields
    id: str
    orders_picked: List[Order]
    # TODO: deserialize from json


class RouteActionType(Enum):
    pickup = "pickup"
    dropoff = "dropoff"


@attr.s(auto_attribs=True)
class RouteAction:
    courier_id: int
    action_type: RouteActionType
    order_id: int
    point_id: int
    depot_id: Optional[int]
    # TODO: serialize json


@attr.s(auto_attribs=True)
class OptimizeTask:
    depots: Dict[int, Location]
    orders: Dict[int, Order]
    couriers: Dict[int, Courier]


class YobaParser:

    def from_input_json(self, task_data_path: Path) -> OptimizeTask:
        logger.info("Loading data from {task_data_path.}")
        task_data = json.loads(task_data_path.read_text())
        return OptimizeTask(orders={
            order.id: order for order in [Order.from_json(order_data) for order_data in task_data["orders"]]
        }, couriers={}, depots={})


if __name__ == "__main__":
    task = YobaParser().from_input_json(get_project_path() / "task-data/data/contest_input.json")
    pprint.pprint(task.orders)
