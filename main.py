from PIL import Image
import os

def writePalette(palette):
    file.write("const uint16_t PALETTE [] PROGMEM={\n")
    for color in palette:
        # print(color)
        file.write("\t"+hex(calculateHex(color))+",\n")
    file.write("};\n")

def writeImgData(palette,imgData, imgDataName):
    file.write("const byte "+imgDataName+" [] PROGMEM={\n")
    for i in range(len(imgData)):
        if (i!=(len(imageData)-1) or i==0):
            file.write("\t"+"0x0"+str(palette.index(imgData[i]))+",")
            if((i+1)%16==0):
                file.write("\n")
        else:
            file.write("\t"+"0x0"+str(palette.index(imgData[i]))+"\n")
            file.write("};\n")



def calculateHex(palleteColor):
    output=0
    if (palleteColor[3]==0):
        return 0x0000
    else:
        output+=int(0xF800*palleteColor[0]/255)
        output+=int(0x07E0*palleteColor[1]/255)
        output+=int(0x001F*palleteColor[2]/255)
        return output
def calculateHexV2(palleteColor):
    output=0
    if (palleteColor[3]==0):
        return 0x0000
    else:
        output+=int(0xF8*palleteColor[0]/255)<<8
        output+=int(0x7E*palleteColor[1]/255)<<4
        output+=int(0x1F*palleteColor[2]/255)
        return output
# Useful resource: https://rgbcolorpicker.com/565
def convertTo16bit(color):
    output=0
    if (color[3]==0):
        return 0x0000
    else:
        red=int(round(color[0]*31/255))
        green=int(round(color[1]*63/255))
        blue=int(round(color[2]*31/255))
        return (red<<11) | (green << 5) | blue
def processImgData(imgData):
    output=[]
    for i in imgData:
        output.append(convertTo16bit(i))
    return output

def writeImgDataD(processedImgData,imgDataName):
    file.write("const uint16_t "+imgDataName+" [] PROGMEM={\n")
    length = len(processedImgData)
    print(f"ImgData size: {length}")

    for i in range(length):
        if (i!=(length-1) or i==0):
            file.write("\t"+hex(processedImageData[i])+",")
            if((i+1)%16==0):
                file.write("\n")
        else:
            file.write("\t"+hex(processedImageData[i])+"\n")
            file.write("};\n")
# This still has some artifacts but is ok for now, there is a single loose pixel towards the end per row
def makeMask(processedImgData, sizeX):
    output=[]
    byte=0x0
    count=0
    total_count=0
    for i in processedImgData:
        if(i!=0):
            byte+=2**(7-count)
        count+=1
        total_count+=1
        if count!=8 and total_count%sizeX==0:
            while count!=7:
                # byte+=2**(7-count)
                count+=1
        if count == 8:
            output.append(byte)
            count=0
            byte=0x0
    return output
def writeMask(mask,imgDataName):
    file.write("const uint8_t "+imgDataName+"_MASK [] PROGMEM={\n")
    length= len(mask)
    print(f"Mask size: {length}")
    for i in range(length):
        if (i!=(length-1) or i==0):
            file.write("\t"+hex(mask[i])+",")
            if((i+1)%16==0):
                file.write("\n")
        else:
            file.write("\t"+hex(mask[i])+"\n")
            file.write("};\n")
def writeImgSizes(imageData):
    for i in imageData:
        file.write("const uint8_t "+i["name"]+"_X ="+str(i["x"])+";\n")
        file.write("const uint8_t "+i["name"]+"_Y ="+str(i["y"])+";\n")


def writeHelperArray(names):
    file.write(f"const int RGB_map_allArray_LEN={len(names)};\n")
    file.write(f"const int RGB_map_allArray[{len(names)}]="+"{\n")
    for i in range(len(names)):
        if (i!=len(names)-1 or i==0):
            file.write("\t"+names[i]+",\n")
        else:
            file.write("\t"+names[i])
            file.write("};\n")
Img_Dir = "./Imgs"
if (os.path.exists(Img_Dir)):
    file = open("output.txt","w")
    imgDatas=[]
    for i in os.listdir(Img_Dir):
        if(i.split(".")[1]!="png"):
            continue
        imgDataName=i.replace("-","_").replace("(","").replace(")","").split(".")[0]
        
        img=Image.open(Img_Dir+"/"+i)
        print(img)
        imageData=list(img.getdata())
        print(set(img.getdata()))
        processedImageData = processImgData(imageData)
        for i in set(processedImageData):
            print((hex(i)))
        mask = makeMask(processedImageData,img.width)
        writeMask(mask,imgDataName)
        writeImgDataD(processedImageData,imgDataName)
        imgDatas.append({"name":imgDataName,"x":img.width,"y":img.height})
    writeImgSizes(imgDatas)
    #     for color in set(imageData):
    #         imgDatas["PALETTE"].add(color)

    #     imgDatas[imgDataName]=imageData
    # imgDatas["PALETTE"]=list(imgDatas["PALETTE"])
    # writePalette(imgDatas["PALETTE"])
    # for i in imgDatas.keys():
    #     if(i=="PALETTE"):
    #         continue
    #     writeImgData(imgDatas["PALETTE"],imgDatas[i],i)
    # writeHelperArray(list(imgDatas.keys()))

    file.close()

