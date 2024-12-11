import numpy as np

lace_array = [["k2tog", "ssp"], ["ssk", "p2tog"], ["yo", "yop"], ["k", "p"]]

cable_array = [["left", "right"], ["right", "left"], ["k", "p"], ["p", "k"]]

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
Make instructions assuming on a color pattern
"""    

def make_instructions_color(punch_card, stitches_per_row, row_number, x_position, y_position):
    number = 1
    row = 1
    previous = -1
    instructions = ""
    row_instructions = ""
    r_selvedge = ""
    l_selvedge = ""
    knit_or_purl = "k"
    
    if (check_valid(punch_card, stitches_per_row, row_number)):
        x_repeats = calc_repeats(int(stitches_per_row), len(punch_card))
        y_repeats = calc_repeats(int(row_number), len(punch_card[0]))
        x_xs_left, x_xs_right = excess_stitch(int(stitches_per_row), len(punch_card), x_position)
        y_xs_up, y_xs_down = excess_stitch(int(row_number), len(punch_card[0]), y_position)

        if (y_xs_down > 0):
            instructions += "Knit " + str(y_xs_down) + " rows stockinette \n \n"
        
        if (x_xs_right > 0):
            r_selvedge = " (selvedge: k" + "A" + str(x_xs_right) + ") "
        if (x_xs_left > 0):
            l_selvedge = " (selvedge: k"  + "A" + str(x_xs_left) + ") " 

        instructions += "Pattern Start: \n"
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
            if (x_repeats > 1):
                instructions += "Row " + str(row) + ": " + l_selvedge + "*" + row_instructions + "* " + str(x_repeats) + " times" + r_selvedge + "\n"
            else:
                instructions += "Row " + str(row) + ": " + l_selvedge + row_instructions + r_selvedge + "\n"        
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
        instructions = "The measurements given do not work. Please choose numbers greater or equal to the number of stitches in the chart"
    #print(instructions)
    return instructions

    
"""
Creates knitting instructions assuming a lace pattern
"""
def make_instructions_lace(punch_card, stitches_per_row, row_number, x_position, y_position):
    number = 1
    row = 1
    previous = -1
    instructions = ""
    row_instructions = ""
    r_selvedge = ""
    l_selvedge = ""
    
    if (check_valid(punch_card, stitches_per_row, row_number)):
        x_repeats = calc_repeats(int(stitches_per_row), len(punch_card))
        y_repeats = calc_repeats(int(row_number), len(punch_card[0]))
        x_xs_left, x_xs_right = excess_stitch(int(stitches_per_row), len(punch_card), x_position)
        y_xs_up, y_xs_down = excess_stitch(int(row_number), len(punch_card[0]), y_position)

        if (y_xs_down > 0):
            instructions += "Knit " + str(y_xs_down) + " rows stockinette \n \n"
        
        if (x_xs_right > 0):
            r_selvedge = " (selvedge: k" + str(x_xs_right) + ") "
        if (x_xs_left > 0):
            l_selvedge = " (selvedge: k" + str(x_xs_left) + ") " 

        instructions += "Pattern Start: \n"
        for i in punch_card:
            for j in i:
                current = j
                if (row % 2 == 0):
                    if (j == "k2tog"):
                        current = "ssp"
                    if (j == "ssk"):
                        current = "p2tog"
                    if (j== "yo"):
                        current = "yop"
                    if (j == "k"):
                        current = "p"
                if current == previous:
                    number += 1
                else:
                    if (previous != -1):
                        if (number != 1):
                            row_instructions += str(number) + previous + ", "
                            number = 1
                        else:
                            row_instructions += previous + ", "
                
                previous = current
            end_catch = current
            if(number != 1):
                row_instructions += str(number) + end_catch
            else:
                row_instructions += end_catch
            #x repeats
            if (x_repeats > 1):
                instructions += "Row " + str(row) + ": " + l_selvedge + "*" + row_instructions + "* " + str(x_repeats) + " times" + r_selvedge + "\n"
            else:
                instructions += "Row " + str(row) + ": " + l_selvedge + row_instructions + r_selvedge + "\n"        
            
            #row reset
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
Makes instructions for a cable chart
"""    

def make_instructions_cable(punch_card, stitches_per_row, row_number, x_position, y_position):
    number = 1
    row = 1
    previous = -1
    instructions = ""
    row_instructions = ""
    r_selvedge = ""
    l_selvedge = ""
    in_cable = False
    cable_count = 0
    
    if (check_valid(punch_card, stitches_per_row, row_number)):
        x_repeats = calc_repeats(int(stitches_per_row), len(punch_card))
        y_repeats = calc_repeats(int(row_number), len(punch_card[0]))
        x_xs_left, x_xs_right = excess_stitch(int(stitches_per_row), len(punch_card), x_position)
        y_xs_up, y_xs_down = excess_stitch(int(row_number), len(punch_card[0]), y_position)

        if (y_xs_down > 0):
            instructions += "Knit " + str(y_xs_down) + " rows stockinette \n \n"
        
        if (x_xs_right > 0):
            r_selvedge = " (selvedge: k" + str(x_xs_right) + ") "
        if (x_xs_left > 0):
            l_selvedge = " (selvedge: k" + str(x_xs_left) + ") " 

        instructions += "Pattern Start: \n"
        for i in punch_card:
            for j in i:
                current = j
                if (row % 2 == 0):
                    if (j == "left"):
                        current = "right"
                    if (j == "right"):
                        current = "left"
                    if (j== "k"):
                        current = "p"
                    if (j == "p"):
                        current = "k"
                if (previous == "right") or (previous == "left"):
                    if (in_cable):
                        print("check, cable false")
                        in_cable = False
                    else:
                        print("check, cable true")
                        in_cable = True
                if current == previous: #gathers all the like stitches together
                    number += 1
                else:
                    if (previous != -1): #previous = -1 is start of row
                        if (number != 1): #this is just to make it look pretty. you don't generally say 1k
                            if (in_cable):
                                cable_count +=1
                            else:
                                if(previous == "left"):
                                    print("left branch exists")
                                    row_instructions += str(cable_count)+"/"+str(cable_count)+ "LC" + ", "
                                    cable_count = 0
                                    number -=1
                                elif(previous == "right"):
                                    row_instructions += str(cable_count)+"/"+str(cable_count)+ "RC" + ", "
                                    cable_count = 0
                                    number -=1
                                else:
                                    row_instructions += str(number) + previous + ", "
                                    number = 1
                        else:
                            if (in_cable):
                                print("in_cable")
                                cable_count +=1
                            else:
                                row_instructions += previous + ","
                previous = current
            end_catch = current
            if(number != 1):
                row_instructions += str(number) + end_catch
            else:
                row_instructions += end_catch
            #x repeats
            if (x_repeats > 1):
                instructions += "Row " + str(row) + ": " + l_selvedge + "*" + row_instructions + "* " + str(x_repeats) + " times" + r_selvedge + "\n"
            else:
                instructions += "Row " + str(row) + ": " + l_selvedge + row_instructions + r_selvedge + "\n"        
            
            #row reset
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
    #print(instructions)
    return instructions
