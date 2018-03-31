# IF3260: Computer Graphics
# Camera 3D Modelling

# Libraries and Packages
import sys

from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Camera Position
angle = 0.0 			# Camera angle
x = 0.0

z = 0.0					# Camera position
dX = 0.0

dZ = 0.0				# Camera direction

# mouse
xrot = 0.0
yrot = 0.0
 
xdiff = 0.0
ydiff = 0.0

mouseDown = False

class Camera:
	
	def __init__(self):
		self.position = (0, 0, 0)
		self.rotation = (0, 0, 0)
	
	def translate(self, dx, dy, dz):
		x, y, z = self.position
		self.position = (x + dx, y + dy, z + dz)
		
	def rotate(self, dx, dy, dz):
		x, y, z = self.rotation
		self.rotation = (x + dx, y + dy, z + dz)
		
	def apply(self):
		glTranslate(*self.position)
		glRotated(self.rotation[0], -1, 0, 0)
		glRotated(self.rotation[1], 0, -1, 0)
		glRotated(self.rotation[2], 0, 0, -1)
		
camera = Camera()

def idle():
	global mouseDown, xrot, yrot
	if (not mouseDown):
		
		if(xrot > 1):
			xrot -= 0.001 * xrot
		elif(xrot < -1):
			xrot += 0.001 * -xrot 
		else:
			xrot = 0

		if(yrot > 1):
			yrot -= 0.001 * yrot
		elif(yrot < -1):
			yrot += 0.001 * -yrot
		else:
			yrot = 0	

def mouse(button, state, x, y):
	global xdiff, ydiff, mouseDown
	# print(str(button) + " " + str(GLUT_LEFT_BUTTON))
	# print(str(state) + " " + str(GLUT_DOWN))
	if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
		mouseDown = True
		
		xdiff = x - yrot
		ydiff = -y + xrot
		print(str(xdiff)+ " "+ str(ydiff))
	else:
		mouseDown = False


def mouseMotion(x, y):
	global yrot, xrot, mouseDown
	if (mouseDown):
		yrot = x - xdiff
		xrot = y + ydiff
		#print(mouseDown)

# Snowman
def drawSnowMan():
	glColor3f(1.0, 1.0, 1.0)

	#Draw Body
	glTranslatef(0.0 ,0.75, 0.0)
	glutSolidSphere(0.75,20,20)

	#Draw Head
	glTranslatef(0.0, 1.0, 0.0)
	glutSolidSphere(0.25,20,20)

	#Draw Eyes
	glPushMatrix()
	glColor3f(0.0,0.0,0.0)
	glTranslatef(0.05, 0.10, 0.18)
	glutSolidSphere(0.05,10,10)
	glTranslatef(-0.1, 0.0, 0.0)
	glutSolidSphere(0.05,10,10)
	glPopMatrix()

	#Draw Nose
	glColor3f(1.0, 0.5 , 0.5)
	glutSolidCone(0.08,0.5,10,2)

def renderScene():
	global x, z, dX, dZ, angle
	#Clear Color and Depth Buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	#Reset transformations
	glLoadIdentity()
	#Set the camera
	#gluLookAt	(	x, 1.0, z,
	#			x+dX, 1.0,  z+dZ,
	#			0.0, 1.0,  0.0
	#			)
		
	camera.apply()
	
	#Draw ground

    #Draw 36 Snowmen
	# for i in range (-3,3):
	# 	for j in range(-3,3):
	# 		glPushMatrix()
	# 		glTranslatef(i*10.0,0,j * 10.0)
	# 		drawSnowMan()
	# 		glPopMatrix()
		
	camera.rotate(xrot*0.001, 0.0, 0.0)
	camera.rotate(0, yrot*0.001, 0.0)
	
	drawSnowMan()
	idle()
	glFlush()
	glutSwapBuffers()
	
def processSpecialKeys(key, xx, yy):
	global x, z, dX, dZ, angle
	fraction = 0.1
	movespeed = 1
	
	if (key == GLUT_KEY_LEFT):
		camera.translate(movespeed, 0, 0)
		#angle -= 0.01
		#dX = sin(angle)
		#dY = -cos(angle)
	elif (key == GLUT_KEY_RIGHT):
		camera.translate(-movespeed, 0, 0)
		#angle -= 0.01
		#dX = sin(angle)
		#dY = -cos(angle)
	elif (key == GLUT_KEY_UP):
		camera.translate(0, -movespeed, 0)
		#x += dX * fraction
		#z += dZ * fraction
	elif (key == GLUT_KEY_DOWN):
		camera.translate(0, movespeed, 0)
		#x -= dX * fraction
		#z -= dZ * fraction
	elif (key == GLUT_KEY_PAGE_UP):
		camera.translate(0, 0, movespeed)
	elif (key == GLUT_KEY_PAGE_DOWN):
		camera.translate(0, 0, -movespeed)

def processNormalKeys(key, x, y):
	if (key == 27):
		exit(0)

def changeSize(w, h):
	#Prevent a divide by zero, when window is too short
	#(you cant make a window of zero width).
	if (h == 0):
		h = 1
	ratio = w * 1.0 / h

	#Use the Projection Matrix
	glMatrixMode(GL_PROJECTION)

	#Reset Matrix
	glLoadIdentity()

	#Set the viewport to be the entire window
	glViewport(0, 0, w, h)

	#Set the correct perspective.
	gluPerspective(45.0, ratio, 0.1, 100.0)

	#Get Back to the Modelview
	glMatrixMode(GL_MODELVIEW)
		
def main():

	#init GLUT and create window
	glutInit()
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
	glutInitWindowPosition(100,100)
	glutInitWindowSize(800,600)
	glutCreateWindow(b'IF3260: Computer Graphics')

	glMatrixMode(GL_PROJECTION)
	gluPerspective(60, 1, 1.0, 1000.0)
	glMatrixMode(GL_MODELVIEW)
	
	#register callbacks
	glutDisplayFunc(renderScene)
	glutReshapeFunc(changeSize)
	glutIdleFunc(renderScene)
	#glutKeyboardFunc(processNormalKeys)
	glutSpecialFunc(processSpecialKeys)
	glutMouseFunc(mouse)
	glutMotionFunc(mouseMotion)

	#OpenGL init
	glEnable(GL_DEPTH_TEST)

	#enter GLUT event processing cycle
	glutMainLoop()
	
main()