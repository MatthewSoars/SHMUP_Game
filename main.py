# Importing the functions
import pygame  # Imports the Pygame Module
import random  # Imports the Random Module

# Pre Defined settings
width = 480  # Sets the width of the window
height = 600  # Sets the height of the window
fps = 60  # Sets the Max FPS/ Target FPS

# Defines the Colours needed
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Main Pygame Startup
pygame.init()  # Initalizes all imported pygame modules
pygame.mixer.init()  # Initializes the mixer module
screen = pygame.display.set_mode((width, height))  # Initialize a windo or screen for displau
pygame.display.set_caption("SHMUP")  # Set the current window caption
clock = pygame.time.Clock()  # Updates the clock

font_name = pygame.font.match_font('arial')  # Find a specific font on the system


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)  # Create a new Font object from a file
    text_surface = font.render(text, True, WHITE)  # Draw text on a new Surface
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Player Class of moving sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Simple base class for visible game objects
        self.image = player_img  # Assigns the object an image in order to give it graphics
        self.image = pygame.transform.scale(player_img, (50, 38))  # Resize to new resolution
        self.image.set_colorkey(BLACK)  # Sets the colour to make transparent (Taking out the background)
        # Defines the hit box of the player sprite
        self.rect = self.image.get_rect()  # Defines the rectangular hit box of a sprite
        self.radius = int(self.rect.width * .85 / 2)  # Defines the circle hit box for the sprite
        # Centers the PLayer Sprite to the bottom of the Screen into the starting position
        self.rect.centerx = width / 2  # Centers the sprite to the middle of the screen
        self.rect.bottom = height - 10  # Puts the sprite at the bottom of the window
        self.speedx = 0  # Sets the starting X axis speed to zero
        self.shield = 100  # Sets the Inital Shield Health
        self.shoot_delay = 250  # How long Until the player can shoot again
        self.last_shot = pygame.time.get_ticks()  # This will be used to calculate the time since the player last shot
        self.lives = 3  # Defines how many lives the player has
        self.hidden = False  # If Player sprite is hidden or not
        self.hide_timer = pygame.time.get_ticks()  # Calculate how long the sprite has been hidden

        # Game Logic Player Movement

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:  # Unhide if hidden after timer is complete
            self.hidden = False  # UnHides the player sprite
            self.rect.center = (width / 2, height - 30)  # Recenters the player sprite
        self.speedx = 0  # Sets the xaxis speed to zero
        # Detects when a key is pressed
        keystate = pygame.key.get_pressed()  # Triggers when any key is pressed
        if keystate[pygame.K_LEFT]:  # Triggers when the left key is pressed
            self.speedx = -8  # Moves player sprite to the left
        if keystate[pygame.K_RIGHT]:  # Triggers when the right key is pressed
            self.speedx = 8  # Moves player sprite to the right
        self.rect.x += self.speedx  # Moves the hitbox with the sprite
        # Stops allowing the player to move if the sprite is off the screen
        if self.rect.right > width:  # If the players x cord is more then the width of the screen in right direct
            self.rect.right = width  # Stops the player sprite from moving
        if self.rect.left < 0:  # Checks to see if the player sprite is outside the screen area in the left
            self.rect.left = 0  # Stops the player sprite from moving
        if keystate[pygame.K_SPACE]:  # Checks to see if the space bar is pressed
            self.shoot()  # Calls the function to shoot

    # Spawns a bullet at the position of the player
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)  # Centers the bullet sprite on the player sprite
            all_sprites.add(bullet)  # Adds the bullet sprite to the sprite list
            bullets.add(bullet)  # Adds multiple bullets
            shootsound.play()  # Plays the premade shoot sound

    # Called when the player temporarily dies after shield <=0
    def hide(self):  # To temporarily hide the player after shield <=0
        self.hidden = True  # Hides the player sprite
        self.hide_timer = pygame.time.get_ticks()  # Starts a timer to calculate how long the player has been hidden
        self.rect.center = (
        width / 2, height + 200)  # Takes the player sprite off the screen so i cant be hit by metors while dead


