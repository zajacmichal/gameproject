import abc
from abc import abstractmethod
import math

import tkinter
from tkinter import *

import math

#deskryptor
class Quantity:
    _count = 0  # zlicza liczbę instancji deskryptora
    def __init__(self):
        cls = self.__class__  # odwołanie do klasy deskryptora
        prefix = cls.__name__
        index = cls._count
        # unikalan wartość atrybutu storage_name dla każdej instancji deskryptora
        self.storage_name = f'_{prefix}#{index}'
        cls._count += 1

    # implementujemy __get__ bo nazwa atrybuty zarządzanego jest inna niż storage_name
    def __get__(self, instance, owner):  # owner - odwołanie do klasy zarządzanej
        return getattr(instance, self.storage_name)  # !

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value) # !
        else:
            raise ValueError("wartość musi być większa od zera!")

#abstract class
class ConvexPolygon(abc.ABC):

    @abstractmethod
    def __init__(self,f_colour, o_colour):
        self.fill=f_colour
        self.outl=o_colour

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    @abstractmethod
    def draw(self):
        pass

#trojkat done
class Triangle(ConvexPolygon):
    a = Quantity()
    b = Quantity()
    c = Quantity()

    def __init__(self, fill, outl):
        super().__init__(fill, outl)


    def draw(self):
        #pobieranie danych
        self.a = float(self.entry_1.get())
        self.b = float(self.entry_2.get())
        self.c = float(self.entry_3.get())


        A=(0,0)
        B=(self.c, 0)
        hc=(2 * (self.a**2*self.b**2 + self.b**2*self.c**2 + self.c**2*self.a**2) - (self.a**4 + self.b**4 + self.c**4))**0.5/(2.*self.c)
        dx = (self.b**2 - hc**2)**0.5
        if abs((self.c-dx)**2 + hc**2 -self.a**2)>0.01: dx = -dx
        C=(dx, hc)

        coords = [int((x+1) * 75) for x in A+B+C]

        rysowanie = Tk()
        canvas = Canvas(rysowanie, width=500, height=500)

        canvas.create_text(100,480, font="italic",text=f"Area: {self.area()}, Perimeter:{self.perimeter()}")

        canvas.create_polygon(*coords, fill=self.fill, outline=self.outl)
        canvas.pack()

    #pole powierzchni
    def area(self):
        return float(self.perimeter())/2

    #obwod
    def perimeter(self):
        return self.a + self.b + self.c

    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)
        self.label_2 = Label(root, text="Podaj bok B: ")
        self.entry_2 = Entry(root)
        self.label_3 = Label(root, text="Podaj bok C: ")
        self.entry_3 = Entry(root)


        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)
        self.label_2.grid(row=1, column=0)
        self.entry_2.grid(row=1, column=1)
        self.label_3.grid(row=2, column=0)
        self.entry_3.grid(row=2, column=1)


        self.button_1.grid(row=3, column=1)

#trojkat rownoramienny
class IsoscelesTriangle(Triangle):
    a = Quantity()
    b = Quantity()

    def __init__(self, fill, outl):
        super().__init__(fill, outl)

    def draw(self):
        self.a = float(self.entry_1.get())
        self.b = float(self.entry_2.get())

        A = (0, 0)
        B = (self.b, 0)
        hc = (2 * (self.a ** 2 * self.b ** 2 + self.b ** 2 * self.b ** 2 + self.b ** 2 * self.a ** 2) - (
                    self.a ** 4 + self.b ** 4 + self.b ** 4)) ** 0.5 / (2. * self.b)
        dx = (self.b ** 2 - hc ** 2) ** 0.5
        if abs((self.b - dx) ** 2 + hc ** 2 - self.a ** 2) > 0.01: dx = -dx
        C = (dx, hc)

        coords = [int((x + 1) * 75) for x in A + B + C]

        rysowanie = Tk()
        canvas = Canvas(rysowanie, width=500, height=500)

        canvas.create_text(100, 480, font="italic", text=f"Area: {self.area()}, Perimeter:{self.perimeter()}")

        canvas.create_polygon(*coords, fill=self.fill, outline=self.outl)
        canvas.pack()



    def area(self):
        return float(self.perimeter())/2

    def perimeter(self):
        return self.a+self.b+self.b

    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)
        self.label_2 = Label(root, text="Podaj bok B: ")
        self.entry_2 = Entry(root)


        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)
        self.label_2.grid(row=1, column=0)
        self.entry_2.grid(row=1, column=1)


        self.button_1.grid(row=2, column=1)

