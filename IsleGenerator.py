import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, Slider
import random

#create 2 column
fig, (ax_plot, ax_randomslider, ax_slider) = plt.subplots(1,3, figsize=(10,5))
fig.subplots_adjust(left=0.1, right=0.9, bottom=0.3)
fig.canvas.manager.set_window_title('Island Generator')
nbPoints = 20
fig.set_facecolor((0.15, 0.15, 0.17))
ax_plot.set_facecolor((0.17, 0.17, 0.20))

COLOR = 'white'
plt.rcParams['text.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR
ax_plot.set_title('Island Generator', color=COLOR)
ax_plot.tick_params(color=COLOR, labelcolor=COLOR)



#return the minimum
def min(liste):
    x = liste[0]
    for i in liste:
        if (i < x):
            x=i
    return x

#return the maximum
def max(liste):
    x = liste[0]
    for i in liste:
        if (i > x):
            x=i
    return x

def distance(point1, point2):
    return ((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)**(1/2)

class Btn:
    def __init__(self, listx, listy, listprime, basex, basey, reverse, nbPoints):
        self.listx = listx
        self.listy = listy
        self.prime = listprime
        self.basex = basex
        self.basey = basey
        self.reverse = reverse
        self.nbPoints = nbPoints
    # create mirror image of "graph"
    def mirror(self, event):
        x = []
        for i in self.listx:
            x.append(-i)
        self.listx = x
        ax_plot.plot(x,self.listy)
        ax_plot.set_title('Island Generator', color=COLOR)
        plt.draw()
    # center the graph 
    def center(self, event):
        text = event
        isX= True
        x = ""
        y = ""
        for i in text :
            if (isX and i!=','):
                x += i
            elif (i==','):
                isX = False
            elif(isX==False and i!=','):
                y += i
        x = int(x)
        y = int(y)
        xmin = min(self.listx)
        xmax = max(self.listx)
        ymin = min(self.listy)
        ymax = max(self.listy)
        x = ((xmax + xmin)/2) -x
        y = ((ymax + ymin)/2) -y
        ax_plot.clear()
        for i in range (len(self.listx)):
            self.listx[i] = self.listx[i] -x
            self.listy[i] = self.listy[i] - y
        ax_plot.plot(self.listx, self.listy)
        ax_plot.set_title('Island Generator', color=COLOR)
        plt.draw()

    def randomizeFreq(self, event):
        ax_plot.clear()
        for i in range(10):
            self.prime[i] = random.uniform(-2, 2)
        self.prime[-1] = self.prime[0]
        self.listx, self.listy = hermiteShape(self.basex, self.basey, self.prime, self.reverse, self.nbPoints)
        ax_plot.plot(self.listx,self.listy)
        ax_plot.set_title('Island Generator', color=COLOR)
        plt.draw()

    def randomizePoints(self, event):
        ax_plot.clear()

        centerX = 25
        centerY = 25        
        self.basex = [25.8, 25.3, 24.7, 24.2, 24, 24.2, 24.7, 25.3, 25.8, 26, 25.8]
        self.basey = [24.4, 24.1, 24.1, 24.4, 25, 25.6, 25.9, 25.9, 25.6, 25, 24.4]
        # Liste pour stocker les coordonnées agrandies
        agrandiX = []
        agrandiY = []
        for i in range(10):
            # Facteur d'agrandissement
            facteur_agrandissement = random.randint(5, 30)
            # Coordonnées du point courant
            x, y = self.basex[i], self.basey[i]

            # Calcul du vecteur reliant le point au centre
            vecteur_point_centre = [centerX - x, centerY - y]
            # Calcul de la distance entre le point et le centre
            dist_point_centre = distance((x, y), (centerX, centerY))

            # Calcul des nouvelles coordonnées agrandies
            nouvel_x = x + vecteur_point_centre[0] * facteur_agrandissement
            nouvel_y = y + vecteur_point_centre[1] * facteur_agrandissement

            # Ajout des nouvelles coordonnées à la liste
            agrandiX.append(nouvel_x)
            agrandiY.append(nouvel_y)
        agrandiX.append(agrandiX[0])
        agrandiY.append(agrandiY[0])

        self.basex = agrandiX
        self.basey = agrandiY


        self.listx, self.listy = hermiteShape(self.basex, self.basey, self.prime, self.reverse, self.nbPoints)
        ax_plot.plot(self.listx,self.listy)
        ax_plot.set_title('Island Generator', color=COLOR)
        plt.draw()

    def changeNbPoints(self, event):
        ax_plot.clear()
        self.nbPoints = int(event)
        self.listx, self.listy = hermiteShape(self.basex, self.basey, self.prime, self.reverse, self.nbPoints)
        ax_plot.plot(self.listx,self.listy)
        ax_plot.set_title('Island Generator', color=COLOR)
        plt.draw()

    #change the tangente with the sliders
    def update(self, event):
        ids, value = event
        ax_plot.clear()
        self.prime[ids-1] = value
        if(ids ==1 ):
            self.prime[10] = value
        self.listx, self.listy = hermiteShape(self.basex, self.basey, self.prime, self.reverse, self.nbPoints)
        ax_plot.plot(self.listx,self.listy)
        ax_plot.set_title('Island Generator', color=COLOR)
        plt.draw()
    

        

def phi1(teta):
    return ((teta-1)**2) * (2*teta + 1)

def phi2(teta):
    return (teta**2) * (-2*teta + 3)

def phi3(teta):
    return ((teta-1)**2) * (teta)

def phi4(teta):
    return (teta**2) * (teta - 1)

def hermite(x0,x1,y0,y1,y0p,y1p, nbPoint):
    x = [x0]
    y = [y0]
    step = (x1 -x0)/nbPoint
    for i in range (1, nbPoint-1):
        x.append(x[i-1]+ step)
        y.append(y0*phi1((x[i]-x0)/(x1-x0)) + y1*phi2((x[i]-x0)/(x1-x0)) + (x1-x0)*y0p*phi3((x[i]-x0)/(x1-x0)) + (x1-x0)*y1p*phi4((x[i]-x0)/(x1-x0)))
    x.append(x1)
    y.append(y1)
    return x,y

def hermiteShape(listBaseX, listeBaseY, listBesePrime, listReverse, nbPoints):
    allX = []
    allY = []
    for i in range (10):
        if ( listReverse[i]):
            x,y = hermite(listBaseX[i+1], listBaseX[i], listeBaseY[i+1], listeBaseY[i], listBesePrime[i+1], listBesePrime[i], nbPoints)
            x=x[::-1]
            y=y[::-1]
        else:
            x,y = hermite(listBaseX[i], listBaseX[i+1], listeBaseY[i], listeBaseY[i+1], listBesePrime[i], listBesePrime[i+1], nbPoints)
        allX.extend(x)
        allY.extend(y)
    return allX, allY

xbase = [9, 30, 18, 43, 37, 47, 45, 29, 30, 13, 9]
ybase = [30, 35, 48, 42, 29, 27, 16, 13, 8, 10, 30]
yprimebase = [-(37-30)/(-8-9), (3-35)/(-6-30), (0-48)/(-2-18), -(-2-42)/(0-43), -(-1-29)/(3-37), (-38-27)/(3-47), (-2-16)/(-1-45), -(3-13)/(0-29), -(0-8)/(-2-30), -(-18-10)/(-13-13), -(37-30)/(-8-9)]

isReverse = [False, True, False, True, False, False, True, False, True, True]

allX, allY = hermiteShape(xbase, ybase, yprimebase, isReverse, nbPoints)

#draw the graph
ax_plot.plot(allX, allY)

callback = Btn(allX, allY, yprimebase, xbase, ybase, isReverse, nbPoints)

#button to mirror
axprev = fig.add_axes([0.4, 0.6, 0.1, 0.075])
bMirror = Button(axprev, 'Mirror', color=(0.17, 0.17, 0.25), hovercolor=(0.20, 0.20, 0.35))
bMirror.on_clicked(callback.mirror)

#button to randomize frequency
axprev = fig.add_axes([0.4, 0.7, 0.16, 0.075])
bRandomFreq = Button(axprev, 'Tangentes Randomize', color=(0.17, 0.17, 0.25), hovercolor=(0.20, 0.20, 0.35))
bRandomFreq.on_clicked(callback.randomizeFreq)

#button to randomize points
axprev = fig.add_axes([0.4, 0.4, 0.16, 0.075])
bRandomPoints = Button(axprev, 'Points Randomize', color=(0.17, 0.17, 0.25), hovercolor=(0.20, 0.20, 0.35))
bRandomPoints.on_clicked(callback.randomizePoints)

#text box to input coordinate (ex: 5, 5)
ax_textbox = plt.axes([0.2, 0.05, 0.1, 0.05])
textbox_center = TextBox(ax_textbox, 'Center', color=(0.17, 0.17, 0.25), hovercolor=(0.20, 0.20, 0.35))
textbox_center.on_submit(callback.center)

# Make a horizontal slider to control the frequency.

# Define the positions for the sliders
slider_height = 0.03  # Height of each slider
slider_spacing = 0.05  # Spacing between sliders
slider_positions = [0.1 + i * (slider_height + slider_spacing) for i in range(10)]

sliders = []
for i in range(10):
    axfreq = fig.add_axes([0.7, slider_positions[i], 0.2, slider_height])
    init_frequency = yprimebase[i]
    slider = Slider(ax=axfreq, label=f'Tangente {i+1}', valmin=-3, valmax=3, valinit=init_frequency, color=(0.17, 0.17, 0.25))
    slider.on_changed(lambda val, index=i+1: callback.update([index, val]))
    sliders.append(slider)

# Slider to change frequency direction
axfreq = fig.add_axes([0.44, slider_positions[i], 0.1, slider_height])
slider = Slider(ax=axfreq, label='Tangentes direction', valmin=-2, valmax=2, valinit=init_frequency, color=(0.17, 0.17, 0.25))
for i in range(10):
    slider.on_changed(lambda val, index=i+1: callback.update([index, val]))
slider.label.set_size(7.5)
sliders.append(slider)

# Slider to change number of points
axfreq = fig.add_axes([0.44, 0.5, 0.1, slider_height])
init_frequency = nbPoints
slider = Slider(ax=axfreq, label='Level of Detail', valmin=1, valmax=20, valinit=init_frequency, valstep = 1, color=(0.17, 0.17, 0.25))
slider.on_changed(callback.changeNbPoints)
slider.label.set_size(7.5)
sliders.append(slider)



ax_randomslider.axis('off')
ax_slider.axis('off')
plt.show()