import cv2
import numpy as np
image = cv2.imread("vv.png")

print(image.shape)

image[100,200] = [0, 0, 255]  # Change the pixel at (100, 200) to red

cv2.imshow("Modified Image", image)
image = cv2.resize(image, (640, 480))  # Resize the image to 640x480
cv2.waitKey(0)

fW = 640
fH = 480

cap = cv2.VideoCapture(0)  # Capture video from the default camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, fW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, fH)

while True:
    ret, frame = cap.read()  # Read a frame from the camera
    if not ret:
        break

    cv2.imshow("Camera Feed", frame)  # Display the camera feed

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key press
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all OpenCV windows

'''Crop
face = image[200:500,300:600]
Meaning
Rows:200 → 500
Columns:300 → 600 '''

small = cv2.resize(image,(640,480)) #(width,height)

small = cv2.resize(
    image,
    None,
    fx=0.5,
    fy=0.5
) # 50 percent of original size

flip = cv2.flip(image,1) #1- horizontal, 0- vertical, -1- both

rotated = cv2.rotate(
    image,
    cv2.ROTATE_90_CLOCKWISE
)
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)  # convert to gray scale
import numpy as np
kernel = np.ones((5,5),np.uint8) # 5x5 kernel of ones for dilation
blur = cv2.GaussianBlur(image, (5, 5), 0)  # Apply Gaussian blur with a 5x5 kernel
canny = cv2.Canny(image, 100, 200)  # Apply Canny edge detection with thresholds 100 and 200
dialate = cv2.dilate(canny , kernel , iterations = 1) # Dilate the edges detected by Canny using the kernel
erode = cv2.erode(dialate , kernel , iterations = 1) # Erode the dilated image using the kernel
''' Why Convert to Grayscale?

Many algorithms only need brightness.
Example:Face detection,Edge detection,OCR
They become
Faster,Simpler,Less memory'''

rgb = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2RGB
)
# HSV 
# Hue :Which color?
# Saturation:How colorful?
# Value :How bright?
hsv = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2HSV
)

'''HSV is extremely useful for:

Color tracking
Object detection
Robotics
Self-driving cars'''

# Split Channels
b, g, r = cv2.split(image)  # Split the image into its blue, green, and red channels
# Notice Each image looks grayscale. Why? Each channel stores intensity only
#Merging Channels
merged = cv2.merge([b, g, r])  # Merge the blue, green, and red channels back into a single image

bright = cv2.convertScaleAbs(
    image,
    alpha=1,
    beta=50
) # Increase brightness by adding 50 to each pixel value

contrast = cv2.convertScaleAbs(
    image,
    alpha=2,
    beta=0
) # Increase contrast by multiplying each pixel value by 2

# Alpha and Beta Alpha = Contrast  Beta = Brightness

canvas = np.zeros((500, 700, 3), dtype=np.uint8) # black canvas
canvas = np.ones((500,700,3), dtype=np.uint8) * 255 # white canvas

# Drawing a line - image, start_point, end_point, color, thickness
cv2.line(canvas, (0, 0), (500, 500), (255, 0, 0), 5)

# Drawing shapes
# 1. Rectangle - image, start_point, end_point, color, thickness
cv2.rectangle(canvas, (50, 50), (200, 200), (0, 255, 0), 3)
# 2. Circle - image, center_coordinates, radius, color, thickness
cv2.circle(canvas, (300, 300), 50, (0, 0, 255), -1)  # Filled circle (-1 thickness means filled)
# 3. Ellipse - image, center_coordinates, axes_lengths, angle, start_angle, end_angle, color, thickness
cv2.ellipse(canvas, (400, 400), (100, 50), 0, 0, 180, (255, 255, 0), 2)

# CROPING AND RESIZING IMAGES
resized_image = cv2.resize(image, (640, 480)) # Resize the image to 640(width)x480(height) pixels
cropped_image = image[100:400, 200:500] # Crop the image from row 100 to 400 and column 200 to 500
img_resized = cv2.resize(cropped_image, (image.shape[1],image.shape[0])) # Resize the cropped image

