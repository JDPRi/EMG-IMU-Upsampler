
#by Joe Richards

import os, fnmatch, array, pip, tkinter as tk
from tkinter import filedialog, StringVar
from colour import Color

allFiles=[]
mainbg = Color("#99AABB")
root = tk.Tk()
root.configure(bg=mainbg)
ogfoldervar = StringVar()
destfoldervar = StringVar()
root.title("EMG - IMU Upsampler (Version 0.1.2)")


root.minsize(600,300)
root.maxsize(600,300)

og_folder=""
target_folder=""

def find_ogfolder():

    global og_folder
    og_folder =filedialog.askdirectory()
    ogfoldervar.set(og_folder)
    
def find_destfolder():

    global target_folder
    target_folder=filedialog.askdirectory()
    destfoldervar.set(target_folder)


ogfolderbttn=tk.Button(root, text="choose folder", borderwidth = 2, command=find_ogfolder)
ogfolderlb = tk.Entry(root,textvariable=ogfoldervar, borderwidth=2,width=70)
        
destfolderbttn = tk.Button(root, text ="choose folder", borderwidth =2, command =find_destfolder)
destfolderlb = tk.Entry(root, textvariable=destfoldervar, borderwidth=2, width=70)


file_types = ["Firings", "MFR", "MUAPs", "stats", "all"]


ogfolderbttn.place(x=50,y=15)
ogfolderlb.place(x=150,y=15)
destfolderbttn.place(x=50,y=45)
destfolderlb.place(x=150,y=45)

copywritelb = tk.Label(root, text="Made by JDPRichards", borderwidth=2, width=85,bg="red").place(x=0,y=280)

ogfoldervar.set("select file to import from")
destfoldervar.set("select file to export to")


def findAll(pattern, path):
    file=[]
    for root,dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                file.append(os.path.join(root, name))
    return file

def find_single(pattern, path):
    result=""
    for root,dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result = os.path.join(root, name)
    return result
    
        
def upscale(target_folder, og_folder):
    print("Upscale")
    str_num=""
    all_files = findAll("*",og_folder)
    for file in all_files:
        print(target_folder)
        new_file =target_folder+"/"+file.split("\\")[1].replace(".csv","")+" upsample.csv"
        print(new_file)
        open(new_file,"w").write("")
        a = open(new_file, "a+")
        
        alldata=open(file, "r").read()
        split_lines = alldata.split("\n")

        headers = split_lines[0].replace('"','')
        splitheaders = headers.split(",")
        for i in range(0,len(splitheaders)+3,2):
            a.write(",file01")
        a.write("\n")
        a.write(",TIME,ANALOGTIME")
        for i in range(1,len(headers.split(",")),2):
            a.write(","+splitheaders[i])
        a.write("\n")
        a.write(",FRAME_NUMBERS,FRAME_NUMBERS")
        for i in range(1,len(headers.split(",")),2):
            a.write(",ANALOG")
        a.write("\n")
        for i in range(1,len(headers.split(","))+4,2):
            a.write(",ORIGINAL")
        a.write("\n")
        a.write("ITEM")
        for i in range(0,len(headers.split(","))+3,2):
            a.write(",0")
        a.write("\n")

        line_split_data = split_lines[2].split(",")
        lowest_intival= 100.0
        highest_intival =0.0
        highest_time=0.0
        latest_row =[]

        lastknownvalues=[]
        target_splitlinedata=[]

        for i in range(0, len(splitheaders)):
            lastknownvalues.append(0)
            latest_row.append(2)
        
        for i in range(0, len(alldata.split("\n"))):
            target_splitlinedata.append(0)

        for i in range(0, len(line_split_data)-2, 2):
            if (float(line_split_data[i]) < lowest_intival):
                lowest_intival = float(line_split_data[i])

        for i in range(0, len(line_split_data)-2, 2):
            if (float(line_split_data[i]) > highest_intival):
                highest_intival = float(line_split_data[i])
        
        for i in range(0, len(line_split_data)-2,2):
            for k in range(1, len(split_lines)-1):
                if split_lines[k].split(",")[i] !="":
                    if (float((split_lines[k]).split(",")[i])>float(highest_time)):
                        highest_time = float((split_lines[k]).split(",")[i])

        row=0
        timevalue =lowest_intival*float(row)
        print(len(split_lines))
        while (timevalue < highest_time):
            a.write(str(row+1)+","+str(timevalue)+","+str(timevalue))
            for i in range(1,len(splitheaders),2):
                if (split_lines[latest_row[i]-1].split(",")[i-1]!=""):
                    if float(split_lines[latest_row[i]-1].split(",")[i-1]) <= timevalue:
                        try:
                            if (lastknownvalues[i]!= split_lines[latest_row[i]-1].split(",")[i]):
                                lastknownvalues[i] = split_lines[latest_row[i]-1].split(",")[i]
                        except:
                            print(len(split_lines[latest_row[i]-1]))

                        if (latest_row[i] < len(split_lines)-1):
                            latest_row[i]=latest_row[i]+1
                a.write(","+str(lastknownvalues[i]))
            a.write("\n")
            row= row+1
            timevalue =lowest_intival*float(row)
        a.close()
        alldata =open(new_file,"r").read().replace(",","	")
        open(new_file,"w").write(alldata)

def upsample():
    upscale(target_folder, og_folder)

upsamplebttn = tk.Button(root, text = "Upsample", borderwidth = 2, command = upsample).place(x=50,y=250)
upsamplelbl = tk.Label(root, text="(Will take a while)",border =2).place(x=130,y=252)


root.mainloop()

print("Finished")
