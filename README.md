# lego-wet-roomba
Lego Mindstorms EV3-based Roomba-like creature that runs around with a wet towel. Won't hit walls and won't fall off.

TODO pictures

### Build the Hardware

The files `woomba*.lxf` can be opened in [Lego Digital Designer](http://ldd.lego.com/en-us/). (It runs fine under Wine.)

Note: While it can generate a building guide, it is a little silly and sometimes it requires extra dimensions to get the bricks to their place. Just following that generated guide will not work.

There are several versions of the build. None is considered final.


### Make the software run

I use [ev3dev](www.ev3dev.org/docs/getting-started/) with Python, not the original LEGO Mindstorms software. You need ev3dev to use my software. Or you can make your own!

Note: Getting ev3dev is not hard, and no dangerous procedures are involved -- you install it on a microSD card, the brick cannot be bricked ;-)

When you have ev3dev, just scp `woomba/main.py` to the Woomba and run it (via ssh or from Brickman).

Or check out `woomba/woomba.py` for a newer, better, also unfinished version, which can also run using [RPyC](https://python-ev3dev.readthedocs.io/en/stable/rpyc.html). It has nice abstractions!

The version in `woomba/main.py`:

- is a terrible hack
- turns when it detects an obstacle
- turns when it detects lack of floor BUT...
- **is NOT safe to run in places where it can fall, because the floor detection is unreliable**
  - this is because the sensor's position is suboptimal -- the model needs to be changed

The version in `woomba/woomba.py` supersedes `woomba/main.py`, it is much less
of a terrible hack, but it does **not** consider avoiding falling at this point.

BTW, the setup of my EV3 is [here](https://github.com/AnotherKamila/cdist-personal/blob/master/manifest/init#L28). The Python specifics are in [here](https://github.com/AnotherKamila/cdist-personal/blob/master/manifest/python).

---------------------------------------------------------------------

Questions, suggestions, anything? Pull requests are welcome!
