#!/usr/bin/env python3

import collections

try:
    import ev3dev.ev3 as ev3
except ImportError:
    import rpyc
    conn = rpyc.classic.connect('10.42.0.156')  # host name or IP address of the EV3
    ev3 = conn.modules['ev3dev.ev3']            # import ev3dev.ev3 remotely


from robot import Controller, mainloop


LR = collections.namedtuple('LR', ['left', 'right'])


class Vehicle_SideMotors(Controller):
    """A vehicle with 2 motors, one on each side, which can be steered by running the motors at different speeds."""
    def __init__(self, motors, default_speed=300):
        """motors: (left, right)"""
        self.motors        = motors
        self.default_speed = default_speed

    def halt(self):
        for i in [0,1]:
            self.motors[i].stop(stop_action='coast')

    def forward(self, speed=None):
        """Command to go forward. Speed sets the motor rotational speed in deg/s."""
        if not speed: speed = self.default_speed
        for i in [0,1]:
            self.motors[i].run_forever(speed_sp=speed)

    def turn(self, clockwise=False, speed=None, offset=0):
        """Command to start turning. Offset will make it also go forward/backward while turning."""
        if not speed: speed = self.default_speed
        Woomba.motors[int(clockwise)  ].run_forever(speed_sp=self.motors_dir*(speed-offset)*-1)
        Woomba.motors[1-int(clockwise)].run_forever(speed_sp=self.motors_dir*(speed+offset))

    def turn_right(self, **kwargs):
        self.turn(clockwise=True, **kwargs)

    def turn_left(self, **kwargs):
        self.turn(clockwise=False, **kwargs)


class Woomba(Vehicle_SideMotors):
    # TODO in theory I could also abstract away the proximity thing :D
    PROXIMITY_NUM_SAMPLES = 5

    def __init__(self):
        self.proximity_samples = collections.deque([50])  # just put in a sane sentinel

        self.ir = ev3.InfraredSensor(mode='IR-PROX')
        # the motors are mounted backwards, therefore polarity='inversed'
        motors = [ev3.LargeMotor(m, polarity='inversed') for m in ('outA', 'outD')]
        Vehicle_SideMotors.__init__(self, motors)

    def proximity(self):
        self.proximity_samples.append(self.ir.proximity)
        if len(self.proximity_samples) > self.PROXIMITY_NUM_SAMPLES: self.proximity_samples.popleft()
        return sum(self.proximity_samples)/len(self.proximity_samples)

    def step(self):
        prox = self.proximity()
        print('proximity', prox)
        if prox < 20:  # obstacle
            self.turn_left(offset=-50)
        else:
            self.forward()


if __name__ == '__main__':
    mainloop(Woomba())
