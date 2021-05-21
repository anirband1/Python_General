def color_avg(l_val1, l_val2):
    l_final = []

    for n in range(3):
        l_final.append(round((int(l_val1[n]) + int(l_val2[n])) / 2))

    return l_final


color1 = (
    input("Color 1:   ")).removeprefix("rgb(").removesuffix(")").split(", ")
color2 = (
    input("Color 2:   ")).removeprefix("rgb(").removesuffix(")").split(", ")

print(f"rgb({color_avg(color1, color2)})".replace("[", "").replace("]", ""))

sfg = "fskfhd"
