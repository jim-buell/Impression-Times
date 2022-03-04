#!/opt/miniconda3/envs/GAN/bin/python3

# Impressions of the Times generator

import feedparser
import os
from datetime import datetime
import random
from torch import absolute, rand
import re
import paintTweet
import platform

# —————————————————————————————————————————————————————————————————————————————————————————————
# OPTIONS

# Enter a custom prompt here. "customPrompt" needs to be set to "True"
prompt = "Prompt goes here"
customPrompt = False

# Use Wikiart as model if true. False defaults to imagenet16384.
wikiArt = True

# Size of final output in pixels. This output is square. If forceSize is false, a random size (within limits) will be automatically determined.
size = 400
forceSize = False

# Number of iterations. Values between 100 and 300 give best results. 
interation = 200

# Toggles tweeting on and off
tweetOn = True

# —————————————————————————————————————————————————————————————————————————————————————————————
# FUNCTIONS 

# Returns the top headline from the RSS feed defined below
def grabHeadline():

    finalHeadline = ""
    headlineLimit = 0
    rssNames = ["https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"]
    
    for item in rssNames:
        rssSources='{}'.format(item)
        rssHeadlines = feedparser.parse(rssSources)
        Headlines = rssHeadlines['entries']
        for entries in Headlines:
            if headlineLimit < 1:
                if "news" in (entries['title']).lower():
                    finalHeadline = f"{entries['title']}."
                    headlineLimit += 1
                else:
                    finalHeadline = f"{entries['title']}."
                    headlineLimit += 1
    return finalHeadline

# returns the current date and time in format (YYYY.MM.DD.HH.MM)
def getDate():
    today = datetime.now()
    dateIs = today.strftime("%Y%m%d-%H%M-")
    return dateIs

def dateWords():
    today = datetime.now()
    dateWords = today.strftime("%B %-d, %Y")
    return dateWords
#TODO: should time be tweeted in EST?

# returns a string of two random numbers to be passed as width and hight to generate.py
def paintSize():
    if forceSize == True:
        paintSize = str(size) + " " + str(size)
    else:
        width = 5 * (round(random.randrange(255, 500)/5))
        height = 5 * (round(random.randrange(255, 500)/5))
        # if the numbers are kinda close, then just make it a square
        if abs(width - height) < 50:
            width = 400
            height = 400
        paintSize = str(width) + " " + str(height)
    return paintSize 

# scales up the image
# from https://github.com/xinntao/Real-ESRGAN.git
def upscale(filename, text):
    # checks which Mac OS version. If 11.0 or higher, uses the binary version of the upscaler. 
    # Otherwise calls the slower python script.
    v, _, _ = platform.mac_ver()
    v = float('.'.join(v.split('.')[:2]))
    filenameUp = "output/4x/" + filename + "_4x.png"
    filename += ".png"
    if v >= 10.16:
        print("This is Mac OS", v, "— using the binary upscaler.")
        command = "./realesrgan-ncnn-vulkan -i " + "output/" + filename + " -o " + filenameUp
    if v < 10.16:
        print("This is Mac OS", v, "— using the Python upscaler.")
        location = "../output/4x/"
        command = "cd Real-ESRGAN && python inference_realesrgan.py -i " + "../output/" + filename + " -o " + location + " --suffix " + "'" + "4x" + "'"
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

    # Checks if option for custom prompt is set. Else grabs headline. 
    if customPrompt == True:
        headline = prompt
    else:
        headline = grabHeadline()
    print("\nThe prompt is:", headline, "\n")

    # creates a filename for the output. Limits the name to 250 chars max. Strips chars that might be illegal for filenames. 
    fileraw = getDate() + headline.rstrip('.')
    filename = re.sub('[^A-Za-z0-9]+', '-', fileraw)
    if len(filename) > 250:
        filename = filename[0 : 250]

    # Create a command to pass all the options and prompt to the GAN image generator
    safeHeadline = headline.replace('"', "")
    safeHeadline = safeHeadline.replace("'", "")
    if customPrompt == True:
        command = "python3 generate.py" + " -p " + "'" + safeHeadline.rstrip('.') + "'" + " -i " + "'" + str(interation) + "'" + " -s " + paintSize() + " -o " + "'output/" + filename + ".png" "'" + " -conf " + "'" + modelCONF + "'" + " -ckpt " + "'" + modelCKPT + "'"
    else:
        command = "python3 generate.py" + " -p " + "'" + "minimalist painting of " + safeHeadline.rstrip('.') + "'" + " -i " + "'" + str(interation) + "'" + " -s " + paintSize() + " -o " + "'output/" + filename + ".png" "'" + " -conf " + "'" + modelCONF + "'" + " -ckpt " + "'" + modelCKPT + "'"

    #TODO: add vivid color random option

    # Calls the generate command via shell. Waits for return before proceeding. 
    print("\nGenerating the image now. \n")
    os.system(command)
    print("The GAN finished the image. \n")

    return filename, headline

def tweetNow(tweet, image):
    tweetText = tweet.replace("'s", "’s")
    tweetText = "“" + tweetText + "”" + "\n\n" + dateWords()
    paintTweet.tweet(tweetText.rstrip('.'), image)

# —————————————————————————————————————————————————————————————————————————————————————————————
# FUNCTION CALLS

if tweetOn == True:
    # Paint generates the image and returns the image filename and original headline.
    # Upscale and tweetNow both take two arguments. The "*" lets the functions pull the tuple return from paint().
    tweetNow(*upscale(*paint()))
else:
    # Just sends an upscaled image to the output/4x folder.
    upscale(*paint())
    
# —————————————————————————————————————————————————————————————————————————————————————————————s