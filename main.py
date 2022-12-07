#!/usr/bin/env python3

import tm
import time
if __name__ == '__main__':
    program  = tm.parse_tm_from_stdin()
    machine = tm.TuringMachine(program, '000111111111')
    while not machine.step():
        continue
    print(machine.halt_state)

