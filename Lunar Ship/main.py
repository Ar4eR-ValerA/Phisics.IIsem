import math
import matplotlib.pyplot as plt

fin = open('input.txt')
fout = open('output.txt', 'w')

#Ввод
distance_os = float(fin.readline()) * 1000
height_os = float(fin.readline()) * 1000
fin.close()

radius = 1738000
g = 1.62
G = 6.6743015151515152 * (10 ** -11)
M_moon = (g * 1738000 ** 2) / G

array_x = []
array_y = []
array_t = []
array_h = []
array_a = []


def height(x, y):
    return math.sqrt(x ** 2 + y ** 2) - radius


def moon():
    dx = 10
    x = -radius
    y = 0
    array_x.append(x)
    array_y.append(y)

    while x < radius:
        x += dx
        y = math.sqrt(radius ** 2 - x ** 2)
        array_x.append(x)
        array_y.append(y)

    while x > -radius:
        x -= dx
        y = -math.sqrt(radius ** 2 - x ** 2)
        array_x.append(x)
        array_y.append(y)

    while x < 0:
        x += dx
        y = math.sqrt(radius ** 2 - x ** 2)
        array_x.append(x)
        array_y.append(y)


def clear():
    array_x.clear()
    array_y.clear()
    array_t.clear()
    array_h.clear()
    array_a.clear()


def append(x, y, t, h, ay):
    array_x.append(x)
    array_y.append(y)
    array_t.append(t)
    array_h.append(h)
    array_a.append(ay)


def print_graphics(stage):
    plt.title("#" + str(stage) + " Высота от времени")
    plt.ylabel("Высота, м")
    plt.xlabel("Время, с")
    plt.plot(array_t, array_h)
    plt.savefig("#" + str(stage) + " Высота.png")
    plt.show()

    plt.title("#" + str(stage) + " Ускорение от времени")
    plt.ylabel("Ускорение, м/с^2")
    plt.xlabel("Время, с")
    plt.plot(array_t, array_a)
    plt.savefig("#" + str(stage) + " Ускорение.png")
    plt.show()

    plt.title("#" + str(stage) + " Орбита ")
    plt.ylabel("Координата y")
    plt.xlabel("Координата x")
    plt.plot(array_x, array_y, color="red")
    plt.savefig("#" + str(stage) + " Орбита.png")
    plt.show()


def full_a(ax, ay):
    return math.sqrt(ax ** 2 + ay ** 2)

def full_V(Vx, Vy):
    return math.sqrt(Vx ** 2 + Vy ** 2)

def tangent_angle_cos(x, y):
    return x / math.sqrt(x ** 2 + y ** 2)

def perpendicular_angle_cos(x, y):
    return y / math.sqrt(x ** 2 + y ** 2)

def next_a(x, y, Fx_mg, Fy_mg, Fx, Fy):
    if y > 0:
        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
    else:
        ax = Fx - Fx_mg
        ay = Fy + Fy_mg

    return  (ax, ay)

def out(Vx, Vy, x, y, alpha, dm_fuel, t):
    fout.write("                Скорости по x и y: " + str(int(Vx)) + " м/с " + str(int(Vy)) + " м/с\n")
    fout.write("              Координаты по x и y: " + str(int(x)) + " " + str(int(y)) + "\n")
    fout.write("Угол направления корабля к оси OX: " + str(int(alpha)) + " градусов\n")
    fout.write("                   Расход топлива: " + str(int(dm_fuel)) + " кг/с\n")
    fout.write("          Время запуска двигателя: " + str(round(t, 4)) + " с\n")
    fout.write("-------------------------------------------------------------------------\n")

