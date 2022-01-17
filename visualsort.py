#just changing to learn git
import pygame 
import random

pygame.init()

class DrawInformation:

	BLUE = 30,40,56
	WHITE = 255,255,255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	PURPLE = 120, 0 , 255
	BACKGROUND_COLOR = WHITE

	purp_GRAD = [
		(215, 161, 249),
		(160, 132, 240),
		(97, 51, 133),
	]

	grey_GRAD = [
		(128, 128, 128),
		(160,160,160),
		(192,192,192),
	]

	GRADIENTS = purp_GRAD

	FONT = pygame.font.SysFont('consolas', 30)
	LARGE_FONT = pygame.font.SysFont('consolas', 40)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):

		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting ALgorithm Visualizer")
		self.set_list(lst)

	def set_list(self,lst):

		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)
		self.block_width = (self.width - self.SIDE_PAD) // len(lst)
		self.block_height = (self.height - self.TOP_PAD) // (self.max_val-self.min_val)
		self.start_x = self.SIDE_PAD // 2


	def draw(self, font_color, algo_name, ascending,lst_status ):

		self.window.fill(self.BACKGROUND_COLOR)

		head = self.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'} - {lst_status}",1,font_color)
		self.window.blit(head,(self.width/2 - head.get_width()/2,0))

		controls = self.FONT.render("'SPACE'- Start : 'R'- Reset : 'T'- Ascending or Descending : 'W'- Theme",1,font_color)
		self.window.blit(controls,(self.width/2 - controls.get_width()/2,70))

		sorting = self.FONT.render("'I'- Insertion Sort : 'B'- Bubble Sort : 'S'- Selection Sort ",1,font_color)
		self.window.blit(sorting,(self.width/2 - sorting.get_width()/2,110))

		self.draw_list()
		pygame.display.update()




	def draw_list(self, color_positons = {}, clear = False):

		lst = self.lst

		if clear:
			clear_r = (self.SIDE_PAD//2, self.TOP_PAD, self.width - self.SIDE_PAD, self.height )
			pygame.draw.rect(self.window, self.BACKGROUND_COLOR, clear_r) 


		for i,val in enumerate(lst):

			x = self.start_x + i * self.block_width
			y = self.height - (val - self.min_val) * self.block_height 

			color = self.GRADIENTS[i % 3]

			if i in color_positons:
				color = color_positons[i]


			pygame.draw.rect(self.window, color, (x,y,self.block_width, self.height))

		if clear:

			pygame.display.update()


def generate_list(n, min_val, max_val):

	lst = []

	for i in range(n):

		val = random.randint(min_val,max_val)
		lst.append(val)

	return lst

def bubble_sort(draw_info, ascending = True):

	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			if (lst[j] > lst[j + 1] and ascending) or (lst[j] < lst[j + 1] and not ascending):
				lst[j],lst[j + 1] = lst[j + 1],lst[j]
				draw_info.draw_list({j:draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True
	return lst

def insertion_sort(draw_info, ascending = True):

	lst = draw_info.lst

	for i in range(1,len(lst)):
		tmp = lst[i]

		while True:

			ascending_sort = i > 0 and lst[i-1] > tmp and ascending
			descending_sort = i > 0 and lst[i-1] < tmp and not ascending

			if not ascending_sort and not descending_sort:
				break
			lst[i] = lst[i - 1]
			i -= 1
			lst[i] = tmp

			draw_info.draw_list({i-1:draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst

def selection_sort(draw_info, ascending = True):

	lst = draw_info.lst

	for i in range(len(lst)):
		tmp = lst[i]
		min1 = i
		for j in range(i+1,len(lst)):

			if lst[j] < tmp and ascending:

				tmp = lst[j]
				min1 = j

			if lst[j] > tmp and not ascending:

				tmp = lst[j]
				min1 = j

			draw_info.draw_list({i:draw_info.GREEN, j: draw_info.RED}, True)

		lst[i],lst[min1] = tmp,lst[i]
		
		yield True


	return lst
def main():

	run = True
	clock = pygame.time.Clock()

	change_toggle = 0
	n = 150
	min_val = 0
	max_val = 100

	lst = generate_list(n, min_val, max_val)
	draw_info = DrawInformation(1780, 800,lst)
	sorting = False
	ascending = True

	lst_status = "Unsorted"

	color = draw_info.PURPLE

	sorting_t = bubble_sort
	sorting_name = "Bubble Sort"
	sorting_gen = None


	while run:

		clock.tick(60)

		if sorting:
			
			try:
				next(sorting_gen)
			except StopIteration:
				sorting = False
				lst_status = "Sorted"
		else:
			draw_info.draw(color, sorting_name, ascending,lst_status)

		pygame.display.update()

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
				lst_status = "Unsorted"

			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				lst_status = "Sorting"
				draw_info.draw(color, sorting_name, ascending,lst_status)
				sorting_gen = sorting_t(draw_info,ascending)

			elif event.key == pygame.K_i and sorting == False:
				sorting_t = insertion_sort
				sorting_name = "Insertion Sort"

			elif event.key == pygame.K_b and sorting == False:
				sorting_t = bubble_sort
				sorting_name = "Bubble Sort"


			elif event.key == pygame.K_s and sorting == False:
				sorting_t = selection_sort
				sorting_name = "Selection Sort"

			elif event.key == pygame.K_t and not sorting:
				if ascending == False:
					ascending = True
				else:
					ascending = False


			elif event.key == pygame.K_w:

				if change_toggle == 0:
					draw_info.BACKGROUND_COLOR = draw_info.BLUE
					draw_info.GRADIENTS = draw_info.grey_GRAD
					color = draw_info.WHITE
					draw_info.draw(draw_info.WHITE,sorting_name,ascending,lst_status)
					change_toggle = 1
				else:
					draw_info.BACKGROUND_COLOR = draw_info.WHITE
					draw_info.GRADIENTS = draw_info.purp_GRAD
					color = draw_info.PURPLE
					draw_info.draw(draw_info.PURPLE,sorting_name,ascending,lst_status)
					change_toggle = 0




	pygame.quit()


if __name__ == "__main__":
	main()
