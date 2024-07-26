<<<<<<< HEAD
import time
import pygame
import random
import math
import pandas as pd
import tkinter as tk
from tkinter import filedialog
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED= 255, 0, 0
    GRAY = 	150,182,182
    OFFWHITE = 206,194,179
    SKY = 204,204,255
    BACKGROUND_COLOR =SKY
    BUTTN = 159,226,191

    GRADIETS = [
        # (128,128,128),
        # (160,160,160),
        # (192,192,192),

        (52, 204, 235),
        (203, 82, 227),
        (128,128,128),

        # (32,32,32),
        # (64,64,64),
        # (128,128,128),

        # (53,47,42),
        # (125,103,86),
        # (188,154,129)
    ]
    # BUTTON_FONT = pygame.font.SysFont(font=BACKGROUND_COLOR)
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

class Button:
    def __init__(self, x, y, width, height, text, color, font, font_color=DrawInformation.BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = font
        self.font_color = font_color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.font_color)
        window.blit(text_surface, (
            self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
            self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        ))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw(draw_info, algo_name, ascending, buttons,elapsed_time):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    time_text = draw_info.FONT.render(f"Time: {elapsed_time:.3f} Sec", 1, DrawInformation.BLACK)
    draw_info.window.blit(time_text, (0 , 125))


    for button in buttons:
        button.draw(draw_info.window)

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIETS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):  
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        if data.shape[1] != 1:
            raise ValueError("CSV file should contain exactly one column")
        return data.iloc[:, 0].tolist()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return file_path


def store_csv_file(lst):
    sorted_list = lst
    print (sorted_list)
    

def timing_sort(draw_info, sort_func, ascending=True):
    start_time = time.time()
    for _ in sort_func(draw_info, ascending):
        yield True
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time



def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    n = len(lst)

    for i in range(n):
        extreme_index = i
        for j in range(i + 1, n):
            if ascending:
                if lst[j] < lst[extreme_index]:
                    extreme_index = j
            else:
                if lst[j] > lst[extreme_index]:
                    extreme_index = j

        lst[i], lst[extreme_index] = lst[extreme_index], lst[i]

        draw_list(draw_info, {extreme_index: draw_info.GREEN, i: draw_info.RED}, True)
        yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(start, end):
        pivot_index = start
        pivot = lst[pivot_index]

        while start < end:
            while start < len(lst) and ((lst[start] <= pivot and ascending) or (lst[start] >= pivot and not ascending)):
                start += 1

            while (lst[end] > pivot and ascending) or (lst[end] < pivot and not ascending):
                end -= 1

            if start < end:
                lst[start], lst[end] = lst[end], lst[start]
                draw_list(draw_info, {start: draw_info.GREEN, end: draw_info.RED}, True)
                yield True

        lst[end], lst[pivot_index] = lst[pivot_index], lst[end]
        draw_list(draw_info, {end: draw_info.GREEN, pivot_index: draw_info.RED}, True)
        

        yield True

        return end
     
    def quick_sort_recursive(start, end):
        if start < end:
            p = yield from partition(start, end)
            yield from quick_sort_recursive(start, p - 1)
            yield from quick_sort_recursive(p + 1, end)

    yield from quick_sort_recursive(0, len(lst) - 1)

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_recursive(start, end):
        if end - start > 1:
            mid = (start + end) // 2
            yield from merge_sort_recursive(start, mid)
            yield from merge_sort_recursive(mid, end)
            left = lst[start:mid]
            right = lst[mid:end]
            k = start
            i = 0
            j = 0
            while start + i < mid and mid + j < end:
                if (left[i] < right[j] and ascending) or (left[i] > right[j] and not ascending):
                    lst[k] = left[i]
                    i = i + 1
                else:
                    lst[k] = right[j]
                    j = j + 1
                k = k + 1
                draw_list(draw_info, {k: draw_info.GREEN, k+1: draw_info.RED}, True)
                yield True

            while start + i < mid:
                lst[k] = left[i]
                i = i + 1
                k = k + 1
                draw_list(draw_info, {k: draw_info.GREEN, k+1: draw_info.RED}, True)
                yield True

            while mid + j < end:
                lst[k] = right[j]
                j = j + 1
                k = k + 1
                draw_list(draw_info, {k: draw_info.GREEN, k+1: draw_info.RED}, True)
                yield True

    yield from merge_sort_recursive(0, len(lst))

