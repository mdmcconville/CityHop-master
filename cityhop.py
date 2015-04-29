import Tkinter as tk
from map import *

if __name__=="__main__":
    city1 = raw_input("Starting city: ")
    city2 = raw_input("Ending city: ")

    # I don't think this function ended up working
    def end(top):
        global city1
        global city2
        city1, city2 = top.getCities()
        print(city1, city2)
        top.destroy()

        
    root = tk.Tk()
    root.configure(background = 'linen')
    
    newMap = Map()
    
    near_start, d_start, near_end, d_end = newMap.closest_nodes(city1, city2)
    # Add the start and end cities to the graph
    newMap.update_graph(near_start, city1, d_start)
    newMap.update_graph(near_end, city2, d_end)
    newMap.label_url(city1, city2)
    newMap.print_map(root, city1, city2)
    
    
