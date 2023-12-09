from functools import cache
import random
from typing import List, Dict, TypeVar, Tuple, Iterable

from model import User, Allocation


class LocalSearchAllocator:
    def __init__(self, steps=1000, max_options=50, n=5):
        self.steps = steps
        self.max_options = max_options
        self.n = n
        ...

    def allocate(self, participants: List[User]) -> List[Allocation]:
        num_categories = len({item for participant in participants for item in participant.can_receive})
        best_allocations, best_score = None, float('-inf')
        for _ in range(self.n):
            curr_score = 0
            allocations: Dict[User, User] = {}

            # randomly allocate initial allocations
            shuffled_participants = random.sample(participants, len(participants))
            while any(giver == reciever for giver, reciever in zip(participants, shuffled_participants)):
                shuffled_participants = random.sample(participants, len(participants))
            for giver, receiver in zip(participants, shuffled_participants):
                allocations[giver] = receiver
                curr_score += _calculate_allocation_score(giver, receiver, num_categories)

            for _ in range(self.steps):
                target_participant = random.choice(participants)
                potential_swaps = random.sample(participants, min(len(participants), self.max_options))
                potential_scores = [
                    _calculate_allocation_score(giver=target_participant, receiver=allocations[pot_participant], num_categories=num_categories)
                    + _calculate_allocation_score(giver=pot_participant, receiver=allocations[target_participant], num_categories=num_categories)
                    for pot_participant in potential_swaps
                ]
                swap_target, swapped_score = _argmax(potential_swaps, potential_scores)
                old_score = _calculate_allocation_score(target_participant, allocations[target_participant], num_categories) \
                            + _calculate_allocation_score(swap_target, allocations[swap_target], num_categories)
                if swapped_score > old_score:
                    old_allocations = allocations.copy()
                    curr_score = curr_score + swapped_score - old_score
                    allocations[target_participant] = old_allocations[swap_target]
                    allocations[swap_target] = old_allocations[target_participant]

            if curr_score > best_score:
                best_score = curr_score
                best_allocations = allocations
        return [Allocation(giver, receiver) for giver, receiver in best_allocations.items()]


@cache
def _calculate_allocation_score(giver: User, receiver: User, num_categories: int) -> float:
    if giver == receiver:
        return float('-inf')
    else:
        return -(num_categories - len(set(giver.can_give).intersection(set(receiver.can_receive)))) ** 2


_T = TypeVar('_T')


def _argmax(entities: Iterable[_T], scores: Iterable[int]) -> Tuple[_T, int]:
    max_score = float('-inf')
    best_entity = None
    for entity, score in zip(entities, scores):
        if score > max_score:
            max_score = score
            best_entity = entity
    return best_entity, max_score


if __name__ == '__main__':
    users = [
        User('foo', can_give=('art', 'writing'), can_receive=('art',)),
        User('baz', can_give=('writing',), can_receive=('writing',)),
        User('qux', can_give=('art', 'writing', 'music'), can_receive=('art', 'writing', 'music')),
        User('quux', can_give=('art', 'music'), can_receive=('art',))
    ]

    lsa = LocalSearchAllocator()
    allocations = lsa.allocate(users)
    print('------')
    for allocation in allocations:
        print(allocation)
