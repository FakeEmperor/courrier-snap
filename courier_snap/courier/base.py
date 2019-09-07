import attr

from courier_snap.models.base import Courier, Location, Order, TimeRange
from typing import List, Dict


@attr.s(auto_attribs=True)
class CourierState:
    original: Courier
    current_location: Location
    current_time: int
    orders_picked: List[Order]


class CourierPlanner:

    def __init__(self, work_time: TimeRange, couriers: Dict[int, Courier]):
        self.work_time = work_time
        self.couriers_states = {
            courier_id: CourierState(original=courier,
                                     current_location=courier.location)
            for courier_id, courier in couriers.items()
        }

    def get_viable_couriers(self, order: Order, couriers: List[Courier]) -> :
        """
        Get all couriers for an order that satisfy the following:

        - Could
        -

        :param order:
        :param couriers:
        :return:
        """