# Stacking image
hor = np.hstack((image, resized_image)) # Horizontal stacking of original and resized images
ver = np.vstack((image, resized_image)) # Vertical stacking of original and resized images
cv2.imshow("Horizontal Stack", hor) # Display the horizontally stacked images
cv2.imshow("Vertical Stack", ver) # Display the vertically stacked images

cv2.waitKey(0) # Wait for a key press to close the windows
cv2.destroyAllWindows() # Close all OpenCV windows

# stacking function
def stackImage(scale, images):
    width = images[0][0].shape[1]
    height = images[0][0].shape[0]
    ver = None
    for img in images:
        hor = None
        for i in img:
            if i.shape[:2] == images[0][0].shape[:2]:
                i = cv2.resize(i, (0, 0), None, scale, scale)
            else:
                i = cv2.resize(i, (width, height), None, scale, scale)

            if len(i.shape) == 2:
                i = cv2.cvtColor(i, cv2.COLOR_GRAY2BGR)

            if hor is not None:
                hor = np.hstack((hor, i))
            else:
                hor = i
        if ver is not None:
            ver = np.vstack((ver, hor))
        else:
            ver = hor
    return ver

# text
"""cv2.putText(
    image,
    text,
    position,
    font,
    scale,
    color,
    thickness
)"""
cv2.putText(
    canvas,
    "Hello OpenCV",
    (50,450),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255,255,255),
    2
)

#wrap view / bird view 
#681,625 
#1. 50,298
#2. 252,595
#3. 622,393
#4. 406,53
w , h = 250,350
xx = np.float32([[100,225],[300,520],[122,450],[300,450]])
pts = np.float32([[0,0],[w,0],[0,h],[w,h]])

matrix = cv2.getPerspectiveTransform(xx,pts)
image_warp = cv2.warpPerspective(image,matrix,(w,h))

for x in range(0,4):
    cv2.circle(image, (int(xx[x][0]), int(xx[x][1])), 5, (0, 0, 255), -1)

cv2.imshow("Canvas with Points", image)
cv2.imshow("Warped Image", image_warp)
cv2.waitKey(0)
cv2.destroyAllWindows()

#color detection
def empty(a):
    pass

cv2.namedWindow("TrackBars") # make a window for trackbars
cv2.resizeWindow("TrackBars", 640, 240) 
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, lambda x: None) # Create a trackbar for minimum hue value with intial value 0 and maximum value 179 with a function that does nothing when the trackbar value changes just run
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, lambda x: None)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, lambda x: None) 
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, lambda x: None)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, lambda x: None)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, lambda x: None)


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

while True:
     h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
     h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
     s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
     s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
     v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
     v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

     lower = np.array([h_min, s_min, v_min])
     upper = np.array([h_max, s_max, v_max])

     mask = cv2.inRange(hsv, lower, upper)
     imgresult = cv2.bitwise_and(image, image, mask=mask)



     cv2.imshow("Original Image", image)
     cv2.imshow("HSV Image", hsv)
     cv2.imshow("Mask", mask)
     cv2.imshow("Result", imgresult)
     cv2.waitKey(0)
     break

#translation - moving image by pixels
def translate(image, x, y):
    transMat = np.float32([[1, 0, x], [0, 1, y]]) # Create a translation matrix
    dimensions = (image.shape[1], image.shape[0]) # Get the dimensions of the image
    return cv2.warpAffine(image, transMat, dimensions) # Apply the translation to the image

#Scaling changes size.
def scale(image, scale_factor):
    width = int(image.shape[1] * scale_factor) # Calculate the new width
    height = int(image.shape[0] * scale_factor) # Calculate the new height
    dimensions = (width, height) # Create a tuple of the new dimensions
    return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA) # Resize the image using INTER_AREA interpolation

