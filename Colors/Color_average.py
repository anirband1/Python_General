import subprocess


def color_avg(l_val1, l_val2):
    return [round((int(l_val1[n]) + int(l_val2[n])) / 2) for n in range(3)]


color1 = (
    input("Color 1:   ")).removeprefix("rgb(").removesuffix(")").split(", ")
color2 = (
    input("Color 2:   ")).removeprefix("rgb(").removesuffix(")").split(", ")

data = f"rgb({color_avg(color1, color2)})".replace("[", "").replace("]", "")

subprocess.run("pbcopy", universal_newlines=True, input=data)

print(data, "copied to clipboard")
