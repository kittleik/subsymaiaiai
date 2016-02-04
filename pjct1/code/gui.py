import pyglet
import random
import math
import boid

pyglet.resource.path = ['../img']
pyglet.resource.reindex()


class GUI(object):

    def __init__(self, num_boids):
        self.batch = pyglet.graphics.Batch()
        self.boid_sprites = self.init_boids(num_boids)
        self.obstacles = []
        self.predators = []

    def init_boids(self, number_of_boids):
        boids = []
        for i in range(number_of_boids):
            new_boid = boid.Boid(
                    img=self.load_img("boid2.png"),
                    x=random.randint(0, 1600),
                    y=random.randint(0, 940),
                    batch = self.batch
                )
            new_boid.velocity_x = 200 - random.random()*400
            new_boid.velocity_y = 200 - random.random()*400

            boids.append(new_boid)
        return boids

    def add_obstacle(self):

        x = random.randint(80, 1520)
        y = random.randint(80, 860)
        obstacle = pyglet.sprite.Sprite(
                    img = self.load_img("obstacle.png"),
                    x=random.randint(80, 1520),
                    y=random.randint(80, 860),
                    batch = self.batch
            )

        self.obstacles.append(obstacle)


    def add_predator(self):

        new_pred = boid.Boid(
                img=self.load_img("pred.png"),
                x=random.randint(0, 1600),
                y=random.randint(0, 940),
                batch = self.batch
            )
        new_pred.maxSpeed = 100
        new_pred.sensing_radius = 150
        new_pred.velocity_x = 200 - random.random()*400
        new_pred.velocity_y = 200 - random.random()*400

        self.predators.append(new_pred)

    def load_img(self,img):

        image = pyglet.resource.image(img)
        image.anchor_y = image.width/2
        image.anchor_x = image.height/2

        return image
