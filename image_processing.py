import cv2
import numpy as np
# pip install pytesseract
import pytesseract
import nltk
import re
# pip install ics
from ics import Calendar, Event
# pip install pyspellchecker
from spellchecker import SpellChecker


# Resize based on the image size
def resize(img):
    height = img.shape[0]
    width = img.shape[1]
    print("The height is:", height)
    print("The width is:", width)

    prescription_text = pytesseract.image_to_string(img)
    if (height <= 1499) & (width <= 1999):
        img = cv2.resize(img, None, fx=2, fy=2)
    elif (height >= 1500) & (width >= 2000):
        img = cv2.resize(img, None, fx=0.25, fy=0.25)
    else:
        img = cv2.resize(img, None, fx=0.5, fy=0.5)
    return img


def correct_directive(directive):
    # The directives get checked and corrected using spellchecker distance ?
    # The strings get corrected to their closest words in the corpus
    # "TAGE 1 TAGLET" becomes "TAKE 1 TABLET"
    spell = SpellChecker()
    # Tokenize the directive
    token_directive = directive.split()
    # Spell Check and correct all the elements of the list
    checked_directive = [spell.correction(token) for token in token_directive]
    # Make the tokens uppercase
    upper_directive = [token.upper() for token in checked_directive]

    return upper_directive


def correct_duration(duration):
    # Regularize durations
    # Capitalize them to begin with
    # Turn "TWICE A DAY" or "TWICE DAILY" into "2 EVERYDAY"
    # Turn "ONCE A DAY" or "ONCE DAILY" into "1 EVERYDAY"
    # Turn  "EVERYDAY" or "EVERY DAY" into "1 EVERYDAY"
    # Turn "4 T0 6 HOURS" into "4-6 HOURS"
    # Tokenize the strings and put them into a list in this form:
    # "2 EVERYDAY" to ['2', 'EVERYDAY']

    # The durations get checked and corrected using spellchecker distance ?
    # The strings get corrected to their closest words in the corpus
    # "Ery 8 Hours" becomes "EVERY 8 HOURS and "
    spell = SpellChecker()
    # Tokenize the directive
    token_duration = duration.split()
    # Spell Check and correct all the elements of the list
    checked_duration = [spell.correction(token) for token in token_duration]
    # Make the tokens uppercase
    upper_duration = [token.upper() for token in checked_duration]


# def create_ics_file(duration, directive):
#     c = Calendar()
#     e = Event()
#     # Add Error Handling stuff
#     medication = input("What would you like to call this medicine: ")
#     quantity = int(input("How many pills are in the bottle: "))
#
#     # If the medication is to be taken daily
#     if duration.__contains__("EVERYDAY"):
#         # duration[0] should be the number of pills taken each time since duration = "# EVERYDAY"
#         # Use days_to_schedule to figure out how many events to add
#         # 30 pills @ TWICE A DAY = 15 dosages/15 events
#         days_to_schedule = quantity/int(duration[0])
#         # What time would you like to start taking the medication
#         print("Enter time 8AM as 8:00 and 8PM as 20:00 Exactly")
#         time_to_take = input("What time would you like to start taking the medication: ")
#
#         e.name = directive + " of " + medication
#         e.begin = '2020-06-26 00:00:00'  # This will be the current day as well as the medication taking time
#
#         while days_to_schedule > 1:
#             c.events.add(e)
#             # Figure out a way to add days to e.begin !!!
#             days_to_schedule -= 1
#     # If the medication is to be taken hourly
#
#     c.events
#     # [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
#     # End the event based off of how many pills are in the bottles. QTY
#     # Ask for the users input on this
#     with open('my.ics', 'w') as my_file:
#         my_file.writelines(c)
#     # and it's done !