"""Enemy Class For Sprite
Rect is a pygame object for storing rectangular coordinates"""


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Simple base class for visible game objects
        self.image_orig = meteor_img  # Sets the sprite image to the imported metor img
        self.image_orig.set_colorkey(BLACK)  # Sets the background colour of the object
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()  # Sets a hit box rectangle to be munipulated into the shape of the mob
        self.radius = int(self.rect.width / 2)  # Sets the hitbox to a circle around the mob
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) --Used to see the hit box if i need to fix
        # Movements of mob is randomised within the next part of the code
        self.rect.x = random.randrange(width - self.rect.width)  # Randomises Movements within the x axis
        self.rect.y = random.randrange(-100, -40)  # Randomises movements within the y axis
        self.speedy = random.randrange(1, 8)  # Randomises Speed in the Y Axis
        self.speedx = random.randrange(-3, 3)  # Randomises Speed in the X Axis
        self.rot = 0  # Sets orginal rotation of the mob
        self.rot_speed = random.randrange(-8, 8)  # Sets the rotation speed in the function
        self.last_update = pygame.time.get_ticks()  # Gets the time in milliseconds

    # Function which rotates the mobs randomly
    def rotate(self):
        now = pygame.time.get_ticks()  # Gets the time in milliseconds
        if now - self.last_update > 50:  # If an update hasnt happened in a certain number of milliseconds
            self.last_update = now  # Sets the most recent updates time
            self.rot = (
                               self.rot + self.rot_speed) % 360  # Uses the combined rotation speed and current rotation to rotate the mob randomly
            self.image = pygame.transform.rotate(self.image_orig, self.rot)  # Rotates the sprite using the calcs
            old_center = self.rect.center  # Sets the old center of the mob
            self.rect = self.image.get_rect()  # Rotates the hitbox
            self.rect.center = old_center  # Rotates to the correct orination

    # Updates the position of the mob
    def update(self):
        self.rotate()  # Calls for the rotatation of mob
        self.rect.x += self.speedx  # Makes the hit box move with the sprite in xaxis
        self.rect.y += self.speedy  # Makes the hit box move with the sprite in yaxis
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:  # If the mob touches the border of the screen
            self.rect.x = random.randrange(
                width - self.rect.width)  # Re sets mob on a diffrent randomised direction in xaxis
            self.rect.y = random.randrange(-100, -40)  # Resets the mob in a diffrent randomised direction in y axis
            self.speedy = random.randrange(1, 8)  # Randomises the speed in the y axis


# Bullet Class that shoots from player sprite
# .Rect is a pygame object for storing rectangular coordinates
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # Simple base class for visible game objects
        self.image = bullet_img  # Sets the bullet to the image in the files
        self.image.set_colorkey(BLACK)  # Sets the background colour as black and removes the background
        self.rect = self.image.get_rect()  # Sets the rect to the size of the rectangle
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10  # Sets the speed of the bullet

    # Movement of bullet
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):  # Class for explosion
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size  # Sets the size
        self.image = explosion_anim[self.size][0]  # Sets the explosion size
        self.rect = self.image.get_rect()  # Positions the explosion
        self.rect.center = center  # Centers the explosion on the metor
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100  # Sets the bar length
    BAR_HEIGHT = 10  # Sets the bar Height
    fill = (pct / 100) * BAR_LENGTH  # Decides how much of the par to fill
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # Creates a rectangle around the bar
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)  # Fills the rectangle
    pygame.draw.rect(surf, GREEN, fill_rect)  # Makes the bar green
    pygame.draw.rect(surf, WHITE, outline_rect, 2)  # Makes the rectangle white


def draw_lives(surf, x, y, lives, img):  # Draws an image of the ship at the top of the screen to display lives
    for i in range(lives):  # Displays the amount of ships corresponding to the amount of lives the player has left
        img_rect = img.get_rect() # Gets the image for the small spaceship
        img_rect.x = x + 30 * i # Positions the small spaceships next to each other in a line X Axis
        img_rect.y = y # Puts them all on the same Y Axis
        surf.blit(img, img_rect) # Blits the surface refreshing the screen


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)  # Adds the mobs according to the max amount


# Load all game graphics
background = pygame.image.load('img/starfield.png').convert()  # Loads the image for background
background_rect = background.get_rect()  # Makes the starfield the background
player_img = pygame.image.load("img/playerShip1_orange.png").convert()  # Loads the image for the spaceship
player_mini_img = pygame.transform.scale(player_img, (25, 19))  # Loads the playership image and scales it down
player_mini_img.set_colorkey(BLACK)  # Sets the background colour to remove as black
meteor_img = pygame.image.load("img/meteorBrown_med1.png").convert()  # Loads the image for the mob
bullet_img = pygame.image.load("img/laserRed16.png").convert()  # Loads the image for the Laser
explosion_anim = {}  # Starts a list for explosions
explosion_anim['lg'] = []  # List of Large explosions
explosion_anim['sm'] = []  # List of small explosions
explosion_anim['player'] = []