#trojkat rownoboczny
class EquilateralTriangl(Triangle):
    a = Quantity()


    def __init__(self, fill, outl):
        super().__init__(fill, outl)

    def draw(self):
        self.a = float(self.entry_1.get())


        A = (0, 0)
        B = (self.a, 0)
        hc = (2 * (self.a ** 2 * self.a ** 2 + self.a ** 2 * self.a ** 2 + self.a ** 2 * self.a ** 2) - (
                self.a ** 4 + self.a ** 4 + self.a ** 4)) ** 0.5 / (2. * self.a)
        dx = (self.a ** 2 - hc ** 2) ** 0.5
        if abs((self.a - dx) ** 2 + hc ** 2 - self.a ** 2) > 0.01: dx = -dx
        C = (dx, hc)

        coords = [int((x + 1) * 75) for x in A + B + C]

        rysowanie = Tk()
        canvas = Canvas(rysowanie, width=500, height=500)

        canvas.create_text(100, 480, font="italic", text=f"Area: {self.area()}, Perimeter:{self.perimeter()}")

        canvas.create_polygon(*coords, fill=self.fill, outline=self.outl)
        canvas.pack()

    def area(self):
        return float(self.perimeter())/2

    def perimeter(self):
        return 3*self.a

    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)


        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)


        self.button_1.grid(row=1, column=1)

#czworotkat
class ConvexQuadrilateral(ConvexPolygon):
    a = Quantity()
    b = Quantity()
    c = Quantity()
    d = Quantity()
    ang_1 = Quantity()
    ang_2 = Quantity()
    ang_3 = Quantity()


    def __init__(self, f_colour, o_colour):
        super().__init__(f_colour,o_colour)



    def area(self):
        h = self.b * math.sin(math.radians(self.angle1))
        return self.a * h

    def perimeter(self):
        return self.a+self.b+self.c+self.d

    def draw(self):
        self.a = float(self.entry_1.get())
        self.b = float(self.entry_2.get())
        self.c = float(self.entry_3.get())
        self.d = float(self.entry_4.get())

        self.angle1 = float(self.entry_5.get())
        self.angle2 = float(self.entry_6.get())
        self.angle3 = float(self.entry_7.get())
        self.angle4= 360 - (self.angle1 + self.angle2 + self.angle3)

        side_1 = self.a * math.cos(math.radians(self.angle1))
        side_2 = self.b * math.sin(math.radians(self.angle2))
        side_3 = self.c * math.cos(math.radians(self.angle3))
        side_4 = self.d * math.sin(math.radians(self.angle4))

        coords = [
            0,0,
            side_1, 0,
            self.a + side_3, side_4,
            side_3,side_4]

        root = Tk()
        canvas = Canvas(root, width=500, height=500)
        canvas.create_polygon(*coords, fill=self.fill, outline=self.outl)

        canvas.create_text(100, 480, font="italic", text=f"Area: {round(self.area(),2)}, Perimeter:{self.perimeter()}")

        canvas.pack()



    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)
        self.label_2 = Label(root, text="Podaj bok B: ")
        self.entry_2 = Entry(root)
        self.label_3 = Label(root, text="Podaj bok C: ")
        self.entry_3 = Entry(root)
        self.label_4 = Label(root, text="Podaj bok D: ")
        self.entry_4 = Entry(root)

        self.label_5 = Label(root, text="Podaj pierwszy kat: ")
        self.entry_5 = Entry(root)
        self.label_6 = Label(root, text="Podaj drugi kat: ")
        self.entry_6 = Entry(root)
        self.label_7 = Label(root, text="Podaj trzeci kat: ")
        self.entry_7 = Entry(root)

        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)
        self.label_2.grid(row=1, column=0)
        self.entry_2.grid(row=1, column=1)
        self.label_3.grid(row=2, column=0)
        self.entry_3.grid(row=2, column=1)
        self.label_4.grid(row=3, column=0)
        self.entry_4.grid(row=3, column=1)

        self.label_5.grid(row=4, column=0)
        self.entry_5.grid(row=4, column=1)
        self.label_6.grid(row=5, column=0)
        self.entry_6.grid(row=5, column=1)
        self.label_7.grid(row=6, column=0)
        self.entry_7.grid(row=6, column=1)

        self.button_1.grid(row=7, column=1)


