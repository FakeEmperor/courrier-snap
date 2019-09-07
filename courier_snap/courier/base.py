import logging

import attr

from courier_snap.models.base import Courier, Location, Order, TimeRange, RouteAction, RouteActionType
from typing import List, Dict, Optional, Set, Tuple


logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class CourierState:
    original: Courier
    current_location: Location
    current_time: int
    orders_picked: List[Order]


class CourierPlanner:

    def __init__(self, work_time: TimeRange, couriers: Dict[int, Courier]):
        self.work_time = work_time
        self.couriers_states: Dict[int, CourierState] = {
            courier_id: CourierState(original=courier,
                                     current_location=courier.location,
                                     current_time=360,
                                     orders_picked=[])
            for courier_id, courier in couriers.items()
        }

    def will_fulfill(self, courier_state: CourierState, order: Order) -> Optional[Tuple[int, int]]:
        travel_to_pickup = courier_state.current_location.distance(order.pickup_location)
        travel_to_dropoff = order.pickup_location.distance(order.dropoff_location)

        pickup_time = (courier_state.current_time + travel_to_pickup)
        dropoff_time = pickup_time + travel_to_dropoff
        if pickup_time in order.pickup_time and dropoff_time in order.dropoff_time and dropoff_time in self.work_time:
            return order.payment - 2 * (travel_to_pickup + travel_to_dropoff), dropoff_time
        return None

    def solve(self, orders: Dict[int, Order]) -> List[RouteAction]:
        unfulfilled_orders: Set[int] = set(orders.keys())
        actions: List[RouteAction] = []
        processed_couriers = 0
        for courier_state in self.couriers_states.values():
            found_order = True
            logger.info(f"[{processed_couriers:02d}/{len(self.couriers_states)}] Processing courier {courier_state.original.id}")
            while found_order:
                found_order = False
                most_profitable: Tuple[int, int, int] = None  # tuple: order_id, profit, time after dropoff
                # find the best across all unfulfilled
                for order_id in unfulfilled_orders:
                    fulfillment_state = self.will_fulfill(courier_state, orders[order_id])
                    if not fulfillment_state:
                        continue
                    profit, dropoff = fulfillment_state
                    if profit is not None and profit > 0 and (most_profitable is None or most_profitable[1] <= profit):
                        most_profitable = (order_id, profit, dropoff)
                        found_order = True

                if found_order:
                    # fulfill order
                    logger.info(f"Order {most_profitable[0]} assigned to {courier_state.original.id}")
                    order = orders[most_profitable[0]]
                    courier_state.current_location = order.dropoff_location
                    courier_state.current_time = most_profitable[2]
                    unfulfilled_orders.remove(most_profitable[0])
                    actions += [
                        RouteAction(courier_state.original.id,
                                    action_type=RouteActionType.pickup,
                                    order_id=order.id,
                                    point_id=order.pickup_point_id, depot_id=None),
                        RouteAction(courier_state.original.id,
                                    action_type=RouteActionType.dropoff,
                                    order_id=order.id,
                                    point_id=order.dropoff_point_id, depot_id=None),
                    ]
                else:
                    logger.info(f"Order not found for {courier_state.original.id}")
            processed_couriers += 1
        return actions
