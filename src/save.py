from os import path, mkdir


root = "../assets/saves"


# reads save data into a list
def read_save(file, temp):
    if not path.exists(root):
        mkdir(root)

    if not path.exists(f"{root}/{file}"):
        save_to_file(file, temp)

    with open(f"{root}/{file}", "r") as f2:
        lis = []
        for li in f2.readlines():
            try:
                lis.append(int(li.replace("\n", "")))
            except ValueError:
                lis.append(li.replace("\n", ""))
        return lis


# writes list to file
def save_to_file(file, data):
    with open(f"{root}/{file}", "w") as f2:
        for li in list(map(str, data)):
            f2.write(li + "\n")


"""
save_template = [0, 0, 0]
save_data = read_save("save_files/save_{x}.txt".format(x=input("Save file: ")), save_template)

file = "save_files/save_{x}.txt".format(x=input("Save file: "))

save_data = read_save(file, save_template)

save_to_file(file, save_data)
"""