#pieciokat
class RegularPentagon(ConvexPolygon):
    a = Quantity()

    def __init__(self, fill, outl):
        super().__init__(fill, outl)

    def area(self):
        return 5*(self.a**2/4) *(1/math.tan(math.radians(36)))

    def perimeter(self):
        return 5 * self.a

    def draw(self):
        start_x = 200
        start_y = 200
        angle = 360/5
        self.a = float(self.entry_1.get())
        rysuj = tkinter.Tk()
        self.canvas2 = tkinter.Canvas(rysuj, height=600, width=600)
        label1 = Label(rysuj)
        label1["text"] = self.area()
        label1.grid(row=0, column=0)
        label2 = Label(rysuj)
        label2["text"] = self.perimeter()
        label2.grid(row=0, column=1)

        self.canvas2.grid(row=1, column=0)
        for i in range(5):
            end_x = start_x + self.a * math.cos(math.radians(angle * i))
            end_y = start_y + self.a * math.sin(math.radians(angle * i))
            self.canvas2.create_polygon(start_x, start_y, end_x, end_y, fill=self.fill, outline=self.outl)
            start_x = end_x
            start_y = end_y

    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj rozmiar boku")
        self.entry_1 = Entry(root)
        self.button_1 = Button(root, text="Rysuj", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)
        self.button_1.grid(row=2, column=1)



#szesciokat
class RegularHexagon(ConvexPolygon):
    a = Quantity()

    def __init__(self, fill, outl):
        super().__init__(fill, outl)

    def area(self):
        return 6 * ((self.a ** 2) / 2) * math.sin(60)

    def perimeter(self):
        return 6 * self.a

    def draw(self):
        start_x = 200
        start_y = 200
        angle = 60
        self.a = float(self.entry_1.get())
        rysuj = tkinter.Tk()
        self.canvas2 = tkinter.Canvas(rysuj, height=600, width=600)
        label1 = Label(rysuj)
        label1["text"] = self.area()
        label1.grid(row=0, column=0)
        label2 = Label(rysuj)
        label2["text"] = self.perimeter()
        label2.grid(row=0, column=1)

        self.canvas2.grid(row=1, column=0)
        for i in range(6):
            end_x = start_x + self.a * math.cos(math.radians(angle * i))
            end_y = start_y + self.a * math.sin(math.radians(angle * i))
            self.canvas2.create_polygon(start_x, start_y, end_x, end_y, fill=self.fill, outline=self.outl)
            start_x = end_x
            start_y = end_y

    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj rozmiar boku")
        self.entry_1 = Entry(root)
        self.button_1 = Button(root, text="Rysuj", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)
        self.button_1.grid(row=2, column=1)


#osmiokat
class RegularOctagon(ConvexPolygon):
    a = Quantity()

    def __init__(self, fill, outl):
        super().__init__(fill, outl)

    def area(self):
        return 2*(1+math.sqrt(2))*self.a**2

    def perimeter(self):
        return 8 * self.a

    def draw(self):
        start_x = 200
        start_y = 200
        angle = 360/8
        self.a = float(self.entry_1.get())
        rysuj = tkinter.Tk()
        self.canvas2 = tkinter.Canvas(rysuj, height=600, width=600)
        label1 = Label(rysuj)
        label1["text"] = self.area()
        label1.grid(row=0, column=0)
        label2 = Label(rysuj)
        label2["text"] = self.perimeter()
        label2.grid(row=0, column=1)

        self.canvas2.grid(row=1, column=0)
        for i in range(8):
            end_x = start_x + self.a * math.cos(math.radians(angle * i))
            end_y = start_y + self.a * math.sin(math.radians(angle * i))
            self.canvas2.create_polygon(start_x, start_y, end_x, end_y, fill=self.fill, outline=self.outl)
            start_x = end_x
            start_y = end_y

    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj rozmiar boku")
        self.entry_1 = Entry(root)
        self.button_1 = Button(root, text="Rysuj", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=1, column=0)
        self.button_1.grid(row=2, column=1)


#romb done
class Rhombus(ConvexPolygon):
    a = Quantity()
    angle = Quantity()

    def __init__(self, f_colour, o_colour):
        super().__init__(f_colour, o_colour)

    def perimeter(self):
        return self.a*4

    def area(self):
        return round(self.a**2*math.sin(math.radians(self.angle)),2)

    def draw(self):
        self.a = float(self.entry_1.get())
        self.angle = float(self.entry_2.get())

        a_cos = self.a * math.cos(math.radians(self.angle))
        b_sin = self.a * math.sin(math.radians(self.angle))

        polygon = [
            0.0, 0.0,
            0.0 + self.a, 0.0,
            0.0 + self.a + a_cos, 0.0 + b_sin,
            0.0 + a_cos, 0.0 + b_sin
        ]

        root = Tk()
        canvas = Canvas(root, width=500, height=500)
        w = canvas.create_polygon(polygon, fill=self.fill, outline=self.outl)

        canvas.create_text(100, 480, font="italic", text=f"Area: {self.area()}, Perimeter:{self.perimeter()}")
        canvas.scale(w,0,0,20,20) #powiekszenie
        canvas.pack()


    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)

        self.label_2 = Label(root, text="Podaj kąt ostry: ")
        self.entry_2 = Entry(root)

        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)

        self.label_2.grid(row=1, column=0)
        self.entry_2.grid(row=1, column=1)

        self.button_1.grid(row=2, column=1)