def main():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Reading in the images to process
    img_one = cv2.imread("images/alamy.jpg")  # Nope lol
    img_two = cv2.imread("images/amoxicillin.jpeg")  # Good Further Processing Required
    img_three = cv2.imread("images/calvin.jpeg")  # Good
    img_four = cv2.imread("images/chris.jpg")  # Not Good (directive)
    img_five = cv2.imread("images/elvis.jpeg")  # Not Good (duration)
    img_six = cv2.imread("images/chris2.jpg")  # Good Further processing required
    img_five = cv2.imread("images/elvis.jpeg")  # Not Good (duration)
    img_eight = cv2.imread("images/jane.jpeg")  # Good Further Processing
    img_nine = cv2.imread("images/miley.png")  # Good
    img_ten = cv2.imread("images/opioid-bottle.jpg")  # Good Further Processing
    img_eleven = cv2.imread("images/warfarin.jpg")  # Good

    # Building the Image Processing Pipeline.
    # 1
    # Resize image_three to make it easier for OCR to analyze
    # This size depends on the size of the picture's text
    # If the image is larger than a certain size reduce its size else increase its size
    resized = resize(img_ten)

    #
    one_dimension = img_one.shape
    two_dimension = img_two.shape
    three_dimension = img_three.shape
    eight_dimension = img_eight.shape
    nine_dimension = img_nine.shape

    print(one_dimension)
    print(two_dimension)
    print(three_dimension)
    print(eight_dimension)
    print(nine_dimension)

    # 2
    # Convert the image to grayscale to remove any filtering
    greyscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # # 3
    # # Find some edges
    # edges = cv2.Canny(greyscale, 30, 200)
    # cv2.waitKey(0)
    # # Find the contours
    # _, contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.imshow("Canny edges after contouring", edges)
    # cv2.waitKey(0)
    # This is useful for reducing the noise from a background that is not homogeneous
    threshold = cv2.adaptiveThreshold(greyscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 20)

    # extract the text from the images
    text_one = pytesseract.image_to_string(threshold)
    # print the text
    print("The text from the image is: ", text_one)

    # Extract the directive from the prescription
    text = "Take many pills as Needed"
    # Add try catches
    try:
        directive_searcher = re.search(
            "([Tt]?[Aa][Kk][Ee]?|[Gg]?[Ii][Vv][Ee]?|[Aa]?[Dd][Mm][Ii][Nn][Ii][Ss][Tt][Ee][Rr]?)(.*)([Mm]?["
            "Oo][Uu]?[Tt]?[Hh]?|[Oo]?[Rr]?[Aa][Ll][Ll][Yy]?|[Tt]?[Aa][Bb][Ll][Ee][Tt][Ss]?)", text_one)
        directive = directive_searcher.group(0)
        print("This is the directive:", directive)
    except AttributeError:
        print("Couldn't Find the Directive")

    try:
        duration_searcher = re.search(
            "([Ee]?[Vv]?[Ee][Rr][Yy]|[Oo][Nn]?[Cc][Ee]|[Tt][Ww]?[Ii]?[Cc]?[Ee]|[Tt][Hh]?[Rr]?[Ii]?[Cc]?["
            "Ee]|[Dd][Aa]?[Ii]?[Ll]?[Yy]|\d\s)(.*)([Dd][Aa]?[Ii]?[Ll]?[Yy]|[Hh]?[Oo][Uu][Rr][Ss]?|"
            "[Dd][Aa][Yy][Ss]?|[Ww][Ee][Ee][Kk][Ss]|[Mm][Oo][Rr][Nn][Ii][Nn][Gg][Ss]?|[Aa][Ff][Tt][Ee][Rr]"
            "[Nn][Oo][Oo][Nn][Ss]?|[Nn][Ii][Gg][Hh][Tt][Ss]?)", text_one)
        duration = duration_searcher.group(0)
        print("This is the duration: ", duration)
    except AttributeError:
        print("Couldn't Find the Duration")

    # Use NLTK To complete the Directives and their Durations
    # Convert Directives and Logic into events on an ics file.

    # cv2.imshow("IMG2", resized)
    # cv2.imshow("IMG1", threshold)
    # Keep the image open
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
