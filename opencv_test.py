import cv2
from imutils import contours
import os
import numpy as np

#winner so far
"""
lace work matrix. The first column is the image to match, the second is the right side stitch, the third is the wrong side,
fourth is the lean (r= right, l = left, n = neutral), fifth is stitches gained or loss
"""

lace_matrix = np.array([["images\knit-symbol-P-on-RS.png", "p", "k", "n", "0"], ["images\knit-symbol-Yarn-over.png", "yo", "yop", "n", "1"], ["images\knit-symbol-SSK-on-RS.png", "ssk", "p2tog", "l", "-1"], ["images\knit-symbol-K2tog-on-RS.png", "k2tog", "ssp", "r", "-1"], ["images\knit-symbol-SSP-on-RS.png", "ssp", "k2tog", "l", "-1"], ], dtype= "object")
"""
cable matrix. The first column is the image to match, the second is the right side stitch, third is wrong side
"""

cable_matrix = np.array([[]], dtype = "object")

def convert(image_path, stitches_per_row, row_number, x_position, y_position):
    stitch_matrix, thresh, gray = process_chart(image_path)
    chart_type = determine_chart(image_path)
    if (chart_type == 0):
        punch_card = color_punch(stitch_matrix, thresh, gray)
        return make_instructions_color(punch_card, stitches_per_row, row_number, x_position, y_position)
    elif (chart_type == 1):
        punch_card = lace_punch(stitch_matrix, thresh, gray)
        return make_instructions_lace(punch_card, stitches_per_row, row_number, x_position, y_positon)
    elif (chart_type == 2):
        punch_card = cable_punch(stitch_matrix, thresh, gray)
        return make_instructions_cable(punch_card, stitches_per_row, row_number, x_position, y_positon)
    else:
        return "error"

def test(text):
    print(text)

