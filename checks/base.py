from datetime import datetime, timedelta
from func_timeout import func_timeout
from func_timeout.exceptions import FunctionTimedOut
from threading import Event
from sys import stderr

class CheckState():
    def __init__(self, machine):
        self.machine = machine

    def set_state(self, state):
        self.machine.set_state(state)

    def get_name(self):
        return 'Unknown'

    def on_up(self):
        pass

    def on_down(self):
        pass

class CheckLimitState(CheckState):
    def __init__(self, machine, limit, limit_target):
        super().__init__(machine)
        self.consecutive = 1
        self.limit = limit
        self.limit_target = limit_target

    def inc_consecutive(self):
        self.consecutive += 1
        if self.consecutive >= self.limit:
            self.set_state(self.limit_target)

class CheckStateUp(CheckState):
    def __init__(self, machine):
        super().__init__(machine)

    def get_name(self):
        return 'UP'

    def on_down(self):
        self.set_state(CheckStateGoingDown)

class CheckStateDown(CheckState):
    def __init__(self, machine):
        super().__init__(machine)

    def get_name(self):
        return 'DOWN'

    def on_up(self):
        self.set_state(CheckStateGoingUp)

class CheckStateGoingUp(CheckLimitState):
    def __init__(self, machine):
        super().__init__(machine, machine.up_checks, CheckStateUp)

    def get_name(self):
        return 'GOING_UP'

    def on_up(self):
        self.inc_consecutive()

    def on_down(self):
        self.set_state(CheckStateDown)

class CheckStateGoingDown(CheckLimitState):
    def __init__(self, machine):
        super().__init__(machine, machine.down_checks, CheckStateDown)

    def get_name(self):
        return 'GOING_DOWN'

    def on_up(self):
        self.set_state(CheckStateUp)

    def on_down(self):
        self.inc_consecutive()

class BaseCheck():
    def __init__(self, config):
        self.name = config.get('name', 'Unnamed check')

        # Fast is used when the service is down, going down or going up
        self.interval_regular = config.getfloat('interval_regular', 5)
        self.interval_fast = config.getfloat('interval_fast', self.interval_regular / 2)
        self.check_timeout = config.getfloat('check_timeout', self.interval_fast)
        self.up_checks = config.getint('up_checks', 5)
        self.down_checks = config.getint('down_checks', 3)
        
        self.next_check = datetime.now()
        self.state = CheckStateDown(self)
        self.should_run_loop = False
        self.thread_wait_e = None
        
    def print(self, line):
        stderr.write('[%s] %s\n' % (self.name, line))
        stderr.flush()

    def set_state(self, StateCls):
        old_state = self.state
        self.state = StateCls(self)
        self.print("Going from %s to %s" % (old_state.get_name(), self.state.get_name()))

    def run(self):
        res = False
        try:
            res = func_timeout(func=self.check, timeout=self.check_timeout)
        except FunctionTimedOut:
            self.print('Check timed out')
        except Exception as e:
            self.print('Failed with exception: %s' % e)

        if res:
            self.state.on_up()
        else:
            self.state.on_down()

        if isinstance(self.state, CheckLimitState):
            self.print('%s [%i/%i]' % (self.state.get_name(), self.state.consecutive, self.state.limit))

        interval = self.interval_regular
        if not self.is_up():
            interval = self.interval_fast
        self.next_check = datetime.now() + timedelta(milliseconds=interval * 1000.0)
        return interval

    def run_loop(self):
        self.should_run_loop = True
        while self.should_run_loop:
            interval = self.run()
            self.thread_wait_e = Event()
            self.thread_wait_e.wait(timeout=interval)

    def stop_loop(self):
        self.should_run_loop = False
        if self.thread_wait_e:
            self.thread_wait_e.set()
            self.thread_wait_e = None

    def is_up(self):
        return isinstance(self.state, CheckStateUp)

    def should_check(self, at=None):
        if at == None:
            at = datetime.now()
        return self.next_check <= at