def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def heapify(end, i):
        l = 2 * i + 1
        r = 2 * (i + 1)
        max_idx = i
        if l < end and ((lst[i] < lst[l] and ascending) or (lst[i] > lst[l] and not ascending)):
            max_idx = l
        if r < end and ((lst[max_idx] < lst[r] and ascending) or (lst[max_idx] > lst[r] and not ascending)):
            max_idx = r
        if max_idx != i:
            lst[i], lst[max_idx] = lst[max_idx], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, max_idx: draw_info.RED}, True)
            yield True
            yield from heapify(end, max_idx)

    length = len(lst)
    start = length // 2 - 1
    for i in range(start, -1, -1):
        yield from heapify(length, i)
    for i in range(length - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        yield True
        yield from heapify(i, 0)

def shell_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = lst[i]
            j = i
            while j >= gap and ((lst[j - gap] > temp and ascending) or (lst[j - gap] < temp and not ascending)):
                lst[j] = lst[j - gap]
                j -= gap
                draw_list(draw_info, {j: draw_info.GREEN, j+gap: draw_info.RED}, True)
                yield True
            lst[j] = temp
            draw_list(draw_info, {j: draw_info.GREEN, i: draw_info.RED}, True)
            
            yield True
        gap //= 2




def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    sorting = False
    elapsed_time = 0  # Variable to store elapsed time
    start_time = None  # Variable to store the start time


    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1000, 750, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
   
    # print ("Before sorting list="+draw_info.lst)

    buttons = [
        Button(775, 0, 100, 28, "Reset", DrawInformation.RED, DrawInformation.FONT,DrawInformation.WHITE),
        Button(900, 0, 100, 28, "Start", DrawInformation.GREEN, DrawInformation.FONT),
        Button(0, 10, 110, 50, "Ascending", DrawInformation.GRAY, DrawInformation.FONT),
        Button(0, 70, 110, 50, "Descending", DrawInformation.GRAY, DrawInformation.FONT),
        Button(150, 78, 100, 50, "Insertion", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(270, 78, 100, 50, "Bubble", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(390, 78, 100, 50, "Selection", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(870, 78, 100, 50, "Quick", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(630, 78, 100, 50, "Merge", DrawInformation.BUTTN, DrawInformation.FONT, DrawInformation.WHITE),
        Button(750, 78, 100, 50, "Heap", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(510, 78,100, 50, "Shell", DrawInformation.BUTTN, DrawInformation.FONT), 
        Button(900, 40,100, 28, "GetList", DrawInformation.BUTTN, DrawInformation.FONT),         
        Button(775, 40, 100, 28, "Load CSV", DrawInformation.BUTTN, DrawInformation.FONT)  # New CSV button
        # Add more buttons here if needed
    ]

    while run:
        clock.tick(30)
        if sorting:
            try:
                next(sorting_algorithm_generator)
                elapsed_time = time.time() - start_time  # Update elapsed time
            except StopIteration:
                
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, buttons,elapsed_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for button in buttons:
                    if button.is_clicked(pos):
                        if button.text == "Reset":
                            lst = generate_starting_list(n, min_val, max_val)
                            draw_info.set_list(lst)
                            elapsed_time = 0  # Reset elapsed time
                            start_time = None  # Reset start time
                        elif button.text == "Start" and not sorting:
                            sorting = True
                            sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                            start_time = time.time()  # Set start time
                        elif button.text == "Ascending" and not sorting:
                            ascending = True
                        elif button.text == "Descending" and not sorting:
                            ascending = False
                            
                        elif button.text == "Insertion" and not sorting:
                            sorting_algorithm = insertion_sort
                            sorting_algo_name = "Insertion Sort"
                        elif button.text == "Bubble" and not sorting:
                            sorting_algorithm = bubble_sort
                            sorting_algo_name = "Bubble Sort"
                        elif button.text == "Selection" and not sorting:
                            sorting_algorithm = selection_sort
                            sorting_algo_name = "Selection Sort"
                        elif button.text == "Quick" and not sorting:
                            sorting_algorithm = quick_sort
                            sorting_algo_name = "Quick Sort"
                        elif button.text == "Merge" and not sorting:
                            sorting_algorithm = merge_sort
                            sorting_algo_name = "Merge Sort"
                        elif button.text == "Heap" and not sorting:
                            sorting_algorithm = heap_sort
                            sorting_algo_name = "Heap Sort"
                        elif button.text == "Shell" and not sorting:
                            sorting_algorithm = shell_sort
                            sorting_algo_name = "Shell Sort"
                        elif button.text == "Load CSV":
                            file_path = select_csv_file()
                            if file_path:
                                lst = read_csv(file_path)
                                draw_info.set_list(lst)
                                elapsed_time = 0  # Reset elapsed time
                        elif button.text == "GetList":
                            store_csv_file(lst)

        
    pygame.quit()

if __name__ == "__main__":
    main()




=======
import time
import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED= 255, 0, 0
    GRAY = 	150,182,182
    OFFWHITE = 206,194,179
    SKY = 204,204,255
    BACKGROUND_COLOR =SKY
    BUTTN = 159,226,191

    GRADIETS = [
        # (128,128,128),
        # (160,160,160),
        # (192,192,192),

        (52, 204, 235),
        (203, 82, 227),
        (128,128,128),

        # (32,32,32),
        # (64,64,64),
        # (128,128,128),

        # (53,47,42),
        # (125,103,86),
        # (188,154,129)
    ]
    # BUTTON_FONT = pygame.font.SysFont(font=BACKGROUND_COLOR)
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

class Button:
    def __init__(self, x, y, width, height, text, color, font, font_color=DrawInformation.BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = font
        self.font_color = font_color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.font_color)
        window.blit(text_surface, (
            self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
            self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        ))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw(draw_info, algo_name, ascending, buttons,elapsed_time):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    time_text = draw_info.FONT.render(f"Time: {elapsed_time:.4f} seconds", 1, DrawInformation.BLACK)
    draw_info.window.blit(time_text, (120, 50))


    for button in buttons:
        button.draw(draw_info.window)

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIETS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):  
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def timing_sort(draw_info, sort_func, ascending=True):
    start_time = time.time()
    for _ in sort_func(draw_info, ascending):
        yield True
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    n = len(lst)

    for i in range(n):
        extreme_index = i
        for j in range(i + 1, n):
            if ascending:
                if lst[j] < lst[extreme_index]:
                    extreme_index = j
            else:
                if lst[j] > lst[extreme_index]:
                    extreme_index = j

        lst[i], lst[extreme_index] = lst[extreme_index], lst[i]

        draw_list(draw_info, {extreme_index: draw_info.GREEN, i: draw_info.RED}, True)
        yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(start, end):
        pivot_index = start
        pivot = lst[pivot_index]

        while start < end:
            while start < len(lst) and ((lst[start] <= pivot and ascending) or (lst[start] >= pivot and not ascending)):
                start += 1

            while (lst[end] > pivot and ascending) or (lst[end] < pivot and not ascending):
                end -= 1

            if start < end:
                lst[start], lst[end] = lst[end], lst[start]
                draw_list(draw_info, {start: draw_info.GREEN, end: draw_info.RED}, True)
                yield True

        lst[end], lst[pivot_index] = lst[pivot_index], lst[end]
        draw_list(draw_info, {end: draw_info.GREEN, pivot_index: draw_info.RED}, True)
        yield True

        return end

    def quick_sort_recursive(start, end):
        if start < end:
            p = yield from partition(start, end)
            yield from quick_sort_recursive(start, p - 1)
            yield from quick_sort_recursive(p + 1, end)

    yield from quick_sort_recursive(0, len(lst) - 1)

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_recursive(start, end):
        if end - start > 1:
            mid = (start + end) // 2
            yield from merge_sort_recursive(start, mid)
            yield from merge_sort_recursive(mid, end)
            left = lst[start:mid]
            right = lst[mid:end]
            k = start
            i = 0
            j = 0
            while start + i < mid and mid + j < end:
                if (left[i] < right[j] and ascending) or (left[i] > right[j] and not ascending):
                    lst[k] = left[i]
                    i = i + 1
                else:
                    lst[k] = right[j]
                    j = j + 1
                k = k + 1
                draw_list(draw_info, {k: draw_info.GREEN, k+1: draw_info.RED}, True)
                yield True

            while start + i < mid:
                lst[k] = left[i]
                i = i + 1
                k = k + 1
                draw_list(draw_info, {k: draw_info.GREEN, k+1: draw_info.RED}, True)
                yield True

            while mid + j < end:
                lst[k] = right[j]
                j = j + 1
                k = k + 1
                draw_list(draw_info, {k: draw_info.GREEN, k+1: draw_info.RED}, True)
                yield True

    yield from merge_sort_recursive(0, len(lst))

def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def heapify(end, i):
        l = 2 * i + 1
        r = 2 * (i + 1)
        max_idx = i
        if l < end and ((lst[i] < lst[l] and ascending) or (lst[i] > lst[l] and not ascending)):
            max_idx = l
        if r < end and ((lst[max_idx] < lst[r] and ascending) or (lst[max_idx] > lst[r] and not ascending)):
            max_idx = r
        if max_idx != i:
            lst[i], lst[max_idx] = lst[max_idx], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, max_idx: draw_info.RED}, True)
            yield True
            yield from heapify(end, max_idx)

    length = len(lst)
    start = length // 2 - 1
    for i in range(start, -1, -1):
        yield from heapify(length, i)
    for i in range(length - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        yield True
        yield from heapify(i, 0)

def shell_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = lst[i]
            j = i
            while j >= gap and ((lst[j - gap] > temp and ascending) or (lst[j - gap] < temp and not ascending)):
                lst[j] = lst[j - gap]
                j -= gap
                draw_list(draw_info, {j: draw_info.GREEN, j+gap: draw_info.RED}, True)
                yield True
            lst[j] = temp
            draw_list(draw_info, {j: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
        gap //= 2




def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    sorting = False
    elapsed_time = 0  # Variable to store elapsed time
    start_time = None  # Variable to store the start time


    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1000, 750, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
   


    buttons = [
        Button(0, 0, 100, 28, "Reset", DrawInformation.RED, DrawInformation.FONT,DrawInformation.WHITE),
        Button(700, 0, 100, 28, "Start", DrawInformation.GREEN, DrawInformation.FONT),
        Button(0, 40, 110, 50, "Ascending", DrawInformation.GRAY, DrawInformation.FONT),
        Button(0, 95, 110, 50, "Descending", DrawInformation.GRAY, DrawInformation.FONT),
        Button(150, 78, 100, 50, "Insertion", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(270, 78, 100, 50, "Bubble", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(390, 78, 100, 50, "Selection", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(870, 78, 100, 50, "Quick", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(630, 78, 100, 50, "Merge", DrawInformation.BUTTN, DrawInformation.FONT, DrawInformation.WHITE),
        Button(750, 78, 100, 50, "Heap", DrawInformation.BUTTN, DrawInformation.FONT),
        Button(510, 78,100, 50, "Shell", DrawInformation.BUTTN, DrawInformation.FONT),        
        # Add more buttons here if needed
    ]

    while run:
        clock.tick(30)
        if sorting:
            try:
                next(sorting_algorithm_generator)
                elapsed_time = time.time() - start_time  # Update elapsed time
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, buttons,elapsed_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for button in buttons:
                    if button.is_clicked(pos):
                        if button.text == "Reset":
                            lst = generate_starting_list(n, min_val, max_val)
                            draw_info.set_list(lst)
                            elapsed_time = 0  # Reset elapsed time
                            start_time = None  # Reset start time
                        elif button.text == "Start" and not sorting:
                            sorting = True
                            sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                            start_time = time.time()  # Set start time
                        elif button.text == "Ascending" and not sorting:
                            ascending = True
                        elif button.text == "Descending" and not sorting:
                            ascending = False
                        elif button.text == "Insertion" and not sorting:
                            sorting_algorithm = insertion_sort
                            sorting_algo_name = "Insertion Sort"
                        elif button.text == "Bubble" and not sorting:
                            sorting_algorithm = bubble_sort
                            sorting_algo_name = "Bubble Sort"
                        elif button.text == "Selection" and not sorting:
                            sorting_algorithm = selection_sort
                            sorting_algo_name = "Selection Sort"
                        elif button.text == "Quick" and not sorting:
                            sorting_algorithm = quick_sort
                            sorting_algo_name = "Quick Sort"
                        elif button.text == "Merge" and not sorting:
                            sorting_algorithm = merge_sort
                            sorting_algo_name = "Merge Sort"
                        elif button.text == "Heap" and not sorting:
                            sorting_algorithm = heap_sort
                            sorting_algo_name = "Heap Sort"
                        elif button.text == "Shell" and not sorting:
                            sorting_algorithm = shell_sort
                            sorting_algo_name = "Shell Sort"


    pygame.quit()

if __name__ == "__main__":
    main()




>>>>>>> 2b503aa9c2b95d68475e72ffa7929b8df94c5612
