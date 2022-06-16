import datetime
from core.state.state import State
from core.state.statetime import StateTime

N_TESTS = 100000

state_avg = 0
state_time_avg = 0

for i in range(N_TESTS):
    if i % (N_TESTS / 10) == 0:
        print(i / N_TESTS * 100, "%")
    t1 = datetime.datetime.now()
    s1 = State()
    t2 = datetime.datetime.now()
    st = StateTime(s1, 0.0)
    t3 = datetime.datetime.now()
    state_avg += (t2 - t1).microseconds
    state_time_avg += (t3 - t2).microseconds

state_avg /= N_TESTS
state_time_avg /= N_TESTS

print("Average time to create State: ", state_avg, " \u03BCs")
print("Average time to create StateTime: ", state_time_avg, " \u03BCs")