def run(dt):
    clear()

    m_spacecraft = 2200
    t = 0
    Vx = 0
    Vy = 0
    ax = 0
    ay = 0
    m_fuel = 4000
    y = radius
    x = 0


    #Первый этап: Вертикальный взлёт при 8 кг/с
    Vx_, Vy_, x_, y_, t_ = Vx, Vy, x, y, t
    while height(x, y) < height_os / 3 and ay < 29.43 and m_fuel > 0 and (height(x, y) > 0 or t == 0):
        t += dt
        F = 3660 * 8 * dt
        F_mg = g * (m_fuel + m_spacecraft) * dt

        ay = F - F_mg
        Vy += ay * dt
        y += Vy * dt
        m_fuel -= 8 * dt

        append(x, y, t, height(x, y), ay)
    print_graphics(1)
    out(Vx_, Vy_, x_, y_, 0, 8, t - t_)


    #Второй этап: Наклон на 30 градусов при 6 кг/с
    Vx_, Vy_, x_, y_, t_ = Vx, Vy, x, y, t
    while height(x, y) < height_os and full_a(ax, ay) < 29.43 and m_fuel > 0 and height(x, y) > 0:
        t += dt
        Fx = 3660 * 6 * dt * math.cos(math.radians(30))
        Fy = 3660 * 6 * dt * math.sin(math.radians(30))
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        m_fuel -= 6 * dt

        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(2)
    out(Vx_, Vy_, x_, y_, 30, 6, t - t_)

    #Третий этап торможение по направлению перпендикуляра к поверхности до верт. скорости почти равно 0
    while Vy > 5.5 and full_a(ax, ay) < 29.43 and m_fuel > 0 and height(x, y) > 100:
        t += dt
        out(Vx, Vy, x, y, math.degrees(math.acos(perpendicular_angle_cos(x, y))) - 90, 4, dt)
        Fx = 3660 * 4 * dt * math.cos(math.radians(math.degrees(math.acos(perpendicular_angle_cos(x, y)))) - 90)
        Fy = 3660 * 4 * dt * math.sin(math.radians(math.degrees(math.acos(perpendicular_angle_cos(x, y)))) - 90)
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        m_fuel -= 4 * dt

        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(3)


    #Четвёртый этап: Разгон до первой космической по направлению касательной к поверхности
    while full_V(Vx, Vy) < math.sqrt(G * M_moon / (radius + height_os)) and full_a(ax, ay) < 29.43:
        t += dt
        out(Vx, Vy, x, y, math.degrees(math.acos(tangent_angle_cos(x, y))) - 90, 4, dt)
        Fx = 3660 * 5.5 * dt * math.cos(math.radians(math.degrees(math.acos(tangent_angle_cos(x, y)))) - 90)
        Fy = 3660 * 5.5 * dt * math.sin(math.radians(math.degrees(math.acos(tangent_angle_cos(x, y)))) - 90)
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        m_fuel -= 5.5 * dt

        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(4)

    #Расчёт времени ождания 1
    t_os = 0
    x_os = 0
    y_os = radius + height_os
    while math.fabs(75945 - x_os) > 100 or math.fabs(1793390 - y_os) > 100 and t_os < 1000:
        t_os += dt
        x_os += full_V(Vx, Vy) * dt * math.cos(full_V(Vx, Vy) * t_os / (radius + height_os))
        y_os -= full_V(Vx, Vy) * dt * math.sin(full_V(Vx, Vy) * t_os / (radius + height_os))

    t_wait = t_os

    #Расчёт времени ождания 2
    t_os = 0
    x_os = 0
    y_os = radius + height_os
    while (math.fabs(x - x_os) > 100 or math.fabs(y - y_os) > 100) and t_os < 1000:
        t_os += dt
        x_os += full_V(Vx, Vy) * dt * math.cos(full_V(Vx, Vy) * t_os / (radius + height_os))
        y_os -= full_V(Vx, Vy) * dt * math.sin(full_V(Vx, Vy) * t_os / (radius + height_os))


    m_spacecraft -= 200

    fout.write("Время ожидания до взлёта: " + str(round(math.fabs(t - t_os + t_wait), 0)) + " секунд\n")
    fout.write("-------------------------------------------------------------------------\n")

    clear()
    t_ = t
    #Пятый этап: Ожидание позиции для торможения
    while math.fabs(x + 144027) > 100 or t < 4000:
        t += dt
        t_os += dt
        x += full_V(Vx, Vy) * dt * math.cos(full_V(Vx, Vy) * t_os / (radius + height_os))
        y += full_V(Vx, Vy) * dt * -math.sin(full_V(Vx, Vy) * t_os / (radius + height_os))

        append(x, y, t, height_os, g)
    print_graphics(5)

    fout.write("Время ожидания до торможения для схода с орбиты: " + str(round(math.fabs(t - t_), 0)) + " секунд\n")
    fout.write("-------------------------------------------------------------------------\n")

    Vx = math.sqrt(G * M_moon / (radius + height_os)) * math.cos(math.radians(math.degrees(math.acos(tangent_angle_cos(x, y)))) - 90)
    Vy = math.sqrt(G * M_moon / (radius + height_os)) * math.sin(math.radians(math.degrees(math.acos(tangent_angle_cos(x, y)))) - 90)

    clear()
    #Шестой этап: Торможение с углом 45 градусов по направлению касательной к поверхности до скорости 0
    while full_V(Vx, Vy) > 0 and full_a(ax, ay) < 29.43 and t < 8000 and Vx > 0 and Vy < 0:
        t += dt
        out(Vx, Vy, x, y, math.degrees(math.acos(tangent_angle_cos(x, y))) - 135, 4, dt)
        Fx = -3660 * 5 * dt * math.cos(math.radians(math.degrees(math.acos(tangent_angle_cos(x, y)))) - 135)
        Fy = -3660 * 5 * dt * math.sin(math.radians(math.degrees(math.acos(tangent_angle_cos(x, y)))) - 135)
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = -g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy + Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        m_fuel -= 5 * dt
        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(6)

    #Седьмой этап: Торможение по горизорнтали
    Vx_, Vy_, x_, y_, t_ = Vx, Vy, x, y, t
    while height(x, y) > 0 and full_a(ax, ay) < 29.43 and Vx > 100 and Vy < 10:
        t += dt
        Fx = -3660 * 5 * dt * math.cos(math.radians(0))
        Fy = 3660 * 5 * dt * math.sin(math.radians(0))
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        m_fuel -= 5 * dt
        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(7)
    out(Vx_, Vy_, x_, y_, 0, 5, t - t_)

    #Восьмой этап: Торможение по вертикали
    Vx_, Vy_, x_, y_, t_ = Vx, Vy, x, y, t
    while height(x, y) > 0 and full_a(ax, ay) < 29.43 and Vy < 0:
        t += dt
        Fx = -3660 * 7 * dt * math.cos(math.radians(90))
        Fy = 3660 * 7 * dt * math.sin(math.radians(90))
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        m_fuel -= 7 * dt
        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(8)
    out(Vx_, Vy_, x_, y_, 90, 7, t - t_)

    #Девятый этап: Торможение по горизорнтали
    Vx_, Vy_, x_, y_, t_ = Vx, Vy, x, y, t
    while height(x, y) > 0 and full_a(ax, ay) < 29.43 and Vx > 0.6:
        t += dt
        Fx = -3660 * 7 * dt * math.cos(math.radians(0))
        Fy = 3660 * 7 * dt * math.sin(math.radians(0))
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        m_fuel -= 7 * dt
        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(9)
    out(Vx_, Vy_, x_, y_, 0, 7, t - t_)

    #Десятый этап: ожидание до высоты 4460м
    t_ = t
    while height(x, y) > 4460 and full_a(ax, ay) < 29.43:
        t += dt
        Fx = 0
        Fy = 0
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(10)
    fout.write("Время ожидания до торможения для посадки: " + str(int(t - t_)) + " секунд\n")
    fout.write("-------------------------------------------------------------------------\n")

    #Одинадцатый этап: Торможение по вертикали
    Vx_, Vy_, x_, y_, t_ = Vx, Vy, x, y, t
    while height(x, y) > 0 and full_a(ax, ay) < 29.43 and Vy < 0:
        t += dt
        Fx = -3660 * 2.7 * dt * math.cos(math.radians(90))
        Fy = 3660 * 2.7 * dt * math.sin(math.radians(90))
        Fx_mg = g * (m_fuel + m_spacecraft) * dt * (x / math.sqrt(x ** 2 + y ** 2))
        Fy_mg = g * (m_fuel + m_spacecraft) * dt * math.sqrt(1 - (x / math.sqrt(x ** 2 + y ** 2)) ** 2)

        ax = Fx - Fx_mg
        ay = Fy - Fy_mg
        Vx += ax * dt
        Vy += ay * dt
        x += Vx * dt
        y += Vy * dt
        m_fuel -= 2.7 * dt
        append(x, y, t, height(x, y), full_a(ax, ay))
    print_graphics(11)
    out(Vx_, Vy_, x_, y_, 90, 2.7, t - t_)

run(0.001)
