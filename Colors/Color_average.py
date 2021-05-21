def color_avg(l_val1, l_val2):
    l_final = []

    for n in range(3):
        l_final.append((l_val1[n] + l_val2[n]) / 2)

    return l_final


color1 = list(input("Color 1:   "))
color2 = list(input("Color 2:   "))

print(f"rgb({color_avg(color1, color2)}")
