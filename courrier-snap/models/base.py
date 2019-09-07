from enum import Enum
from typing import List, Optional, Tuple
import attr


@attr.s(auto_attribs=True)
class Order:
    order_id: int
    pickup_point_id: int
    pickup_location: Tuple[int, int]
    pickup_from: 360
    pickup_to: 1380
    dropoff_point_id: int
    dropoff_location: Tuple[int, int]
    dropoff_time_range: Tuple[int, int]
    payment: int


@attr.s(auto_attribs=True)
class Courier:
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
