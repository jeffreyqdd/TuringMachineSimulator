#!/usr/bin/env python3
from sys import stdin
from typing import List, Tuple, Dict
from collections import namedtuple
"""
turing machines are represented using dictionaries:
key = current_state + symbol under head
value = Action(priority, new symbol, direction, next_state)
"""
Action = namedtuple('Action', 'priority, new_symbol, direction, next_state')

class TuringMachine:
    def __init__(self, tm: Dict[str, Action], input: str, head_start:int = 0,
                 starting_state:str = "0"):
        self.instructions = tm
        input = input.replace(' ', '_')
        self.tape = list(input)

        self.head_idx = head_start
        self.current_state = starting_state
        self.halt_state = "running"

    def step(self):
        current_symbol = self.tape[self.head_idx]
        action = None
        action1 = None
        key = gen_tm_key(self.current_state, current_symbol)
        if key in self.instructions:
            action = self.instructions[key]
        key = gen_tm_key(self.current_state, '*')
        if key in self.instructions:
            action1 = self.instructions[gen_tm_key(self.current_state, '*')]

        if action is None and action1 is None:
            print('Reached state that does not exist.')
            print(f'current state: {self.current_state}, symbol on tape: {current_symbol}')
            exit()
        else:
            if action is None and action1 is not None:
                action = action1
            elif action is not None and action1 is not None:
                if action1.priority < action.priority:
                    action = action1
            assert action is not None
            #print(f'state: {self.current_state}, head: {(self.head_idx, current_symbol)}, action: {action}')
            if action.new_symbol != '*':
                self.tape[self.head_idx] = action.new_symbol

            if action.direction == 'l':
                if self.head_idx == 0:
                    self.tape.insert(0, '_')
                else:
                    self.head_idx -= 1;
            elif action.direction == 'r':
                if self.head_idx == len(self.tape) - 1:
                    self.tape.append('_')
                self.head_idx += 1;

            self.current_state = action.next_state

            if 'halt' in self.current_state:
                self.halt_state = self.current_state
                return True
            return False

def gen_tm_key(current_state: str, content_under_head: str) -> str:
    return f'{current_state}%%%{content_under_head}'

def gen_tm_value(priority: int, new_symbol: str, direction: str, next_state: str) -> Action:
    return Action(priority, new_symbol, direction, next_state)

def parse_tm(transition_functions : List[Tuple[int, str]]) -> Dict[str, Action]:
    """ transition functions is a single string, space separated/
    - symbol under head: x
    - replace symbol under head with: y

    current_state x y direction next_state
    """
    tm = {}
    for fun in transition_functions:
        yeet = fun[1].split(' ')[:5]
        s0, x, y, d, s1 = yeet
        action : Action= gen_tm_value(fun[0], y, d, s1)
        if action.next_state == '*':
            print(f'parse error on line {fun[0]+1}: cannot use * as next_state')
            exit()
        tm[gen_tm_key(s0, x)] = action

    return tm

def parse_tm_from_stdin() -> Dict[str, Action]:
    x = []
    for idx, line in enumerate(stdin):
        line = line.strip('\n').strip(' ')
        if line == '':
            continue # avoid blank lines
        if line[0] == ';':
            continue # skip comments
        x.append((idx,line))

    return parse_tm(x)
