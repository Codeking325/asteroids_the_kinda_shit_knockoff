import pygame
import utils_pygame
import os
import random 
class Config:
    """act as container for global variables"""
    skills = {}
    maxrank = 0
    points = []
    spent = [0]

class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        self.create_image()
        self.distance_traveled = 0 # in pixel
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)

    def _overwrite_parameters(self):
        """change parameters before create_image is called""" 
        pass

    def _default_parameters(self, **kwargs):    
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        if "color" not in kwargs:
            #self.color = None
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "hitpoints" not in kwargs:
            self.hitpoints = 100
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 10
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "bossnumber" not in kwargs:
            self.bossnumber = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "sticky_with_boss" not in kwargs:
            self.sticky_with_boss = True
        if "mass" not in kwargs:
            self.mass = 15
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = True
        if "edge_distance" not in kwargs:
            self.edge_distance = 0
        if "timelord" not in kwargs:
            self.timelord = False

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)

    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
            return
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
            return
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
            return
            
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
                    return
            if self.sticky_with_boss:
                boss = VectorSprite.numbers[self.bossnumber]
                #self.pos = v.Vec2d(boss.pos.x, boss.pos.y)
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
        #if self.timelord:
        self.pos += self.move * seconds 
        #else:
            #if PygView.bullettime:
            #    self.pos += self.move * seconds / 10
            #else:
              #  self.pos += self.move * seconds
        self.distance_traveled += self.move.length() * seconds 
        self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), -round(self.pos.y, 0) )
        self.move *= self.friction 


    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0 - self.edge_distance:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0 - self.edge_distance
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = Viewer.width + self.edge_distance 
        # -------- upper edge -----
        if self.pos.y  > 0 + self.edge_distance:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0 + self.edge_distance
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -Viewer.height - self.edge_distance
        # -------- right edge -----                
        if self.pos.x  > Viewer.width + self.edge_distance:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = Viewer.width + self.edge_distance
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0 - self.edge_distance
        # --------- lower edge ------------
        if self.pos.y   < -Viewer.height - self.edge_distance:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -Viewer.height - self.edge_distance
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0 + self.edge_distance
        
        
class Player(VectorSprite):
    
    
    def _overwrite_parameters(self):
        self.friction = 0.99  #1.0 = no friction
      #  self.radius = 8
        self.mass = 3000
        self.speed = 1
        self.rockets = 1
        self.bulletspeed = 188
        self.stop = True
        self.timer = 0
        self.regenhp = False
        self.targeted = True
        self.powers = False
        self.timelord = True
    
    def fire(self):
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        t = pygame.math.Vector2(70,0)
        t.rotate_ip(self.angle)
        sa = []
        d = 90 / (self.rockets + 1)
        start = -45
        point = start + d
        while point < 45:
            sa.append(point)
            point += d
        # in sa are the desired shooting angels for rockets
        for point in sa:
            v = pygame.math.Vector2(self.bulletspeed,0)
            v.rotate_ip(self.angle + point)
            v += self.move # adding speed of spaceship to rocket
            a = self.angle + point
            Rocket(pos=p+t, move=v, angle=a)
        
 
        
    
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        
        
    
    def move_forward(self, speed=1):
        v = pygame.math.Vector2(self.speed,0)
        v.rotate_ip(self.angle)
        self.move += v
        # --- engine glow ----
        #p = pygame.math.Vector2(-30,0)
        #p.rotate_ip(self.angle)
        #Muzzle_flash(pos=pygame.math.Vector2(self.pos.x, self.pos.y) + p, max_age=0.1, angle = self.angle+180)
       
        
    def turn_left(self, speed=3):
        self.rotate(speed)
        
    def turn_right(self, speed=3):
        self.rotate(-speed)    
    
    def create_image(self):
        #self.image = pygame.Surface((50,50))
        #pygame.draw.polygon(self.image, (0,255,0), ((0,0),(50,25),(0,50),(25,25)))
        #self.image.set_colorkey((0,0,0))
        #self.image.convert_alpha()
        self.image = Viewer.images["ship"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()        

class Viewer():
    width = 1024
    height = 800
    images = {}
    skillrect = [270,50]
    fontsize1 = 50
    


    def __init__(self, width=1024, height=800, fps=60):
        Viewer.width = width
        Viewer.height = height
        Viewer.topleft = (100,100)
        Viewer.bottomright = (50,50)
        self.fps = fps
        pygame.init()
        self.fontsize = 15
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.create_background()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        self.load_images()
        self.create_sprites()
        #self.run()
        skillrects = {}



    def create_sprites(self):
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.playergroup = pygame.sprite.Group()
        # gruppen zuweisen
        Player.groups = self.allgroup, self.playergroup
        
        #- create sprites
        self.player1 = Player(pos=pygame.math.Vector2(100,-100))
        
        
        

    def create_background(self, color1 = (0,0,0)):
        self.background = pygame.surface.Surface((self.width, self.height))
        self.background.fill(color1)
        self.stars()

    def stars(self, max_stars = 600):
        for i in range(0, max_stars):
            color = random.randint(128,150)
            pygame.draw.circle(self.background, (color, color, color,), (random.randint(0, self.width), random.randint(0, self.height)), random.randint(1,3))

    def load_images(self, folder='data', prefix=""):
        """load images from harddisk (folder 'data') and stores them into Viewer.images {"name": image object} """
        for root, dirs, files in os.walk(folder):
            for f in files:
                print("folder:", folder, "file:", f)
                if f.lower().startswith(prefix) and (f.lower().endswith(".png") or f.lower().endswith(".jpg")):
                    print("adding:",f)
                    Viewer.images[f[:-4].lower()] = pygame.image.load(os.path.join(folder, f)).convert_alpha()
            break
        print(Viewer.images)

    def run(self):
        self.playtime = 0
        running = True
        redraw = True
        

        while running:
            milliseconds = self.clock.tick(self.fps)  #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # ---- event handler -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            x = pygame.math.Vector2(2,2)
            keys = pygame.key.get_pressed()         
            if keys[pygame.K_LEFT]:
                self.player1.rotate(3)
                
            if keys[pygame.K_RIGHT]:
                self.player1.rotate(-3)
                
            if keys[pygame.K_UP]:
                self.player1.move_forward()
                
                
                    
                        
            # clear screen
            if redraw:
                self.screen.blit(self.background, (0, 0))
            #redraw = False
            #self.screen.blit(Viewer.images["ship"], (700, 300))
            self.allgroup.update(seconds)
            self.allgroup.draw(self.screen)
            
            

           
            fps_text = "FPS: {:5.3}".format(self.clock.get_fps())
            pygame.draw.rect(self.screen, (64, 255, 64), (Viewer.width - 110, Viewer.height - 20, 110, 20))
            utils_pygame.write(self.screen, text=fps_text, origin="bottomright", x=Viewer.width - 2, y=Viewer.height - 2,
                  font_size=16, bold=True, color=(0, 0, 0))
            pygame.display.flip()
        #---------------- end of run ----------
        pygame.quit()






if __name__ == "__main__":
    v = Viewer(1500, 770)
    

    v.run()
 