#kwadrat done
class Square(Rhombus):#kwadrat
    a = Quantity()

    def __init__(self, f_colour, o_colour):
        super().__init__(f_colour, o_colour)

    def area(self):
        return self.a**2

    def perimeter(self):
        return 4*self.a

    def draw(self):
        self.a = float(self.entry_1.get())

        rysowanie = Tk()
        canvas = Canvas(rysowanie, width=500, height=500)

        canvas.create_text(100, 480, font="italic", text=f"Area: {self.area()}, Perimeter:{self.perimeter()}")

        w = canvas.create_rectangle((0,0,self.a,self.a), fill=self.fill, outline=self.outl)
        canvas.scale(w,0,0,20,20)
        canvas.pack()


    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)


        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)

        self.button_1.grid(row=1, column=1)

#rownoleglobok
class Parallelogram(Rhombus):
    a = Quantity()
    b = Quantity()
    c = Quantity()

    def __init__(self, f_colour, o_colour):
        super().__init__(f_colour, o_colour)

    def perimeter(self):
        return round(2*self.a + 2* self.b,2)

    def area(self):
        return round(self.a * self.b *math.sin(math.radians(self.angle)),2)

    def draw(self):
        self.a = float(self.entry_1.get())
        self.b = float(self.entry_2.get())
        self.angle = float(self.entry_3.get())

        a_cos = self.a * math.cos(math.radians(self.angle))
        b_sin = self.b * math.sin(math.radians(self.angle))

        polygon = [
            0.0, 0.0,
            0.0 + self.a + self.b, 0.0,
            0.0 + self.a + a_cos + self.b, 0.0 + b_sin,
            0.0 + a_cos, 0.0 + b_sin
        ]

        root = Tk()
        canvas = Canvas(root, width=500, height=500)
        w = canvas.create_polygon(polygon, fill=self.fill, outline=self.outl)

        canvas.create_text(100, 480, font="italic", text=f"Area: {self.area()}, Perimeter:{self.perimeter()}")

        canvas.pack()

    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)
        self.label_2 = Label(root, text="Podaj bok B: ")
        self.entry_2 = Entry(root)
        self.label_3 = Label(root, text="Podaj kat ostry: ")
        self.entry_3 = Entry(root)

        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)
        self.label_2.grid(row=1, column=0)
        self.entry_2.grid(row=1, column=1)
        self.label_3.grid(row=2,column=0)
        self.entry_3.grid(row=2,column=1)


        self.button_1.grid(row=3, column=1)

#deltoid nie wiem
class Kite(ConvexPolygon):
    a = Quantity()
    b = Quantity()
    angle = Quantity()

    def __init__(self, f_colour, o_colour):
        super().__init__(f_colour, o_colour)


    def perimeter(self):
        return round(2 * self.a + 2 * self.b, 2)

    def area(self):
        return self.a*self.b*math.sin(math.radians(self.angle))

    def draw(self):
        self.a = float(self.entry_1.get())
        self.b = float(self.entry_2.get())
        self.angle = float(self.entry_3.get())

        p1 = 2*self.a *math.cos(math.radians(180 - self.angle / 2))
        p2 = self.a * math.cos(math.radians(self.angle /2)) + self.b *math.cos(math.radians((180 - self.angle) / 2))
        h = math.sqrt(math.pow(self.a,2) - (math.pow(p1,2)) / 4)

        root = Tk()
        canvas = Canvas(root, width=500, height=500)

        canvas.update()
        A = (100,100)
        B = (100 + p2, 100)

        S = (p2 +100 - h, 100)

        C = (S[0], 100 - p1 / 2)
        D = (S[0], 100 + p1 / 2)

        coords = [int((x + 1)*2) for x in A + C + B + D]
        print(coords)


        min_c = min(coords)
        if min_c < 0:
            for i, coord in enumerate(coords):
                if i % 2 != 0:
                    coords[i] = coord - (min_c * 2)

        while max(coords) > 100:
            for i, coord in enumerate(coords):
                coords[i] = coord / 2

        canvas.create_polygon(*coords, fill=self.fill, outline=self.outl, width=6)



    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)
        self.label_2 = Label(root, text="Podaj bok B: ")
        self.entry_2 = Entry(root)
        self.label_3 = Label(root, text="Podaj kat: ")
        self.entry_3 = Entry(root)

        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)
        self.label_2.grid(row=1, column=0)
        self.entry_2.grid(row=1, column=1)
        self.label_3.grid(row=2, column=0)
        self.entry_3.grid(row=2, column=1)

        self.button_1.grid(row=3, column=1)