"""
function to process the chart. Takes an image chart, returns a sorted matrix and manipulated images (gray, big image, thresh)
"""
def process_chart(image_path):
    
    # Read the image
    image = cv2.imread(image_path)
    big_image= cv2.resize(image, None, fx = 3.0, fy = 3.0, interpolation = cv2.INTER_LINEAR)
    
    #image processing
    gray = cv2.cvtColor(big_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 100, 200, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(thresh, 100, 255, None, 3)

    #find the contours
    knit_contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    #find contours finds the contours outside and inside the box, basically doubling the amount of boxes
    #only the internal boxes count. These remove the outside ones. 

    hierarchy = hierarchy[0]
    inner_contours = []
    for component in zip(knit_contours, hierarchy):
        currentContour = component[0]
        currentHierarchy = component[1]
        x, y, w, h = cv2.boundingRect(currentContour)
        if w*h > 300:
            if w*h < 7000:
                if currentHierarchy[1] < 0: 
                    inner_contours.append(currentContour)
                    cv2.rectangle(big_image,(x,y),(x+w,y+h),(0,0,255),1)
    inner_contours.pop(0)

    #initial bottom to top sorting of contours
    (inner_contours, _) = contours.sort_contours(inner_contours, method="bottom-to-top")

    #determining the length of row
    stitches_per_row = count_row_stitches(inner_contours)
    stitches_per_row = 10

    #sorting the stitches inside each row from right to left
    stitches = []
    row = []
    for (i, c) in enumerate(inner_contours, 1):
        row.append(c)
        if i % stitches_per_row == 0:  
            (inner_contours, _) = contours.sort_contours(row, method="right-to-left")
            stitches.append(inner_contours)
            row = []
    #print_stitch(stitches, big_image)
    #cv2.imshow("Labeled Grid", big_image)
    return stitches, thresh, gray

"""
determines if the chart is a color, lace or cable chart. returns an integer for type. 0 is color, 1 is lace, 2 is cable
"""

def determine_chart(image_path):
    image = cv2.imread(image_path)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("images\yotemplate.PNG", 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    #for pt in zip(*loc[::-1]):
        #cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    type = -1
    uniques = np.unique(image.reshape(-1, image.shape[-1]), axis=0)
    #ironically color charts have the fewest amount of colors because text display anti aliasing display nice
    if len(uniques) < 20:
        type = 0
        return type
    elif len(loc) > 4:
        type = 1
        return type
    else:
        type = 2
        return type 

"""
creates the stitch matrix assuming a color punch card
"""
def color_punch(stitches, thresh, gray):
    #creating the color matrix
    punch_card = []
    punch_card_row = []
    for row in stitches:
        for c in row:
            x, y, w, h = cv2.boundingRect(c)
            mask = np.zeros(thresh.shape[:2], dtype="uint8")
            cv2.rectangle(mask, (x,y), (x+w, y+h), 255, -1)
            masked = cv2.bitwise_or(gray, thresh, mask=mask)
            total = np.sum(masked == 255)
            if total > 0:
                punch_card_row.append(0)
            else:
                punch_card_row.append(1)
        punch_card.append(punch_card_row)
        punch_card_row = []
    return punch_card

"""
creates stitch matric assuming a lace punch card
"""

def lace_punch(stitches, image, gray):
    #creating the color matrix
    punch_card = []
    punch_card_row = []
    k2tog = cv2.imread("images/template-k2tog.PNG", 0)
    ssk = cv2.imread("images/template-ssk.PNG", 0)
    yo = cv2.imread("images/template-yo.PNG", 0)
    for row in stitches:
        for c in row:
            x, y, w, h = cv2.boundingRect(c)
            mask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(mask, (x,y), (x+w, y+h), 255, -1)
            masked = cv2.bitwise_and(gray, gray, mask=mask)
            res_k2tog = cv2.matchTemplate(masked, k2tog, cv2.TM_CCOEFF_NORMED)
            threshold = 0.90
            k2tog_loc = np.where(res_k2tog >= threshold)
            print("k2tog: ")
            print(len(k2tog_loc))
            res_ssk = cv2.matchTemplate(masked, ssk, cv2.TM_CCOEFF_NORMED)
            threshold = 0.90
            ssk_loc = np.where(res_ssk >= threshold)
            print("ssk: ")
            print(len(ssk_loc))
            res_yo = cv2.matchTemplate(masked, yo, cv2.TM_CCOEFF_NORMED)
            threshold = 0.90
            yo_loc = np.where(res_yo >= threshold)
            print("yo: ")
            print(len(yo_loc))
            if len(yo_loc) > 4:
                punch_card_row.append('yo')
            elif len(ssk_loc) > 4:
                punch_card_row.append('ssk')
            elif len(k2tog_loc) > 5:
                punch_card_row.append('k2tog')
            else:
                punch_card_row.append('k')
        punch_card.append(punch_card_row)
        punch_card_row = []
    print(punch_card)
    return punch_card

"""
creates stitch matric assuming a cable punch card
"""

def cable_punch(stitches, thresh, gray):
    #creating the color matrix
    punch_card = []
    punch_card_row = []
    k2tog = cv2.imread("images/template-k2tog.PNG", 0)
    ssk = cv2.imread("images/template-ssk.PNG", 0)
    yo = cv2.imread("images/template-yo.PNG", 0)
    for row in stitches:
        for c in row:
            x, y, w, h = cv2.boundingRect(c)
            mask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(mask, (x,y), (x+w, y+h), 255, -1)
            masked = cv2.bitwise_and(gray, gray, mask=mask)
            res_k2tog = cv2.matchTemplate(masked, k2tog, cv2.TM_CCOEFF_NORMED)
            threshold = 0.90
            k2tog_loc = np.where(res_k2tog >= threshold)
            print("k2tog: ")
            print(len(k2tog_loc))
            res_ssk = cv2.matchTemplate(masked, ssk, cv2.TM_CCOEFF_NORMED)
            threshold = 0.90
            ssk_loc = np.where(res_ssk >= threshold)
            print("ssk: ")
            print(len(ssk_loc))
            res_yo = cv2.matchTemplate(masked, yo, cv2.TM_CCOEFF_NORMED)
            threshold = 0.90
            yo_loc = np.where(res_yo >= threshold)
            print("yo: ")
            print(len(yo_loc))
            if len(yo_loc) > 4:
                punch_card_row.append('yo')
            elif len(ssk_loc) > 4:
                punch_card_row.append('ssk')
            elif len(k2tog_loc) > 5:
                punch_card_row.append('k2tog')
            else:
                punch_card_row.append('k')
        punch_card.append(punch_card_row)
        punch_card_row = []
    return punch_card

"""
creates an image with the chart with numbers for  debugging purposes
"""

def print_stitch(stitches, big_image):         
    #print stitch numbers
    number = 0
    for row in stitches:
        for c in row:
            x,y,w,h = cv2.boundingRect(c)
            cv2.putText(big_image, "#{}".format(number + 1), (x,y + h- 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            number += 1

"""
Determines the number of stitches per row
maybe buggy
"""

def count_row_stitches(knit_contours):
    rownum = 1
    ycoor = []
    for (i,c) in enumerate(knit_contours, 1):
        x, y, w, h = cv2.boundingRect(c)
        ycoor.append(y)
    for a in range(len(ycoor)):
        if (ycoor[a] == ycoor[a+1]):
            break
        elif (ycoor[a]-ycoor[a+1] > 5):
            break
        else:
            rownum +=1
    return rownum

"""
checks if the numbers are valid
"""

def check_valid(punch_card, stitches_per_row, row_number):
    pattern_rows_count = len(punch_card)
    pattern_stitches_per_row = len(punch_card[0])
    spr = int(stitches_per_row)
    nor = int(row_number)
    if (nor == spr == -1):
        return True
    elif (nor == -1) and (spr > pattern_rows_count -1):
        return True
    elif (spr == -1) and (nor > stitches_per_row -1):
        return True
    elif (nor < pattern_rows_count):
        return False
    elif (spr < pattern_stitches_per_row):
        return False
    else:
        return True

"""
calculates the repeat stitches
"""

def calc_repeats(stitches, row):
    if (stitches != -1):
        repeats = stitches//row
    else:
        repeats = 1
    return repeats

"""
checks if there are excess stitches or is needed
"""

def is_excess(stitches, rows):
    if (stitches % rows == 0):
        return False
    else:
        if (stitches == -1):
            return False
        else:
            return True

"""
calculates the excess stitches
"""
def xs_stitches(stitches, rows, position):
    xs = stitches % rows
    xs_left = 0
    xs_right = 0
    if (position == "left") or (position == "up"):
        xs_left = xs
    elif (position == "right") or (position == "down"):
        xs_right = xs
    elif (position == "center"):
        xs_left = xs//2
        xs_right = xs-xs_left
    else:
        xs_left = 0
        xs_right = 0
    
    return xs_left, xs_right

"""
all excess calcs in one
"""

def excess_stitch(stitches, rows, position):
    if (is_excess(stitches, rows)):
        return xs_stitches(stitches, rows, position)
    else:
        return 0, 0
    
"""
Creates knitting instructions assuming a colorwork pattern
"""
def make_instructions_color(punch_card, stitches_per_row, row_number, x_position, y_position):
    number = 1
    row = 1
    previous = -1
    instructions = ""
    row_instructions = ""
    knit_or_purl = "k"
    
    if (check_valid(punch_card, stitches_per_row, row_number)):
        x_repeats = calc_repeats(int(stitches_per_row), len(punch_card))
        y_repeats = calc_repeats(int(row_number), len(punch_card[0]))
        x_xs_left, x_xs_right = excess_stitch(int(stitches_per_row), len(punch_card), x_position)
        y_xs_up, y_xs_down = excess_stitch(int(row_number), len(punch_card[0]), y_position)

        if (y_xs_down > 0):
            instructions += "Knit " + str(y_xs_down) + " rows stockinette \n \n"

        instructions += "Pattern Start: \n"
        for i in punch_card:
            if (x_xs_left > 0):
                row_instructions += "(selvedge: k"  + "A" + str(x_xs_left) + ") "  
            for j in i:
                if j == previous:
                    number += 1
                else:
                    if j == 0:
                        if (previous != -1):
                            row_instructions += knit_or_purl + "B" + str(number) + ", "
                            number = 1
                        previous = j
                    elif j == 1: 
                        if (previous != -1):
                            row_instructions += knit_or_purl + "A" + str(number) + ", "
                            number = 1
                        previous = j
            end_catch = "A" if previous%2 == 0 else "B"
            row_instructions += knit_or_purl + end_catch + str(number)
            if (x_xs_right > 0):
                row_instructions += " (selvedge: k" + "A" + str(x_xs_right) + ")"  
            if (x_repeats > 1):
                instructions += "Row " + str(row) + ": *" + row_instructions + "* " + str(x_repeats) +" times" + "\n"
            else:
                instructions += "Row " + str(row) + ": " + row_instructions + "\n"
            knit_or_purl = "k" if row%2 == 0 else "p"
            previous = -1
            number = 1
            row_instructions = ""
            row +=1
        if(y_repeats > 1):
            instructions += "\nRepeat pattern for " + str(y_repeats) + " number of times \n"
        if (y_xs_up > 0):
            instructions += "\nKnit " + str(y_xs_up) + " rows in stockinette"
    else:
        instructions = "The measurements given do not work."
    return instructions

"""
Make instructions assuming on a lace pattern
"""    

def make_instructions_lace(punch_card, stitches_per_row, row_number):
    #used to monitor odd or even
    number = 1
    row = 1
    previous = -1
    instructions = ""
    row_instructions = ""
    knit_or_purl = "k"
    for i in punch_card:
        for j in i:
            if j == previous:
                number += 1
            else:
                if j == 0:
                    if (previous != -1):
                        row_instructions += knit_or_purl + "B" + str(number) + ", "
                        number = 1
                    previous = j
                elif j == 1: 
                    if (previous != -1):
                        row_instructions += knit_or_purl + "A" + str(number) + ", "
                        number = 1
                    previous = j
        end_catch = "A" if previous%2 == 0 else "B"
        row_instructions += knit_or_purl + end_catch + str(number)
        instructions += "Row " + str(row) + ": " + row_instructions + "\n"
        knit_or_purl = "k" if row%2 == 0 else "p"
        previous = -1
        number = 1
        row_instructions = ""
        row +=1
    print(instructions)
    return instructions

"""
Makes instructions for a cable chart
"""    

def make_instructions_cable(punch_card, stitches_per_row, row_number):
    number = 1
    row = 1
    previous = -1
    instructions = ""
    row_instructions = ""
    knit_or_purl = "k"
    for i in punch_card:
        for j in i:
            if j == previous:
                number += 1
            else:
                if j == 0:
                    if (previous != -1):
                        row_instructions += knit_or_purl + "B" + str(number) + ", "
                        number = 1
                    previous = j
                elif j == 1: 
                    if (previous != -1):
                        row_instructions += knit_or_purl + "A" + str(number) + ", "
                        number = 1
                    previous = j
        end_catch = "A" if previous%2 == 0 else "B"
        row_instructions += knit_or_purl + end_catch + str(number)
        instructions += "Row " + str(row) + ": " + row_instructions + "\n"
        knit_or_purl = "k" if row%2 == 0 else "p"
        previous = -1
        number = 1
        row_instructions = ""
        row +=1
    print(instructions)
    return instructions

# Example usage
#image, punch_card = process_chart("C:/Users/Alabaster/Pictures/knit_chart_color_small.png")
#stitch_matrix, thresh, gray = process_chart("C:/Users/Alabaster/Pictures/knit_chart_cable.png")
#punch_card = lace_punch(stitch_matrix, thresh, gray)
#make_instructions_lace(punch_card)
#determine_chart("C:/Users/Alabaster/Pictures/knit_chart_lace.png")
#cv2.imshow("Labeled Grid", image)
#cv2.waitKey(0)
#make_instructions(punch_card)
#cv2.destroyAllWindows()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
