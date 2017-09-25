"""A Controller class for composable things controlling robots, plus utility stuff.

An important abstraction here is Command: a function that returns immediately.
It may issue sub-Commands to motors and such, and do quick calculations, but
it must be fast. It must not block, ever. It will be called often enough to
safely process inputs. Usually it will cause something to happen until another
Command is issued. Example: telling the motor to run is a Command.

Note that:

- EV3 motor commands are Commands
- Commands can call other Commands
- Commands *cannot* call non-Commands (would break the Command contract)
- all fast non-blocking functions are technically Commands, so those can be used

"""

import time

class Controller:
    """A base class for composable things that control robots.

    The methods step() and halt() must be implemented and their contracts
    *must* be fulfilled. See their docs.
    """
    def step(self):
        """Performs one step. Will be called often enough. Must return immediately.

        This function *must not* block. It is a Command.
        It can assume that it will be called frequently enough to process events in time.
        """
        return NotImplementedError

    def halt(self):
        """Stops motors and turns off all devices that need to be turned off when the program exits.

        Will be called at program exit. Must make sure that the robot is safe & stationary.
        """
        return NotImplementedError


# def step_coroutine(gen):
#     """Allows a generator/coroutine to be used as a Controller's step(). Helpful for sequential code.
#
#     You can then do the following:
#
#         # TODO this code cannot possibly be correct, fix it
#         def step(self):
#             # wait for 1s
#             now = time.now()
#             while (time.now() - now) < 1000:
#                 # do nothing
#                 yield  # "return" immediately to fulfill the Command contract
#
#             # after 1s, do something for 10s
#             now = time.now()
#             while (time.now() - now) < 10000:
#                 self.do_something()
#                 yield  # and yield control back to the main loop to fulfill Command contract
#     """
#     # TODO this code cannot possibly be correct, fix it and test with the above example
#     # one especially wrong thing is: what happens when the generator "runs out"? does it throw an exception? or what?
#     def step():
#         gen()
#     return step

def mainloop(controller, freq=50):
    """A convenience function that you can safely use as the main loop.

    controller: an instance of Controller (duck-typed). *Must* fulfill the Controller contracts.
    freq: the approximate frequency at which controller.step() will be called, in Hz. The actual frequency will be lower.
    """
    try:
        dt = 1.0/freq
        while True:
            controller.step()
            time.sleep(dt)
    except KeyboardInterrupt:
        pass
    finally:
        controller.halt()  # This is _very important_ :D
