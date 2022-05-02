import pygame,random
from random import randint
import math
from sklearn.cluster import KMeans

def distance(p1,p2):
	return math.sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("kmeans visualization")

running = True
	
clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BLACK = (0,0,0)
BACKGROUND_PANEL = (249, 255, 230)
WHITE = (255,255,255)



font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20)
text_plus = font.render('+', True, WHITE)
text_minus = font.render('-', True, WHITE)
text_run = font.render("Run", True, WHITE)
text_random = font.render("Random", True, WHITE)
text_algorithm = font.render("Algorithm", True, WHITE)
text_reset = font.render("Reset", True, WHITE)

COLORS=[]
K = 0
error = 0
points = []	
clusters = []
labels = []

while running:
	clock.tick(60)
	screen.fill(BACKGROUND)
	mouse_x, mouse_y = pygame.mouse.get_pos()

	# Draw interface
	# Draw panel
	pygame.draw.rect(screen, BLACK, (50,50,700,500))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (55,55,690,490))

	# K button + 
	pygame.draw.rect(screen, BLACK, (850,50,50,50))
	screen.blit(text_plus, (865,49))

	# K button -
	pygame.draw.rect(screen, BLACK, (950,50,50,50))
	screen.blit(text_minus, (969,49))

	# K value
	text_k = font.render("K = " + str(K), True, BLACK)
	screen.blit(text_k, (1050,50))

	# run button
	pygame.draw.rect(screen, BLACK, (850,150,150,50))
	screen.blit(text_run, (860,150))

	# random button
	pygame.draw.rect(screen, BLACK, (850,250,150,50))
	screen.blit(text_random, (860,250))

	# Reset button
	pygame.draw.rect(screen, BLACK, (850,550,150,50))
	screen.blit(text_reset, (860,550))

	# Algorithm button
	pygame.draw.rect(screen, BLACK, (850,450,150,50))
	screen.blit(text_algorithm, (860,450))

	# Draw mouse position when mouse is in panel
	if 50 < mouse_x < 750 and 50 < mouse_y < 550:
		text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")",True, BLACK)
		screen.blit(text_mouse, (mouse_x + 10, mouse_y))

	# End draw interface

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Create point on panel
			if 50 < mouse_x < 750 and 50 < mouse_y < 550:
				labels = []
				point = [mouse_x -50, mouse_y-50]
				points.append(point)
				print(points)

			# Change K button +
			if 850 < mouse_x < 900 and 50 < mouse_y < 100:
				labels = []
				clusters = []
				K = K+1
				print("Press K +")
				COLORS=[]
				for i in range(K):
					random_color_1 = random.randint(0, 255)
					random_color_2 = random.randint(0, 255)
					random_color_3 = random.randint(0, 255)
					color = [random_color_1, random_color_2, random_color_3]
					COLORS.append(color)
			
			# Change K button -
			if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
				labels=[]
				clusters = []
				if K > 0:
					K -= 1
				print("Press K -")
				COLORS = []
				for i in range(K):
					random_color_1 = random.randint(0, 255)
					random_color_2 = random.randint(0, 255)
					random_color_3 = random.randint(0, 255)
					color = [random_color_1, random_color_2, random_color_3]
					COLORS.append(color)

			# Random button
			if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
				clusters = []
				for i in range(K):
					random_point = [randint(0, 700), randint(0, 500)]
					clusters.append(random_point)
				print("Random")

			# Run button
			if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
				if clusters!=[]:
					labels = []
					# Assign points to closet clusters
					for p in points:
						distances_to_cluster = []
						for c in clusters:
							dis = distance(p,c)
							distances_to_cluster.append(dis)

						min_distance = min(distances_to_cluster)
						label = distances_to_cluster.index(min_distance)
						labels.append(label)

					# Update clusters
					for i in range(K):
						sum_x = 0
						sum_y = 0
						count = 0
						for j in range(len(points)):
							if labels[j] == i:
								sum_x += points[j][0]
								sum_y += points[j][1]
								count += 1
						if count != 0:
							new_cluster_x = sum_x/count
							new_cluster_y = sum_y/count
							clusters[i] = [new_cluster_x, new_cluster_y]
				print("Run")


			# Reset button
			if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
				COLORS = []
				K = 0
				error = 0
				points = []
				clusters = []
				labels = []
				print("Reset pressed")

			# Algorithm 
			if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
				if K!=0 and points!= []:
					kmeans = KMeans(n_clusters=K).fit(points)
					labels = kmeans.predict(points)
					clusters=kmeans.cluster_centers_
				print("Algorithm pressed")

	# Draw cluster
	if clusters!=[]:
		for i in range(len(clusters)):
			pygame.draw.circle(screen,COLORS[i], (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)
			print(clusters[i])

	# Draw point
	for i in range(len(points)):
		pygame.draw.circle(screen,BLACK, (points[i][0] + 50, points[i][1] + 50), 6)

		if labels == []:
			pygame.draw.circle(screen,WHITE, (points[i][0] + 50, points[i][1] + 50), 5)
		else:
			if clusters != []:
				pygame.draw.circle(screen,COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 5)

	# Calculate and draw error
	error = 0
	if clusters != [] and labels != []:
		for i in range(len(points)):
			error += distance(points[i], clusters[labels[i]])

	text_error = font.render("Error = " + str(int(error)), True, BLACK)
	screen.blit(text_error, (860,350))

	pygame.display.flip()

pygame.quit()
