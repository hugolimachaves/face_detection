# import the necessary packages
import cv2
import math

class EyeTracker:
	def __init__(self, faceCascadePath, eyeCascadePath):
		# load the face and eye detector
		self.faceCascade = cv2.CascadeClassifier(faceCascadePath)
		self.eyeCascade = cv2.CascadeClassifier(eyeCascadePath)

	def track(self, image):
		# detect faces in the image and initialize the list of
		# rectangles containing the faces and eyes
		faceRects = self.faceCascade.detectMultiScale(image,scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30),flags = cv2.CASCADE_SCALE_IMAGE)
		rects = []

		# loop over the face bounding boxes
		for (fX, fY, fW, fH) in faceRects:
			# extract the face ROI and update the list of
			# bounding boxes
			faceROI = image[fY:fY + fH, fX:fX + fW]
			rects.append((fX, fY, fX + fW, fY + fH))
			# detect eyes in the face ROI
			eyeRects = self.eyeCascade.detectMultiScale(faceROI,scaleFactor = 1.1, minNeighbors = 10, minSize = (20, 20),flags = cv2.CASCADE_SCALE_IMAGE)
			if len(eyeRects) == 2:
                                '''
				print('##################')
				print(eyeRects)
                                '''
                                
				eye_centroid = []
				dif_eye1x = eyeRects[0][2] - eyeRects[0][0]
				dif_eye1y = eyeRects[0][3] - eyeRects[0][1]
				dif_eye2x = eyeRects[1][2] - eyeRects[1][0]
				dif_eye2y = eyeRects[1][3] - eyeRects[1][1]
				cent_eye1x = eyeRects[0][0] + dif_eye1x/2
				cent_eye1y = eyeRects[0][1] + dif_eye1y/2
				cent_eye2x = eyeRects[1][0] + dif_eye2x/2
				cent_eye2y = eyeRects[1][1] + dif_eye2y/2
				eye_centroid.append([dif_eye1x , dif_eye1y])
				eye_centroid.append([dif_eye2x, dif_eye2y])

                                '''
				print('Centro do primeiro olho, coord. x:' + str(cent_eye1x) )
				print('Centro do primeiro olho, coord. y:' + str(cent_eye1y) )
				print('------------------' )
				print('Centro do segundo olho, coord. x:' + str(cent_eye2x) )
				print('Centro do segundo olho, coord. y:' + str(cent_eye2y) )
				'''
				coord_olho = []
				coord_olho.append([cent_eye1x , cent_eye1y])
				coord_olho.append([cent_eye2x , cent_eye2y])
				ca =  coord_olho[1][0] - coord_olho[0][0]
				co =  coord_olho[0][1] - coord_olho[1][1]
				inclinacao = math.degrees(math.atan(co/ca))
				'''
				print('A inclinação da cabeça é de ' + str(inclinacao) + ' graus')
				'''
			# loop over the eye bounding boxes
			for (eX, eY, eW, eH) in eyeRects:
				# update the list of boounding boxes
				rects.append((fX + eX, fY + eY, fX + eX + eW, fY + eY + eH))

		# return the rectangles representing bounding
		# boxes around the faces and eyes
		return rects

