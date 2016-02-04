import pyglet
import random
import math

class Boid(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Boid, self).__init__(*args, **kwargs)
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.boids_pos_vel = []
        self.preds_pos_vel = []

        self.sensing_radius = 50
        self.maxSpeed = 150

        self.obstacles = []

    def separation_force(self, neighbor_list):
        vx = 0
        vy = 0
        for boid in neighbor_list:
            distance_weight = (self.sensing_radius - boid[4])/self.sensing_radius
            vx = vx + distance_weight*boid[0]
            vy = vy + distance_weight*boid[1]

        return (vx/self.sensing_radius,vy/self.sensing_radius)

    def alignment_force(self, neighbor_list):
        vx = 0
        vy = 0
        number_of_neighbors = len(neighbor_list)
        for boid in neighbor_list:
            vx = vx + boid[2]
            vy = vy + boid[3]

        vx = vx/len(neighbor_list)
        vy = vy/len(neighbor_list)
        hyp = (math.sqrt(vx**2+vy**2))

        return (vx/hyp,vy/hyp)

    def cohesion_force(self, neighbor_list):
        distX = 0
        distY = 0
        for boid in neighbor_list:
            distX = distX + boid[0]
            distY = distY + boid[1]

        distX = distX/len(neighbor_list)
        distY = distY/len(neighbor_list)
        hyp = (math.sqrt(distX**2+distY**2))
        if (hyp==0):
            return(0,0)

        return (distX/hyp,distY/hyp)

    def avoid_force(self, obstacles):
        if (obstacles==[]):
            return (0,0)
        vx = 0
        vy = 0
        hyp = (math.sqrt(self.velocity_x**2+self.velocity_y**2))
        sensor = (
                self.x + (self.velocity_x/hyp)*2*self.sensing_radius,
                self.y + (self.velocity_y/hyp)*2*self.sensing_radius
            )
        sensor2 = (
                self.x + (self.velocity_x/hyp)*(self.sensing_radius/2),
                self.y + (self.velocity_y/hyp)*(self.sensing_radius/2)
            )
        for ob in obstacles:
            dist = math.sqrt((ob[0]-sensor[0])**2+(ob[1]-sensor[1])**2)
            dist2 = math.sqrt((ob[0]-sensor2[0])**2+(ob[1]-sensor2[1])**2)
            if(dist<90 or dist2<90):
                vx = vx + (ob[0]-self.x-self.velocity_x)
                vy = vy + (ob[1]-self.y-self.velocity_y)
                hyp = (math.sqrt(vx**2+vy**2))
                vx, vy = vx/hyp, vy/hyp
        return (vx,vy)

    def flee_force(self, preds):
        vx = 0
        vy = 0

        for pred in preds:
            vx = vx + pred[0]/pred[4]
            vy = vy + pred[1]/pred[4]

        return (vx,vy)

    def check_bounds(self):
        min_x = -self.image.width/2
        min_y = -self.image.height/2
        max_x = 1600 + self.image.width/2
        max_y = 940 + self.image.height/2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

    def get_neighbors(self,r):
        neighbors = []
        for boid in self.boids_pos_vel:
            x_diff = self.x-boid[0]
            y_diff = self.y-boid[1]
            distance = math.sqrt(x_diff**2+y_diff**2)
            if distance < r and self.x != boid[0]:
                neighbors.append((x_diff, y_diff, boid[2], boid[3], distance))
        return neighbors

    def get_close_predators(self,r):
        preds = []
        for pred in self.preds_pos_vel:
            x_diff = self.x-pred[0]
            y_diff = self.y-pred[1]
            distance = math.sqrt(x_diff**2+y_diff**2)
            if distance < r and self.x != pred[0]:
                preds.append((x_diff, y_diff, pred[2], pred[3], distance))
        return preds

    def set_max_speed(self, vx, vy, hyp):
        new_vx = vx/hyp*self.maxSpeed
        new_vy = vy/hyp*self.maxSpeed

        return new_vx,new_vy

    def update(self, dt, sepW, alignW, cohW, avoidW, fleeW):
        neighbors = self.get_neighbors(self.sensing_radius)
        preds = self.get_close_predators(self.sensing_radius)

        if(len(neighbors)!=0):

            sepF = self.separation_force(neighbors)
            sepX = sepW * sepF[0]
            sepY = sepW * sepF[1]

            alignF = self.alignment_force(neighbors)
            alignX = alignW * alignF[0]
            alignY = alignW * alignF[1]

            cohF = self.cohesion_force(neighbors)
            cohX = cohW * cohF[0]
            cohY = cohW * cohF[1]

            avoidF = self.avoid_force(self.obstacles)
            avoidX = avoidW * avoidF[0]
            avoidY = avoidW * avoidF[1]

            fleeF = self.flee_force(preds)
            fleeX = fleeW * fleeF[0]
            fleeY = fleeW * fleeF[1]

            self.velocity_x = self.velocity_x + sepX + alignX - cohX - avoidX + fleeX
            self.velocity_y = self.velocity_y + sepY + alignY - cohY - avoidY + fleeY

            hyp = math.sqrt(self.velocity_x**2+self.velocity_y**2)
            if (hyp > self.maxSpeed):
                self.velocity_x, self.velocity_y = self.set_max_speed(self.velocity_x, self.velocity_y, hyp)


        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rotation = math.atan2(self.velocity_x, self.velocity_y)*180/math.pi
        self.check_bounds()
