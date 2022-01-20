import pygame
from pygame.locals import *  #importing all the modules from pygame.locals
import time
import random
SIZE=20
BACKGROUND_COLOUR=(229,43,80)

class Apple:
    def __init__(self,parent_screen):  #constructor
        self.parent_screen=parent_screen
        self.image= pygame.image.load(r'Resources\apple.jpg').convert_alpha() #never use double quotes for path
        self.x=SIZE*3 
        self.y=SIZE*3 #setting the initial position of the image

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))  #this will draw the apple on the screen
        pygame.display.flip() 

    def move(self):
        self.x=random.randint(0,20)*SIZE
        self.y=random.randint(0,16)*SIZE

class Snake:
    def __init__(self,parent_screen,length): #constructor , we will pass our surface in parent_screen
        self.length=length
        self.parent_screen=parent_screen
        self.block= pygame.image.load(r'Resources\block.png').convert_alpha() #never use double quotes for path
        self.x=[SIZE]*length  
        self.y=[SIZE]*length # setting the initial position of the block
        self.direction='down'  #snake will start moving in downward direction in the biginning
        #these 3 parameters above are basically the default values at the starting of the game

    def draw(self): 
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip() 

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
    
    def move_up(self):
        self.direction='up'
       
    def move_down(self):
        self.direction='down'
       
    def move_left(self):
        self.direction='left'
       
    def move_right(self):
        self.direction='right'
       
        
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction=='up':
             self.y[0]-=SIZE
        if self.direction=='down':
             self.y[0]+=SIZE
        if self.direction=='left':
             self.x[0]-=SIZE
        if self.direction=='right':
             self.x[0]+=SIZE

        self.draw()
        
             

        
        
class Game:  #game initialising class
    def __init__(self):       #constructor
        pygame.init()  #initialise all pygame imported modules 
        pygame.display.set_caption("Snake Xenia")  #title of the game
        
        self.play_background_music()  #start playing the background music 

        self.surface=pygame.display.set_mode((1000,800)) #pygame.display.set_mode - initialises a screen or window for display #surface will be the variable for our game's screen
        #self.surface.fill(BACKGROUND_COLOUR)    #filling the background with white colour - in brackets rgb codes are written for a colour - eg- (255,255,255) for white
         #self. something is making it a class member so that it can be used in other functions as well
        self.snake=Snake(self.surface,1)  #creating a snake by calling the snake class
        self.snake.draw()  #draw the snake
        self.apple=Apple(self.surface)
        self.apple.draw()

    def is_collision(self,x1,y1,x2,y2):
        if(x1 >= x2 and x1 < x2+SIZE):
            if(y1 >= y2 and y1 < y2+SIZE):
                return True
        
        return False
    
    # def snake_crosses_boundary(self,x,y):
    #     if(x==0 or x==1000 or y==0 or y==800):
    #         return True
        
    #     return False
    
    def display_score(self):
        font=pygame.font.SysFont('ariel', 40)  #to display score on the screen
        score=font.render(f"Score: {self.snake.length}", True, (255,255,255))  #print the score which will be snake's length #(255,255,255) is rgb code for white colour
        self.surface.blit(score,(850,10))   
    
    def render_background(self):
        bg=pygame.image.load(r'Resources\background.jpg')
        self.surface.blit(bg,(0,0))

    def play_background_music(self):
        pygame.mixer.music.load("Resources/background music.mp3")
        pygame.mixer.music.play()

    def play_sound(self,sound_name):
        sound=pygame.mixer.Sound(f"Resources/{sound_name}.mp3") #putting the backslash will not add the sound file so be careful while adding path of a file/image
        pygame.mixer.Sound.play(sound) 
     
    def play(self):
        self.render_background()
        self.snake.walk()  #snake will walk on its own 
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        #snake eating the apple //snake colliding with the apple
        if(self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y)):
            self.play_sound("ding")   #playing the ding sound when snake eats the apple
            
            self.snake.increase_length()
            self.apple.move()
            
        #snake colliding with itself-game over
        for i in range(3,self.snake.length):
            if(self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i])):
                 self.play_sound("crash")    #playing the crash sound
            
                 raise "Collision occured"  #raising an exeption

         
        # #snake crosses the boundary 
        # if(self.snake_crosses_boundary(x[0],y[0])):
        #     self.play_sound("crash")    #playing the crash sound
            
        #     raise "Boundary crossed"  #raising an exeption
            
    def show_game_over(self):
        self.render_background()
        font=pygame.font.SysFont('ariel', 40)
        line1=font.render(f"Game is Over! Your Score is: {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(200,300))  #blit is used to show any message on the screen
        line2=font.render(f"To play again press Enter. To exit press Escape!",True,(255,255,255))
        self.surface.blit(line2,(200,350))  
        pygame.display.flip() #refreshes the UI or screen

        pygame.mixer.music.pause()  #pause the bg music after the game is over
  
    
    def game_reset(self):
        self.snake=Snake(self.surface,1)  
        self.snake.draw()  
        self.apple=Apple(self.surface)
        self.apple.draw()


    def run(self):
        running=True
        pause=False
        #event loop - used in all UI applications- eg run the game till the user presses escape
        while running: #an infinite loop as running is true
            for event in pygame.event.get():
                if event.type==KEYDOWN: #keydown means you are pressing the key
                    if event.key==K_ESCAPE:  #by pressing the escape button, you will exit from the game
                        running = False
                    if event.key==K_RETURN:  #RETURN is ENTER button
                       pause=False           #this will restart the game
                       self.game_reset()  
                       pygame.mixer.music.unpause()  #start the bg music again        
                    
                    if not pause:   #if paused, then do not consider the following commands
                        if event.key== K_UP:
                            self.snake.move_up()
                        if event.key== K_DOWN:
                            self.snake.move_down()
                        if event.key== K_LEFT:
                            self.snake.move_left()
                        if event.key== K_RIGHT:
                            self.snake.move_right()
                        
                    
                elif event.type== QUIT:
                    running=False  #this will quit end the while loop and quit the game
       
            try:
                if not pause: #game will be played only till pause remains False
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True   #game is paused here 
                
            time.sleep(0.1) #will produce a delay of 0.2 seconds otherwise snake will move very fast      
    
if __name__=="__main__": #main game starts from here

    game=Game()  
    game.run() 
    