for i in range(9):
    filename = 'img/regularExplosion0{}.png'.format(i)  # Sets the current exlosion file
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)  # Removes the background
    img_lg = pygame.transform.scale(img, (75, 75))  # Scales the large explosion
    explosion_anim['lg'].append(img_lg)  # Applys transformation
    img_sm = pygame.transform.scale(img, (32, 32))  # Scales the small explosion
    explosion_anim['sm'].append(img_sm)  # Applys transformation
    filename = 'img/sonicExplosion0{}.png'.format(i)  # Sets the current sonic exlosion file
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)  # Removes the background
    explosion_anim['player'].append(img)

for i in range(9):
    filename = 'img/regularExplosion0{}.png'.format(i)  # Sets the current exlosion file
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)  # Removes the background
    img_lg = pygame.transform.scale(img, (75, 75))  # Scales the large explosion
    explosion_anim['lg'].append(img_lg)  # Applys transformation
    img_sm = pygame.transform.scale(img, (32, 32))  # Scales the small explosion
    explosion_anim['sm'].append(img_sm)  # Applys transformation

# Loads Sounds
shootsound = pygame.mixer.Sound('sound/pew.wav')  # Loads the sound for the lazer
ExpSound = pygame.mixer.Sound('sound/expl3.wav')  # Loads the expolosion sound
# Plays background music of either arctic monkeys or catfish and the bottle men 8bit versions
randombackgroundmusic = random.randint(1, 2)
if randombackgroundmusic == 1:
    pygame.mixer.music.load('sound/BackgroundMusic2.mp3')  # Loads arctic monkeys song
elif randombackgroundmusic == 2:
    pygame.mixer.music.load('sound/BackgroundMusic2 .mp3')  # loads Catfish and the bottlemen song
pygame.mixer.music.set_volume(0.4)  # Sets the music volume

# Creates a sprite group and adds a player sprite
all_sprites = pygame.sprite.Group()  # Creates a sprite group
mobs = pygame.sprite.Group()  # Adds mobs to the sprite group
bullets = pygame.sprite.Group()  # Adds bullet to the sprite group
player = Player()  # Changes Player() to player
all_sprites.add(player)  # Adds Player to the sprite group

score = 0
pygame.mixer.music.play(loops=-1)  # Loops the music

for i in range(8):  # Sets the limit for mobs on screen
    newmob()

# Game Loop
running = True
while running:
    # How many times the screen refreshes per second
    clock.tick(fps)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Triggered when a player presses a button
            if event.key == pygame.K_SPACE:  # Triggered when the SpaceBar is pressed
                player.shoot()  # Calls the function to shoot

    # Update
    all_sprites.update()  # Calls the update method on contained Sprites

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius  # Calculates how many points are allocated per mob kill
        expl = Explosion(hit.rect.center, 'lg')  # Positions the expolosion on the screen
        all_sprites.add(expl)  # Adds the large explosion to the screen
        ExpSound.play()  # Plays the explosion sound
        newmob()  # Calls the function made to respawn the mob that has despawned

    # Check to see if a mob hits the player
    hits = pygame.sprite.spritecollide(player, mobs, True,
                                       pygame.sprite.collide_circle)  # Checks to see if their is a collision
    for hit in hits:
        player.shield -= hit.radius * 2  # The players Shield will be subtracted depending upon the radius
        expl = Explosion(hit.rect.center, 'sm')  # Positions the expolosion on the screen
        all_sprites.add(expl)  # Adds the small explosion to the screen
        newmob()  # Calls the function made to respawn the mob that has despawned
        if player.shield <= 0:  # When players shield is less than or equal to 0
            death_explosion = Explosion(player.rect.center,
                                        'player')  # Centers location of the death animation onto the player
            all_sprites.add(death_explosion)  # Calls the death animation
            player.hide()  # Calls the player hide function
            player.lives -= 1  # Minus one of the players lives
            player.shield = 100  # Resets the players shield to 100

    # If Player Dies And Expolosion has finished playing
    if player.lives <= 0 and not death_explosion.alive():
        running = False  # Stops the game from running after explosion has finished

    # Colouring the screen
    screen.blit(background, background_rect)
    all_sprites.draw(screen)  # Blit the Sprite images
    draw_text(screen, str(score), 18, width / 2, 10)  # Puts the current Score on the screen
    draw_shield_bar(screen, 5, 5, player.shield)  # Puts the current shield onto the screen
    draw_lives(screen, width - 100, 5, player.lives, player_mini_img) #Adds the lives to the screen
    # Updates the screen
    pygame.display.flip()
