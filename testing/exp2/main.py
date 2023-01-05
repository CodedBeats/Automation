import cv2 as cv
import numpy as np

# wrap all this code in a function
def findImageMatches(baseImagePath, isolatedImagePath, thresholdVal, mode, rectColor = (0, 0, 255)):

    # define imgs as variables 
    baseImage = cv.imread(baseImagePath, cv.IMREAD_UNCHANGED)
    isolatedImage = cv.imread(isolatedImagePath, cv.IMREAD_UNCHANGED)
    baseImage.astype(np.float32)
    baseImage.astype(np.uint8)
    isolatedImage.astype(np.float32)
    isolatedImage.astype(np.uint8)
    # save dimenshions of Pea Shooter img
    isolatedImageW = isolatedImage.shape[1]
    isolatedImageH = isolatedImage.shape[0]

    # set a threshold for matching accuracy
    threshold = thresholdVal

    # match isolatedImage against baseImage with 1 of the following methods
    # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(baseImage, isolatedImage, method)
    
    # Get all positions from the match result that exceed the threshold
    locations = np.where(result >= threshold)
    # refine the locations array to just return x and y coordinates of each matched location
    locations = list(zip(*locations[::-1]))

    # create list of rectangles [x, y, w, h] (so they can be grouped together) 
    rectangles = []
    for l in locations:
        rect = [int(l[0]), int(l[1]), isolatedImageW, isolatedImageH]
        # Add every box to the list twice in order to retain single (non-overlapping) boxes
        rectangles.append(rect)
        rectangles.append(rect)

    # group rectangles that are close to each other where 3rd parameter controls how close together they must be to be grouped
    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

    points = []
    if len(rectangles):
        # set rect properties
        lineColor = rectColor # (B,G,R)
        lineThickness = 2
        lineType = cv.LINE_8
        markerColor = (0, 255, 255) # (B,G,R)
        markerType = cv.MARKER_CROSS
        markerSize = 30
        markerThickness = 2

        # loop over each location
        for (x, y, w, h) in rectangles:

            if mode == "rectangles":
                # determine rect pos
                topLeft = (x, y)
                bottomRight = (x + w, y + h)
                # draw the box
                cv.rectangle(baseImage, topLeft, bottomRight, lineColor, lineThickness, lineType)

            elif mode == "points":
                # get center of rect
                centerX = x + int(w/2)
                centerY = y + int(h/2)
                # save points
                points.append((centerX, centerY))
                # draw the center point
                cv.drawMarker(baseImage, (centerX, centerY), markerColor, markerType, markerSize, markerThickness)

        if mode:
            # display baseImage with matched data
            cv.imshow("Matched Image", baseImage)
            cv.waitKey()
            # save the image
            # cv.imwrite('result_click_point.jpg', haystack_img)


    else:
        print("Didn't find any matches")



# points = findImageMatches("./imgRef/PvZ.png", "./imgRef/peaShooter.png", thresholdVal = 0.7, mode = "points")
points = findImageMatches("./imgRef/xx.png", "./imgRef/yy.png", thresholdVal = 0.3, mode = "rectangles", rectColor = (0, 255, 0))