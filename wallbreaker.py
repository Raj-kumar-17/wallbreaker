import pygame
import math
import sys
import random
import cv2
import mediapipe as mp
import time


#Game controls
xval=0
yval=0

hcam=720
wcam=1280

def get_coordinates(x,y):
	global xval
	global yval
	xval=x
	yval=y
	
    
cam=cv2.VideoCapture(0)
cam.set(3,wcam)
cam.set(4,hcam)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils


ptime=0
ctime=0





#GAME
pygame.init()
pygame.display.set_caption("Wall-breaker by @rahulraj")
clock=pygame.time.Clock()

WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(144,24,27)
BLUE=(0,0,255)

# display height and width
sw=1000
sh=600

#Game initial status
life=3

img=pygame.image.load(r'D:\Rahul\Progams\py\Wall breaker\heart.jpg')
img0=pygame.transform.scale(img, (35,35))
img1=pygame.transform.scale(img, (35,35))
img2=pygame.transform.scale(img, (35,35))



#creating screen
screen=pygame.display.set_mode((sw,sh))





#paddle class
class Paddle():
	def __init__(self):
		self.x=sw/2.0
		self.y=550
		self.dx=0
		self.width=200
		self.height=25
		self.score=0

	def left(self):
	   self.dx= -27

	def right(self):
	   self.dx=27

	def move(self):
		self.x= self.x+self.dx

		if self.x<0+self.width/2.0:
			self.x=0+self.width/2.0
			self.dx=0

		elif self.x>sw-self.width/2.0:
			self.x=sw-self.width/2.0
			self.dx=0 

	def render(self):
	   pygame.draw.rect(screen,WHITE,pygame.Rect(int(self.x-self.width/2.0),int(self.y-self.height/2.0),self.width,self.height))


	def is_colliding(self,other):
	   x_collision=(math.fabs(self.x-other.x)*2)<(self.width+other.width)
	   y_collision=(math.fabs(self.y-other.y)*2)<(self.height+other.height)
	   return (x_collision and y_collision)   

#Ball class
class Ball():
	def __init__(self):
		self.x=sw/2.0
		self.y=530
		self.dx=10
		self.dy=-10
		self.width=10
		self.height=10

	

	def move(self):
		self.x= self.x+self.dx
		self.y=self.y+self.dy

		if self.x<0+self.width/2.0:
			self.x=0+self.width/2.0
			self.dx*=-1

		elif self.x>sw-self.width/2.0:
			self.x=sw-self.width/2.0
			self.dx*=-1


		if self.y<0+self.height/2.0:
			self.y=0+self.height/2.0
			self.dy*= -1

		elif self.y>sh-self.height/2.0:
			self.y=sh-self.height/2.0
			self.x=sw/2.0
			self.y=sh/2.0	 

	def render(self):
		pygame.draw.circle(screen, RED, (self.x, self.y), 14, 14)

	def is_colliding(self,other):
	   x_collision=(math.fabs(self.x-other.x)*2)<(self.width+other.width)
	   y_collision=(math.fabs(self.y-other.y)*2)<(self.height+other.height)
	   return (x_collision and y_collision)  

	def is_ground(self):
		if self.y>589:
			return True
		else:
			return False
		  	
	       	

#bricks
class Brick():
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.width=60
		self.height=25
		self.color=random.choice([WHITE,RED,GREEN,BLUE])

	def render(self):
	    pygame.draw.rect(screen,self.color,pygame.Rect(int(self.x-self.width/2.0),int(self.y-self.height/2.0),self.width,self.height))


#font
font=pygame.font.SysFont("comicsansms",18)

#paddle object
paddle=Paddle()
ball=Ball()
bricks=[]
for y in range(55,280,25):
	for x in range(25,1000,50):
		bricks.append(Brick(x,y))




#Maingame loop
while True:

	#controls loop
	 ok,img=cam.read()
	 imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	 res=hands.process(imgRGB)

	 if res.multi_hand_landmarks:
	 	for handlms in res.multi_hand_landmarks:
	 		for id,lm in enumerate(handlms.landmark):
	 			h,w,c=img.shape
	 			cx,cy=int(lm.x*w),int(lm.y*h)
	 			get_coordinates(cx,cy)

	 		mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)


	 ctime=time.time()
	 fps=1/(ctime-ptime)
	 ptime=ctime
	 


	 cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,4,(255,0,255),3)
	 cv2.imshow('my webcam', img)
	 if cv2.waitKey(1)==27:
	 	break

#game loop

	 for event in pygame.event.get():
	 	if event.type==pygame.QUIT:
	 		sys.exit()

      #Keyboard controls
	 	#if event.type==pygame.KEYDOWN:
	 	#	if event.key==pygame.K_LEFT:
	 	#		paddle.left()

	 	#	elif event.key==pygame.K_RIGHT:
	 	#		paddle.right()  


	 if life!=0:
	 	ball.move()
	 	paddle.move()
	 	

#check for collision
	 if ball.is_colliding(paddle):
		 ball.dy*=-1


	 for brick in bricks:
	 	if ball.is_colliding(brick):
			 ball.dy*=-1
			 paddle.score+=10
			 brick.x=12000


	#Background color of Screen
	 screen.fill((0,0,0))

	#Rendering objects
	 paddle.render()
	 if life!=0:
	 	ball.render()
	 for brick in bricks:
	 	brick.render()

     #Rendering score
	 score=font.render(f"Score:{paddle.score}",True,WHITE)
	 screen.blit(score,(sw/2.0-25,10))
	 if ball.is_ground():
		 life-=1

	 if life==3:
	 	screen.blit(img0,(0,0))
	 	screen.blit(img1,(30,0))
	 	screen.blit(img2,(60,0))

	 elif life==2:
	 	screen.blit(img0,(0,0))
	 	screen.blit(img1,(30,0))

	 elif life==1:
	 	screen.blit(img0,(0,0))

	 else:
	 	game=font.render("GAME OVER :(",True,WHITE)
	 	screen.blit(game,(0,0))
	 	life=0


    #vision control
	 if xval>640:
	 		paddle.left()

	 else:
	 	paddle.right()	


	 pygame.display.flip()

	 #FPS
	 clock.tick(29)		