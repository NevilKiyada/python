import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED= 255, 0, 0
    # GREY =128, 128, 128
    BACKGROUND_COLOR =WHITE

    GRADIETS = [
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]

    FONT = pygame.font.SysFont('comicsans',20)
    LARGE_FONT = pygame.font.SysFont('comicsans',28)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")

        self.set_list(lst)

    def set_list(self,lst):
        self.lst = lst  
        self.min_val = min(lst)
        self.max_val = max(lst)
        
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))  
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info ,algo_name , ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)


    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}",1,draw_info.GREEN) 
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 ,5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending" ,1,draw_info.BLACK) 
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 ,40))
    
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort " ,1,draw_info.BLACK) 
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 ,65))
    
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info , color_positions={},clear_bg=False):
    lst =  draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2,draw_info.TOP_PAD,
                       draw_info.width - draw_info.SIDE_PAD,draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR, clear_rect)


    for i , val in enumerate(lst):
        x=draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIETS[i % 3]

        if i in color_positions:
            color = color_positions[i]



        pygame.draw.rect(draw_info.window , color , (x,y,draw_info.block_width , draw_info.height))
    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):  
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst=draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)- 1 - i):
            num1=lst[j]
            num2=lst[j+1]

            if (num1>num2 and ascending) or (num1<num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1] , lst[j]

                draw_list(draw_info , {j: draw_info.GREEN ,j + 1: draw_info.RED}, True)
                yield True
 

    return lst


def Selection_sort(draw_info , ascending=True):
    lst= draw_info.lst

    n= len(lst)

    for i in range(n):
        extreme_index = i
        for j in range(i+1, n):
            if ascending:
                if lst[j] < lst[extreme_index]:
                    extreme_index = j
            else:
                if lst[j] > lst[extreme_index]:
                    extreme_index = j

        # Swap the found extreme element with the first element of the unsorted part
        lst[i], lst[extreme_index] = lst[extreme_index], lst[i]

        draw_list(draw_info, {extreme_index: draw_info.GREEN, i: draw_info.RED}, True)
        yield True

    return lst


'''
def merge_sort(draw_info , ascending=True):

    lst = draw_info.lst


    if len(lst) > 1:
        mid = len(lst) // 2
        left_half = lst[:mid]
        right_half = lst[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                lst[k] = left_half[i]
                i += 1
            else:
                lst[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            lst[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            lst[k] = right_half[j]
            j += 1
            k += 1

    return lst


'''


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i -1]
            i=i-1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.GREEN, i : draw_info.RED}, True)
            yield True

    return lst


def main():
    
    run = True
    clock = pygame.time.Clock()

    n= 50
    min_val = 0
    max_val = 100
    sorting = False

    lst = generate_starting_list(n, min_val, max_val)
    draw_info =DrawInformation(800,600,lst) 
    sorting = False
    ascending = True

    sorting_algorithm  = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None


    while run:
        clock.tick(30)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name,ascending)

            
        # draw(draw_info , sorting_algo_name,ascending)
        # pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True 
                sorting_algorithm_generator = sorting_algorithm(draw_info , ascending )
            elif event.key == pygame.K_a and not sorting :
                ascending = True 
            elif event.key == pygame.K_d and not sorting :
                ascending = False 

            elif event.key == pygame.K_i and not sorting :
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting :
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_s and not sorting :
                sorting_algorithm = Selection_sort
                sorting_algo_name = "Selection_sort"

            elif event.key == pygame.K_m and not sorting :
                sorting_algorithm = merge_sort
                sorting_algo_name = "merge_sort"

    pygame.quit()

if __name__ == "__main__":
    main()