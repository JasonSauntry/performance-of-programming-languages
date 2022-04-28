#!/usr/bin/env python3
import pprint
import random as rand
from dataclasses import dataclass
from typing import Optional

from common import get_number
from common import run_bench
from common import timef

pp = pprint.PrettyPrinter().pprint


@dataclass
class HeapNode:
    value: any
    left: Optional["HeapNode"] = None
    right: Optional["HeapNode"] = None
    __empty: bool = False

    def push(self, new_value: any):
        if new_value >= self.value:
            if self.left is None:
                self.left = HeapNode(new_value)
            elif self.right is None:
                self.right = HeapNode(new_value)
            else:
                expand_side = (
                    self.left if self.left.depth < self.right.depth else self.right
                )
                expand_side.push(new_value)
        else:
            old_value = self.value
            old_right = self.right
            old_left = self.left

            self.value = new_value
            self.right = None
            self.left = HeapNode(old_value, old_left, old_right)

    def pop(self) -> any:
        ret = self.value
        if self.left and self.right:
            pop_side = self.left if self.left.value < self.right.value else self.right
            self.value = pop_side.pop()
        elif self.left:
            self.value = self.left.value
            self.right = self.left.right
            self.left = self.left.left
        elif self.right:
            self.value = self.right.value
            self.left = self.right.left
            self.right = self.right.right
        else:
            self.__empty = True

        if self.left and self.left.empty:
            self.left = None
        if self.right and self.right.empty:
            self.right = None

        return ret

    @property
    def depth(self) -> int:
        ldepth = self.left.depth + 1 if self.left else 1
        rdepth = self.right.depth + 1 if self.right else 1

        return max(ldepth, rdepth)

    @property
    def empty(self) -> bool:
        return self.__empty


@dataclass
class Heap:
    head_node: Optional[HeapNode] = None

    def push(self, val: any):
        if self.head_node:
            self.head_node.push(val)
        else:
            self.head_node = HeapNode(val)

    def pop(self):
        if self.head_node:
            ret = self.head_node.pop()
            if self.head_node.empty:
                self.head_node = None
            return ret
        else:
            raise ValueError("Popped empty heap")

    def empty():
        return self.head_node is not None

    def pop_all(self):
        while self.head_node:
            yield self.pop()


def act(size: int) -> int:
    unsorted = [get_number() for i in range(size)]

    def sort():
        h = Heap()
        for e in unsorted:
            h.push(e)

        return [e for e in h.pop_all()]

    time, s = timef(lambda: sort())

    if len(s) < 50:
        pp(s)
    else:
        print(s[rand.randint(0, len(s) - 1)])

    return time


if __name__ == "__main__":
    run_bench(
        lambda size: act(size),
        description="Sorting floats using a heap",
        size_help="Number of floats to sort",
    )
