import pygame, random
from random import randint
import math


def distance(p1, p2):
	return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


pygame.init()

screen = pygame.display.set_mode((1200, 700))

pygame.display.set_caption("kmeans visualization")

running = True

clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BLACK = (0, 0, 0)
BACKGROUND_PANEL = (249, 255, 230)
WHITE = (255, 255, 255)

#TEXT
def create_text_white(string):
	font=pygame.font.SysFont('sans',40)
	return font.render(string,True,WHITE)
def create_text_black(string):
	font=pygame.font.SysFont('sans',40)
	return font.render(string,True,BLACK)
k = 0
errol = 0
point = list()
clusters = list()
lable = list()
col = list()
while running:
	clock.tick(60)
	screen.fill(BACKGROUND)

	#Draw interface
	#Draw panel
	pygame.draw.rect(screen,BLACK,(50,50,700,500))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

	# K Button +
	pygame.draw.rect(screen,BLACK,(800,50,50,50))
	screen.blit(create_text_white('+'),(816,50))
	# K Button -
	pygame.draw.rect(screen, BLACK, (900, 50, 50, 50))
	screen.blit(create_text_white("-"), (919, 49))
	# Random button
	pygame.draw.rect(screen, BLACK, (800, 150, 150, 50))
	screen.blit(create_text_white("Random"), (810,155))
	# Run button
	pygame.draw.rect(screen, BLACK, (800, 250, 150, 50))
	screen.blit(create_text_white("Run"), (810, 255))
	# Algorithm button
	pygame.draw.rect(screen, BLACK, (800, 450, 150, 50))
	screen.blit(create_text_white("Algorithm"), (810, 455))
	# Reset button
	pygame.draw.rect(screen, BLACK, (800, 550, 150, 50))
	screen.blit(create_text_white("Reset"), (810, 555))

	#End draw interface
	# get position of mouse
	mouse_x, mouse_y = pygame.mouse.get_pos()
	#draw mouse position when mouse is in panel
	if 55<mouse_x<(55+690) and 55< mouse_y<(55+490):
		font1 = pygame.font.SysFont('sans', 20)
		text_mouse= font1.render("("+str(mouse_x-55)+","+str(mouse_y-55)+")",True,BLACK)
		screen.blit(text_mouse,(mouse_x+10,mouse_y))



	# print(mouse_x,mouse_y)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Create point on panel
			lable=[]
			errol = 0
			if 55 < mouse_x < (55 + 690) and 55 < mouse_y < (55 + 490):
				point.append([mouse_x-55,mouse_y-55])
				print(point)

			if 800<mouse_x<850 and 50<mouse_y<100:
				print("Plus K")
				k+=1
			if 900<mouse_x<950 and 50<mouse_y<100:
				print("Subtract K")
				if k>0:
					k-=1
			if 800<mouse_x<950 and 150<mouse_y<200:
				lable=[]
				print("Random")
				clusters = []
				for i in range(k):
					random_x = random.randint(55,(55+690))
					random_y = random.randint(55,(55+490))
					random_color_1 = random.randint(0,255)
					random_color_2 = random.randint(0, 255)
					random_color_3 = random.randint(0, 255)
					color=[random_color_1,random_color_2,random_color_3]
					clusters.append([random_x-55,random_y-55,color])
					print(clusters[i])
			if 800 < mouse_x < 950 and 250 < mouse_y < 300:
				if point==[]:
					print("Dont have point")
				else:
					lable=[]
					print("Run")

					#Asign points to closet clusters
					for i in range(len(point)):
						Min = [1000, 0, 0]
						distance=[]
						for r in range(len(clusters)):
							dx = clusters[r][0]-point[i][0]
							dy = clusters[r][1]-point[i][1]
							d = math.sqrt(pow(dx,2)+pow(dy,2))
							distance.append([d,i,r])
						for m in range(len(distance)):
							if Min[0]>=distance[m][0]:
								Min=distance[m]
						lable.append(Min[2])
					#Remove Clusters centroid to mean
					clusters_2=[]
					for i in range(k):
						sum_x=0
						sum_y=0
						count=0
						for j in range(len(point)):
							if clusters[i][2]==clusters[lable[j]][2]:
								sum_x += (point[j][0] )
								sum_y += (point[j][1] )
								count += 1
						if count!=0:
							clus=[(sum_x)/count,(sum_y)/count,clusters[i][2]]
							print(clus)
						clusters_2.append(clus)
					clusters=clusters_2

					#Errol
					for i in range(len(point)):
						Min = [1000, 0, 0]
						distance = []
						for r in range(len(clusters)):
							dx = clusters[r][0] - point[i][0]
							dy = clusters[r][1] - point[i][1]
							d = math.sqrt(pow(dx, 2) + pow(dy, 2))
							distance.append([d, i, r])
						for m in range(len(distance)):
							if Min[0] >= distance[m][0]:
								errol+=distance[m][0]



			if 800 < mouse_x < 950 and 450 < mouse_y < 500:
				print("Algorithm")
			if 800 < mouse_x < 950 and 550 < mouse_y < 600:
				print("Reset")


		screen.blit(create_text_black('K = '+ str(k)), (1000, 50))
		screen.blit(create_text_black('Errol = ' + str(errol)), (800, 350))

	for i in range(len(point)):
		pygame.draw.circle(screen, BLACK, (point[i][0] + 55, point[i][1] + 55), 6)
		if lable==[]:
			pygame.draw.circle(screen, WHITE, (point[i][0] + 55, point[i][1] + 55), 5)
		else:
			pygame.draw.circle(screen, clusters[lable[i]][2], (point[i][0] + 55, point[i][1] + 55), 6)
	for i in range(len(clusters)):
		pygame.draw.rect(screen, tuple(clusters[i][2]),(clusters[i][0]+55,clusters[i][1]+55,20,20))
	pygame.display.flip()

pygame.quit()