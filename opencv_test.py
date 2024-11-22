import cv2
from imutils import contours
import os
import numpy as np

#winner so far

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
        if currentHierarchy[2] < 0:
            inner_contours.append(currentContour)
            cv2.rectangle(big_image,(x,y),(x+w,y+h),(0,0,255),1)

    #initial bottom to top sorting of contours
    (inner_contours, _) = contours.sort_contours(inner_contours, method="bottom-to-top")

    #determining the length of row
    stitches_per_row = count_row_stitches(inner_contours)

    #sorting the stitches inside each row from right to left
    stitches = []
    row = []
    for (i, c) in enumerate(inner_contours, 1):
        row.append(c)
        if i % stitches_per_row == 0:  
            (inner_contours, _) = contours.sort_contours(row, method="right-to-left")
            stitches.append(inner_contours)
            row = []

    #creating the color matrix
    punch_card = []
    punch_card_row = []
    for row in stitches:
        for c in row:
            isGrey = None
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
         
    #print stitch numbers
    number = 0
    for row in stitches:
        for c in row:
            x,y,w,h = cv2.boundingRect(c)
            cv2.putText(big_image, "#{}".format(number + 1), (x,y + h- 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
            number += 1


    return big_image, punch_card

"""
Determines the number of stitches per row
"""

def count_row_stitches(knit_contours):
    rownum = 1
    ycoor = []
    for (i,c) in enumerate(knit_contours, 1):
        x, y, w, h = cv2.boundingRect(c)
        ycoor.append(y)
    for a in range(len(ycoor)):
        if (ycoor[a]-ycoor[a+1] > 5):
            break
        else:
            rownum +=1
    return rownum

def make_instructions(punch_card):
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

# Example usage
image, punch_card = process_chart("C:/Users/Alabaster/Pictures/knit_chart_color_small.png")
cv2.imshow("Labeled Grid", image)
cv2.waitKey(0)
make_instructions(punch_card)
cv2.destroyAllWindows()
