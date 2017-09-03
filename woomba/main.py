#!/usr/bin/env python3

from collections import namedtuple
from time import sleep

try:
    import ev3dev.ev3 as ev3
except ImportError:
    from ev3mock import print_to_console_mock as ev3

LR = namedtuple('LR', ['left', 'right'])

# Note to self: a function is a Command when it is asynchronous (issues commands to motors + sensors and immediately returns).


class Woomba:
    motors = LR(ev3.LargeMotor('outA'), ev3.LargeMotor('outD'))
    motors_dir = -1 # the motors are mounted backwards => negative speed for going forward

    def forward(self, speed=300):
        """Command to go forward until another command is issued.

        Speed is in deg/s."""
        for i in [0,1]:
            Woomba.motors[i].run_forever(speed_sp=self.motors_dir*speed)

    def stop(self):
        for i in [0,1]:
            Woomba.motors[i].stop(stop_action='hold')

    # def safe_forward(self, speed=400):
    #     """Command to go forward until a

    def turn(self, clockwise=False, speed=300, offset=0):
        Woomba.motors[int(clockwise)  ].run_forever(speed_sp=self.motors_dir*(speed-offset)*-1)
        Woomba.motors[1-int(clockwise)].run_forever(speed_sp=self.motors_dir*(speed+offset))

    def clean(self):
        """Command to do the cleaning routine until another command is issued.

        Actually, this is nothing like a Command. TODO fix it!
        Only checks the sensors at the beginning, so that it can return right away -- must be called frequently enough!
        """
        color = ev3.ColorSensor()
        print('reflected_light_intensity', color.reflected_light_intensity)
        if color.reflected_light_intensity < 20:
            self.turn(offset=-400)
            sleep(0.1)
            return

        ir = ev3.InfraredSensor()
        print('proximity', ir.proximity)
        if ir.proximity < 20:
            self.turn()
            sleep(0.1)
            return

        self.forward()


    def main(self):
        """Woomba's main loop. This is a busy loop, _not_ a Command."""
        actions = [self.clean, self.stop]
        current_action = 0
        def toggle_action(ignore=False):
            """Toggles current action. Will not do anything if ignore == True."""
            if ignore: return
            current_action = 1 - current_action

        btn = ev3.Button()
        btn.on_enter = toggle_action

        while True:
            actions[current_action]()
            btn.process()
            sleep(0.01)

if __name__ == '__main__':
    woomba = Woomba()
    try:
        woomba.main()
    except KeyboardInterrupt:
        pass
    finally:
        woomba.stop()  # This is _very important_ :D