#prostokat
class Rectangle(Parallelogram):
    a = Quantity()
    b= Quantity()

    def sprawdz(self):
        return
    def __init__(self, f_colour, o_colour):
        super().__init__(f_colour, o_colour)

    def perimeter(self):
        return super().perimeter()

    def area(self):
        return self.a*self.b

    def draw(self):
        self.a = float(self.entry_1.get())
        self.b = float(self.entry_2.get())

        rysowanie = Tk()
        canvas = Canvas(rysowanie, width=500, height=500)

        canvas.create_text(100, 480, font="italic", text=f"Area: {self.area()}, Perimeter:{self.perimeter()}")

        w = canvas.create_rectangle((0, 0, self.a + self.b, self.a), fill=self.fill, outline=self.outl)
        canvas.scale(w, 0, 0, 10, 10)
        canvas.pack()

    def rysuj(self):
        root = tkinter.Tk()
        self.label_1 = Label(root, text="Podaj bok A: ")
        self.entry_1 = Entry(root)
        self.label_2 = Label(root, text="Podaj bok B: ")
        self.entry_2 = Entry(root)

        self.button_1 = Button(root, text="Rysuj!", command=self.draw)

        self.label_1.grid(row=0, column=0)
        self.entry_1.grid(row=0, column=1)
        self.label_2.grid(row=1, column=0)
        self.entry_2.grid(row=1, column=1)

        self.button_1.grid(row=2, column=1)

def fill_colours():

    f_c=['red','black','green','blue','yellow']

    print("wybierz 1 z kolorów: ")
    print(f_c)
    x=input()

    if x in f_c:
        return x
    else:
        print("wpisz kolor z listy!")


def out_colours():

    f_c=['red','black','green','blue','yellow']

    print("wybierz 1 z kolorów: ")
    print(f_c)
    y=input()

    if y in f_c:
        return y
    else:
        print("podales zly kolor!")
        return 0


x=fill_colours()
y=out_colours()


my_window=Tk()



trojkat = Triangle(x,y)
t_rownoramienny = IsoscelesTriangle(x,y)
t_rownoboczny = EquilateralTriangl(x,y)
kwadrat = Square(x,y)
romb = Rhombus(x,y)
rownoleglobok = Parallelogram(x,y)
prostokat = Rectangle(x,y)
czworokat = ConvexQuadrilateral(x,y)
pieciokat = RegularPentagon(x,y)
szesciokat = RegularHexagon(x,y)
osmiokat = RegularOctagon(x,y)
deltoid = Kite(x,y)

print(Kite.__mro__)

button_1 = Button(my_window, text= "trojkat",command=trojkat.rysuj)
button_1.grid(row=0,column=0)

button_2 = Button(my_window,text="trojkat rownoramienny", command=t_rownoramienny.rysuj)
button_2.grid(row=0, column=1)

button_3 = Button(my_window,text="trojkat rownoboczny",command=t_rownoboczny.rysuj)
button_3.grid(row=0, column=2)

button_4 = Button(my_window,text="kwadrat", command=kwadrat.rysuj)
button_4.grid(row=0, column=3)

button_5 = Button(my_window,text="romb", command = romb.rysuj)
button_5.grid(row=0, column=4)

button_6 = Button(my_window,text="rownoleglobok", command = rownoleglobok.rysuj)
button_6.grid(row=0, column=5)

button_7 = Button(my_window,text="prostokat", command =prostokat.rysuj)
button_7.grid(row=0, column=6)

button_8 = Button(my_window,text="czworokat", command =czworokat.rysuj)
button_8.grid(row=0, column=7)

button_9 = Button(my_window,text="pieciokat", command =pieciokat.rysuj)
button_9.grid(row=0, column=8)

button_10 = Button(my_window,text="szesciokat", command =szesciokat.rysuj)
button_10.grid(row=0, column=9)

button_10 = Button(my_window,text="osmio", command =osmiokat.rysuj)
button_10.grid(row=0, column=10)



my_window.mainloop()

#czworokat jako przekatne