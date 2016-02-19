import pyglet
import random
import math
import boid
import gui

WINDOW_X = 1600;
WINDOW_Y = 940;

sepW = 45
alignW = 30
cohW = 20
avoidW = 80
fleeW = 60

gui = gui.GUI(200)
window = pyglet.window.Window(WINDOW_X, WINDOW_Y)

level_label = pyglet.text.Label(text="Cock Flocking: M, M, M",
                                x=3, y=920, anchor_x="left")
@window.event
def on_draw():
    window.clear()
    gui.batch.draw()
    level_label.draw()

def update(dt):
    boidz_pos_vel = []
    predz_pos_vel = []
    ob_xy = []

    for ob in gui.obstacles:
        ob_xy.append((ob.x,ob.y))

    for boid in gui.boid_sprites:
        boid.obstacles = ob_xy
        boidz_pos_vel.append((boid.x,boid.y,boid.velocity_x,boid.velocity_y))

    for pred in gui.predators:
        pred.obstacles = ob_xy
        predz_pos_vel.append((pred.x,pred.y,pred.velocity_x,pred.velocity_y))

    for boid in gui.boid_sprites:
        boid.boids_pos_vel = boidz_pos_vel
        boid.preds_pos_vel = predz_pos_vel
        boid.update(dt, sepW, alignW, cohW, avoidW, fleeW)

    for pred in gui.predators:
        pred.preds_pos_vel = predz_pos_vel
        pred.boids_pos_vel = boidz_pos_vel
        pred.update(dt, 0, 0, 20, 60, 10)


@window.event
def on_key_press(symbol, modifiers):

    global level_label
    global sepW
    global alignW
    global cohW

    if symbol == pyglet.window.key.Q:
        level_label = pyglet.text.Label(text="Cock Flocking: L, L, H",
                                        x=3, y=920, anchor_x="left")
        sepW = 10
        alignW = 10
        cohW = 70

    elif symbol == pyglet.window.key.W:
        level_label = pyglet.text.Label(text="Cock Flocking: L, H, L",
                                        x=3, y=920, anchor_x="left")
        sepW = 15
        alignW = 70
        cohW = 15
    elif symbol == pyglet.window.key.E:
        level_label = pyglet.text.Label(text="Cock Flocking: H, L, L",
                                        x=3, y=920, anchor_x="left")
        sepW = 70
        alignW = 10
        cohW = 10
    elif symbol == pyglet.window.key.R:
        level_label = pyglet.text.Label(text="Cock Flocking: L, H, H",
                                        x=3, y=920, anchor_x="left")
        sepW = 10
        alignW = 50
        cohW = 50
    elif symbol == pyglet.window.key.T:
        level_label = pyglet.text.Label(text="Cock Flocking: H, L, H",
                                        x=3, y=920, anchor_x="left")
        sepW = 50
        alignW = 10
        cohW = 30
    elif symbol == pyglet.window.key.Y:
        level_label = pyglet.text.Label(text="Cock Flocking: H, H, H",
                                        x=3, y=920, anchor_x="left")
        sepW = 70
        alignW = 70
        cohW = 70
    elif symbol == pyglet.window.key.U:
        level_label = pyglet.text.Label(text="Cock Flocking: M, M, M",
                                        x=3, y=920, anchor_x="left")
        sepW = 45
        alignW = 30
        cohW = 20
    elif symbol == pyglet.window.key.A:
        gui.add_obstacle()
    elif symbol == pyglet.window.key.S:
        gui.add_predator()
    elif symbol == pyglet.window.key.Z:
        gui.obstacles = []
    elif symbol == pyglet.window.key.X:
        gui.predators = []
    elif symbol == pyglet.window.key.D:
        sepW += 1
    elif symbol == pyglet.window.key.C:
        sepW -= 1
    elif symbol == pyglet.window.key.F:
        alignW +=1
    elif symbol == pyglet.window.key.V:
        alignW -=1
    elif symbol == pyglet.window.key.G:
        cohW += 1
    elif symbol == pyglet.window.key.B:
        cohW -= 1

pyglet.clock.schedule_interval(update, 1/60.0)

if __name__ == '__main__':
    pyglet.app.run()
