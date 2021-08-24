from tkinter import *
import csv
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure



# Import geology map 

geology = []
rowlist_geo = []

with open('geology.txt',newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        geology.append(row)
        for value in row: 
            rowlist_geo.append(value)
            
            
# Rescale the value to 0 to 255

for i in range(len(geology)):
    for j in range(len(geology[0])):
        geo_max = max(geology[j])
        geo_min = min(geology[j])
        
for i in range(len(geology)):
    for j in range(len(geology[0])):
        geology[i][j] = (255/geo_max)*geology[i][j]
        
        
            
#plt.imshow(geology, cmap = plt.get_cmap('gray'))


# Import Transport map 
transport = []
rowlist_trans = []

with open('transport.txt',newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        transport.append(row)
        for value in row: 
            rowlist_trans.append(value)
  
# Find the minimum and maximum for rescale
for i in range(len(transport)): 
    for j in range(len(transport[0])):
        trans_max = max(transport[j])
        trans_min = min(transport[j])
        
        
for i in range(len(transport)):
    for j in range(len(transport[0])):
        transport[i][j] = (255/trans_max)*transport[i][j]
        

#plt.imshow(transport, cmap = plt.get_cmap('gray'))
        
# Import population map 

population = []
rowlist_pop = []

with open('population.txt',newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        population.append(row)
        for value in row: 
            rowlist_pop.append(value)

for i in range(len(population)): 
    for j in range(len(population[0])):
        pop_max = max(population[j])
        pop_min = min(population[j])
        
for i in range(len(population)):
    for j in range(len(population[0])):
        population[i][j] = (255/pop_max)*population[i][j]
  

#plt.imshow(population, cmap = plt.get_cmap('gray'))
        


canvas = None

class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title("Map")
        self.minsize(640,400)
        self.createWidget()
        self.myscale()
        
        
        
        
    def createWidget(self):
        l0 = Label(self, text = "Choose the maps")
        l0.place(x = 0, y = 1)
        
        l1=Label(self,text="Geology")
        l1.place(x = 200, y = 20)
        
        l2=Label(self,text="Population")
        l2.place(x = 200, y = 60)
        
        l3=Label(self,text="Transport")
        l3.place(x = 200, y = 100)
   
   
    def myscale(self):
        
       
        
        self.dou_var1 = DoubleVar()
        self.scale1 = Scale(self, from_=0, to=1,  orient='horizontal',variable=self.dou_var1)
        self.scale1.pack()
        
        self.dou_var2 = DoubleVar()
        self.scale2 = Scale(self, from_=0, to=1,  orient='horizontal', variable=self.dou_var2)
        self.scale2.pack()
        
        self.dou_var3 = DoubleVar()
        self.scale3 = Scale(self, from_=0, to=1,  orient='horizontal', variable = self.dou_var3)
        self.scale3.pack()
        
        
       
        Button(self, text="Show map", command = self.mergeMap).pack()
        Button(self, text="Save map", command = self.saveMap).pack()
        
         
    def mergeMap(self):
        global canvas, reshaped_to_2d, mergemap
        reshaped_to_2d = []
        mergemap = [] 
        

        f = Figure(figsize=(10,10), dpi=100)
        a = f.add_subplot(111)
        
        
        var1 = self.dou_var1.get()
        var2 = self.dou_var2.get()
        var3 = self.dou_var3.get()
        
       
    
        for i in range(len(geology)): 
            for j in range(len(geology[0])):
                if (var1  == 0) and (var2 == 0) and (var3 == 0):
                    self.quit()
                else:
                    mergemap.append((geology[i][j]*var1+ 
                                 transport[i][j]*var2+ 
                                 population[i][j]*var3)/(var1+var2+var3))
                       
        merge_max = max(mergemap)
        for i in range(len(mergemap)): 
            mergemap[i] = (255/merge_max)*mergemap[i]
        
        reshaped_to_2d = np.reshape(mergemap, (-1, 335))
        
        
        a.imshow(reshaped_to_2d, cmap = plt.get_cmap('gray'))
        if canvas: canvas.get_tk_widget().pack_forget()
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
      
        
        
    def saveMap(self): 
        global reshaped_to_2d, mergemap
        with open('mergedmap.csv', 'w') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(reshaped_to_2d)
            
  

if __name__ == "__main__" :
    root = Root()
    root.mainloop() 
  

