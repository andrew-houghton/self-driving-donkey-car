import cv2
import matplotlib.pyplot as plt

def sliding_window(image, stepSize, windowSize):
	# slide a window across the image
	for y in xrange(0, image.shape[0], stepSize):
		for x in xrange(0, image.shape[1], stepSize):
			# yield the current window
			yield (x,y,image[y:y + windowSize[1], x:x + windowSize[0]])


img = cv2.imread('/Users/Travis/PycharmProjects/eigenface/sliding_windows_image/multiscale1.jpg', 0)  # read as a grayscale image
size = (112,92)

for w in sliding_window(img,10,size):
    plt.imshow(w[2])
    plt.show()

