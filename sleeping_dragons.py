import pgzrun, math
"""
Project No. Sleeping Dragons 
Control the hero by with the 4 arrow keys. Hero must collect 20 eggs from the dragon lair to win. If the hero 
is near a dragon when it's awake, the player loses a life. The game wends when the player runs out of lives or collects
enough eggs 

"""

#CONSTANTS
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
CENTER = CENTER_X,CENTER_Y
FONT_COLOR = (0,0,0)
EGG_TARGET = 20
HERO_START = 200,300
ATTACK_DIST = 200
DRAGON_WAKE_TIME = 2
EGG_HIDE_TIME = 2
MOVE_DISTANCE = 5

#globa vars
lives=3
eggs_collected = 0
#FLAGS
game_over = False
game_complete =False
reset_required = False

#dictionaries
easy_dragon = {
    "dragon": Actor('dragon-asleep',pos=(600,100)),
    'eggs': Actor('one-egg',pos=(400,100)),
    'egg_count':1,
    'egg_hidden': False,
    'egg_hide_counter': 0,
    'sleep_length': 10,
    'sleep_counter': 0,
    'wake_counter': 0
}
medium_dragon = {
    "dragon": Actor('dragon-asleep',pos=(600,300)),
    'eggs': Actor('two-eggs',pos=(400,300)),
    'egg_count':2,
    'egg_hidden': False,
    'egg_hide_counter': 0,
    'sleep_length': 7,
    'sleep_counter': 0,
    'wake_counter': 0
}
hard_dragon = {
    "dragon": Actor('dragon-asleep',pos=(600,500)),
    'eggs': Actor('three-eggs',pos=(400,500)),
    'egg_count':3,
    'egg_hidden': False,
    'egg_hide_counter': 0,
    'sleep_length': 4,
    'sleep_counter': 0,
    'wake_counter': 0
}
dragons_list = [easy_dragon,medium_dragon,hard_dragon]
hero = Actor('hero',pos=HERO_START)

def draw():
    screen.clear()
    screen.blit('dungeon',(0,0))
    if not game_over:
        hero.draw()
        draw_dragons(dragons_list)
        draw_counters(eggs_collected,lives)
    elif game_complete:
        screen.draw.text('YOU WON!', fontsize=60,center=CENTER,color=FONT_COLOR)
    else: #game over
        screen.draw.text('GAME OVER ', fontsize=60, center=CENTER, color=FONT_COLOR)



def draw_dragons(dragons_dict):
    for dragon in dragons_dict:
        dragon['dragon'].draw()
        if dragon['egg_hidden'] is False:
            dragon['eggs'].draw()

def draw_counters(eggs_collected,lives):
    screen.blit('egg-count',(0,HEIGHT-30))
    screen.draw.text(str(eggs_collected), fontsize=40,pos=(30, HEIGHT-30), color= FONT_COLOR)
    screen.blit('life-count', (60,HEIGHT-30))
    screen.draw.text(str(lives), fontsize=40, pos=(90, HEIGHT - 30), color=FONT_COLOR)

def subtract_life():
    global lives, reset_required, game_over
    lives -= 1
    if lives == 0 :
        game_over = True
    reset_required = False #var set to false since the hero is already at the starting position

def handle_dragon_collision():
    #reset hero back to original position and then call subtract_life function
    global reset_required
    reset_required = True
    animate(hero,pos=HERO_START,on_finished=subtract_life) #reset the hero back to original position after lives are subtracte

def check_egg_collision(dragon):
    global eggs_collected, game_complete, dragons_list
    if hero.colliderect(dragon['eggs']):
        dragon['eggs_hidden'] = True #hide the eggs now that they are collided with
        eggs_collected += dragon['egg_count']
        if eggs_collected>=EGG_TARGET:
            print('hello')
            game_complete=True

def check_dragon_collision(dragon):
    x_dist = hero.x-dragon['dragon'].x
    y_dist = hero.y-dragon['dragon'].y
    dist = math.hypot(x_dist,y_dist) #distance formula
    if dist<=ATTACK_DIST: #if the distance is smaller than the attack distance
        handle_dragon_collision() #the hero has gotten caught by the dragon and now must do something

def check_for_collision():
    #check for dragon and egg collosion
    for dragon in dragons_list:
        if dragon['egg_hidden'] == False: #eggs are not hiding right now
           check_egg_collision(dragon)
        if dragon['dragon'].image == 'dragon-awake' and reset_required == False:
            check_dragon_collision(dragon)


def update_sleeping_dragon(dragon):
    global dragons_list
    if dragon['sleep_counter']>=dragon['sleep_length']: #slept long enough now wake up
        dragon['dragon'].image = 'dragon-awake'
        #print('dragon {} s image is {}'.format(dragon['egg_count'],dragon['dragon'].image))
        dragon['sleep_counter'] = 0
    else:
        dragon['sleep_counter']+=1 #since the function is called every one second, you can add 1 to the slepe counter

def update_waking_dragon(dragon):
    #update the dragon if its been awake for too long
    if dragon['wake_counter']>=DRAGON_WAKE_TIME: #dragon goes to sleep
        dragon['dragon'].image = 'dragon-asleep'
        dragon['wake_counter'] = 0
    else: #dragon is still sleeping
        dragon['wake_counter'] +=1

def update_egg(dragon):
    #print(dragon['egg_count'])
    if dragon['egg_hidden'] == True:
        if dragon['egg_hide_counter'] >= EGG_HIDE_TIME: #time to hide the egg
            dragon['egg_hidden'] == False #egg is showing
            dragon['egg_hide_counter'] = 0
    else:
        dragon['egg_hide_counter'] += 1


def update_dragons():
    #loop through each dictionary of dragons and check if the dragon is asleep or awake
    for dragon in dragons_list:
        if dragon['dragon'].image == 'dragon-awake':
            update_waking_dragon(dragon)
        elif dragon['dragon'].image =='dragon-asleep':
            update_sleeping_dragon(dragon)
        update_egg(dragon)



def print_stats():

    for dragon in dragons_list:
        print('dragon #{}: wake_counter={} sleep_counter={}'.format(dragon['egg_count'],dragon['wake_counter'],dragon['sleep_counter']))
    print('----------------------------------------------------')


def update():
    if not game_over:
        if keyboard.up and hero.y>65:
            hero.y -=MOVE_DISTANCE
        if keyboard.right and hero.x<WIDTH:
            hero.x += MOVE_DISTANCE
        if keyboard.down and hero.y<HEIGHT:
            hero.y += MOVE_DISTANCE
        if keyboard.left and hero.x>0:
            hero.x -= MOVE_DISTANCE
        check_for_collision()

clock.schedule_interval(update_dragons,1)

pgzrun.go()