#This estimation of pixel values is called interpolation. 
# 1. nearest-neighbor interpolation: The simplest method, which assigns the value of the nearest pixel to the new pixel. This can result in a blocky appearance.
# 2. bilinear interpolation: Considers the closest 2x2 neighborhood of known pixel values to estimate the value of the new pixel.
# 3. bicubic interpolation: Considers the closest 4x4 neighborhood of known pixel values, resulting in smoother images than bilinear interpolation.
# 4. Lanczos interpolation: Uses a larger neighborhood of pixels and a sinc function to achieve high-quality results, especially for downscaling.
# 5. INTER_AREA: This method is generally used for downscaling and is based on pixel area relation. It may give moire’-free results. It is the preferred method for image decimation, as it gives better results than the other methods.
# 6. INTER_CUBIC: This method uses bicubic interpolation over 4x4 pixel neighborhood and is slower but produces better results than INTER_LINEAR.
large = cv2.resize(
    image,
    (1000,1000),
    interpolation=cv2.INTER_CUBIC
)

# rotation
h, w = image.shape[:2]

center = (w//2, h//2)

matrix = cv2.getRotationMatrix2D(
    center,
    45,
    1
)

rotated = cv2.warpAffine(
    image,
    matrix,
    (w,h)
)

# Affine Transformation
# An affine transformation is a linear mapping method that preserves points, straight lines, and planes. Sets of parallel lines remain parallel after an affine transformation. It can be represented using a 2x3 matrix and can perform operations like rotation, translation, scaling, and shearing.
# To perform an affine transformation, you need to specify three points in the source image and their corresponding points in the destination image. The transformation matrix is then calculated based on these points.
pts1 = np.float32([
    [50,50],
    [200,50],
    [50,200]
])

pts2 = np.float32([
    [10,100],
    [200,50],
    [100,250]
])

M = cv2.getAffineTransform(
    pts1,
    pts2
)

output = cv2.warpAffine( # warpAffine applies the affine transformation to the image using the transformation matrix M and the specified output size (w, h)
    image,
    M,
    (w,h)
)

# Perspective Transformation
# A perspective transformation is a more general transformation that can represent the change in perspective of an image. It can be represented using a 3x3 matrix and can perform operations like rotation, translation, scaling, shearing, and perspective distortion.

matrix = cv2.getPerspectiveTransform(
    pts1, # four points in the source image
    pts2
)

# countour
imageContour = image.copy() # Create a copy of the original image to draw contours on 
def getContours(image):
    countour , heierarchy = cv2.findContours(image , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in countour:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 500:
            cv2.drawContours(imageContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True) 
            print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            objCor = len(approx)
            x , y , w , h = cv2.boundingRect(approx) # boundary 

            if objCor == 3: objectType = "Tri"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05: objectType = "Square"
                else: objectType = "Rectangle"
            elif objCor > 4: objectType = "Circle"
            else: objectType = "None"

            cv2.rectangle(imageContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imageContour,objectType,
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,
                        0.7,(0,0,0),2)

# face detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") # Load the Haar Cascade classifier for face detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert the image to grayscale for better detection
faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Detect faces in the grayscale image using the detectMultiScale method with a scale factor of 1.1 and a minimum of 4 neighbors
for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)


# mouse click
circles = np.zeros((4, 2), int)
counter = 0

# Define the mouse callback function
def mousePointer(event, x, y, flags, param):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        circles[counter] = x, y
        counter += 1
        print(circles)

# Read the image
img = cv2.imread("image/me.jpg")
width, height = 250, 350

# Check if the image is loaded successfully
if img is None:
    print("nothing as a image")
else:
    cv2.imshow("original img", img)
    cv2.setMouseCallback("original img", mousePointer)

    while True:
        for x in range(0, 4):
            cv2.circle(img, (int(circles[x][0]), int(circles[x][1])), 5, (0, 0, 255), cv2.FILLED)

        if counter == 4:
            pts1 = np.float32(circles)
            pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgOutput = cv2.warpPerspective(img, matrix, (width, height))
            cv2.imshow("imgOutput", imgOutput)

        cv2.imshow("original img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

