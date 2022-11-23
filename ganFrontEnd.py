# GAN Front End

import os
from datetime import datetime
import random
import re

# —————————————————————————————————————————————————————————————————————————————————————————————
# OPTIONS

# Enter a custom prompt here. "customPrompt" needs to be set to "True"
prompt = "Prompt goes here"

# Add an optional secondary prompt here. 
#TODO: add prompt code

# Use Wikiart as model if true. False defaults to imagenet16384.
wikiArt = True

# Size of final output in pixels. 
sizeWidth = 512
SizeHeight = 512

# Number of iterations. Values between 100 and 300 give best results. 
interation = 200

# Upscales the image by 4X using machine learning when True
upscaleOn = False

# —————————————————————————————————————————————————————————————————————————————————————————————
# FUNCTIONS 

# returns the current date and time in format (YYYY.MM.DD.HH.MM)
def getDate():
    today = datetime.now()
    dateIs = today.strftime("%Y%m%d-%H%M-")
    return dateIs

# scales up the image
# from https://github.com/xinntao/Real-ESRGAN.git
def upscale(filename, text):
    filenameUp = "output/4x/" + filename + "_4x.png"
    filename += ".png"
    # for the biary version of the upscaler
    command = "./realesrgan-ncnn-vulkan -i " + "output/" + filename + " -o " + filenameUp
    
    # for the python version of the upscaler
    #location = "../output/4x/"
    #command = "cd Real-ESRGAN && python inference_realesrgan.py -i " + "../output/" + filename + " -o " + location + " --suffix " + "'" + "4x" + "'"
    
    print("Now upscaling the image. \n")
    os.system(command)
    print("\nFinished upscaling the image. \n")
    return text, filenameUp

# calls the GAN generate script from generate.py using the top headline grabbed from grabHeadline()
# GAN from https://github.com/nerdyrodent/VQGAN-CLIP
def paint():

    # Checks if option for Wikiart model is set.
    if wikiArt == True:
        modelCKPT = "checkpoints/wikiart_16384.ckpt"
        modelCONF = "checkpoints/wikiart_16384.yaml"

    else:
        modelCKPT = "checkpoints/vqgan_imagenet_f16_16384.ckpt"
        modelCONF = "checkpoints/vqgan_imagenet_f16_16384.yaml"

    headline = prompt
    print("\nThe prompt is:", headline, "\n")

    # creates a filename for the output. Limits the name to 250 chars max. Strips chars that might be illegal for filenames. 
    fileraw = getDate() + headline.rstrip('.')
    filename = re.sub('[^A-Za-z0-9]+', '-', fileraw)
    if len(filename) > 250:
        filename = filename[0 : 250]

    # Create a command to pass all the options and prompt to the GAN image generator
    safeHeadline = headline.replace('"', "")
    safeHeadline = safeHeadline.replace("'", "")
    command = "python3 generate.py" + " -p " + "'" + safeHeadline.rstrip('.') + "'" + " -i " + "'" + str(interation) + "'" + " -s " + str(sizeWidth) + " " + str(SizeHeight) + " -o " + "'output/" + filename + ".png" "'" + " -conf " + "'" + modelCONF + "'" + " -ckpt " + "'" + modelCKPT + "'"

    #TODO: add vivid color random option

    # Calls the generate command via shell. Waits for return before proceeding. 
    print("\nGenerating the image now. \n")
    os.system(command)
    print("The GAN finished the image. \n")

    return filename, headline


# —————————————————————————————————————————————————————————————————————————————————————————————
# FUNCTION CALLS

if upscaleOn == False:
    # Paint generates the image and returns the image filename and original headline.
    # Upscale and tweetNow both take two arguments. The "*" lets the functions pull the tuple return from paint().
    paint()
else:
    # Just sends an upscaled image to the output/4x folder.
    upscale(*paint())
    
# —————————————————————————————————————————————————————————————————————————————————————————————s