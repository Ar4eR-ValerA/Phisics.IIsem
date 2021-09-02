import math
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

fin = open('input.txt')

#Ввод
r_inside = float(fin.readline()) / 100
r_outside = float(fin.readline()) / 100
Vx_start = float(fin.readline())
L = float(fin.readline()) / 100

fin.close()

m = 9.1093837015 * (10 ** -31)
e = -1.602176634 * (10 ** -19)
t_end = L / Vx_start

array_t = []
array_Vy = []
array_x = []
array_y = []
array_ay = []

def ln(x):
    return math.log(x, math.e)

def E(h, u):
    return u / (ln(r_outside / r_inside) * h)

def a(h, U):
    return e * E(h, U) / m

def run(U, dt):
    array_t.clear()
    array_Vy.clear()
    array_x.clear()
    array_y.clear()
    array_ay.clear()

    t = 0
    y = r_inside + (r_outside + r_inside) / 2
    Vy = 0
    ay = a(y, U)
    x = 0

    array_t.append(t)
    array_Vy.append(Vy)
    array_y.append(y)
    array_x.append(x)
    array_ay.append(ay)

    while t < t_end and y > r_inside:
        t += dt
        y += Vy * dt
        Vy += ay * dt
        ay = a(y, U)
        x += Vx_start * dt

        array_t.append(t)
        array_Vy.append(Vy)
        array_y.append(y)
        array_x.append(x)
        array_ay.append(ay)

    return not(y > r_inside)

def bin_search(left, right, dt):
    while right - left > dt:
        middle = (left + right) / 2
        if run(middle, dt):
            right = middle
        else:
            left = middle
    return middle



U = bin_search(0, 40, 10**-11)

print("Время полёта:")
print(t_end)
print("Конечная скорость по y")
print(array_Vy[len(array_Vy) - 1])
print("Разница потенциалов:")
U = round(U, 3)
print(U)


plt.title("Зависимость высоты от расстояния")
plt.xlabel("Расстояние, м")
plt.ylabel("Высота, м")
plt.grid()
plt.plot(array_x, array_y)
plt.savefig("y(x).png")
plt.show()


plt.title("Зависимость скорости по y от времени")
plt.xlabel("Время, с")
plt.ylabel("Скорость, м/с")
plt.grid()
plt.plot(array_t, array_Vy)
plt.savefig("Vy(t).png")
plt.show()


plt.title("Зависимость ускорения по y от времени")
plt.xlabel("Время, с")
plt.ylabel("Ускорение, м/с^2")
plt.grid()
plt.plot(array_t, array_ay)
plt.savefig("ay(t).png")
plt.show()


plt.title("Зависимость высоты от времени")
plt.xlabel("Время, с")
plt.ylabel("Высота м")
plt.grid()
plt.plot(array_t, array_y)
plt.savefig("y(t).png")
plt.show()


#Сохранение отчёта
images = []
temp = Image.open("y(x).png")
images.append(temp.convert("RGB"))
temp = Image.open("Vy(t).png")
images.append(temp.convert("RGB"))
temp = Image.open("ay(t).png")
images.append(temp.convert("RGB"))
temp = Image.open("y(t).png")
images.append(temp.convert("RGB"))

temp = Image.new("RGB", (640, 200), (255, 255, 255))
stroke = ImageDraw.Draw(temp)
font = ImageFont.truetype("DejaVuSans.ttf", 18)
stroke.text((300, 140), "Разность потенциалов равна:\n" + str(U) + " В", fill=(0, 0, 0), align="left", font=font)

temp.convert("RGB").save("output.pdf", save_all=True, append_images=images)