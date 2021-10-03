''' Importing Libraries '''

# for image clicking purposes
from imutils.video import VideoStream, FPS

# to run multiprocesses at the same time
from multiprocessing import Process, process
from multiprocessing import Queue

# for machine learning model purposes
import numpy as np
import argparse
import imutils
import time
import cv2




'''
classify function is responsible for our multiprocessing
3 Params :-
# 1. neuralNetwork object is for machine learning model
# 2. inputQ is a queue for frames for object detection
# 3. outputQ is a queue of detection which will be processes further in main thred
'''

def classify (neuralNetworkObject, inputQ, outputQ):
	
    # looping until true
	while True:

		# if there is already any frames in our inputQ
		if not inputQ.empty():

			# grab the frame from the input queue, 
			frame = inputQ.get()

            # resize it, and .....
			frame = cv2.resize(frame, (300, 300))

            # construct a blob from it
			blob = cv2.dnn.blobFromImage(frame, 0.007843,(300, 300), 127.5)

			# set the blob as input to our deep learning object detector and....
			neuralNetworkObject.setInput(blob)

            # obtain the detections
			detections = neuralNetworkObject.forward()
			
            # write the detections to the output queue
			outputQ.put(detections)



''' Function that will get called by main pyhton file '''

def person_detection():

    ''' Parsing Command line arguments '''

    # construct the argument parse and ...
    argParse = argparse.ArgumentParser()
    argParse.add_argument("-p", "--prototxt", required = True, help = "path to Caffe 'deploy' prototxt file")
    argParse.add_argument("-m", "--model", required = True, help = "path to Caffe pre-trained model")
    argParse.add_argument("-c", "--confidence", type = float, default = 0.2, help = "to filter weak detections, the min probability")

    # parse the arguments
    args = vars(argParse.parse_args())



    ''' Initializing some Variables '''

    # initialize the list of class labels MobileNet SSD was trained to detect
    #(taking some extra labels for better model building purpose)
    CLASSES = ["background", "bird", "boat", "bottle", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "person"]


    # then generate a set of bounding box colors for each class
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))



    ''' Loading Serializable Models '''

    print("[INFO] loading model...")

    # loading model with arguments defined above
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])


    # initialize the frames (input queue), detections (output queue),and .....
    inputQ = Queue(maxsize=1)    
    outputQ = Queue(maxsize=1)

    # note:- Both of these queues trivially have a size of one as our neural
    # network will only be applying object detections to one frame at a time.

    # the list of actual detections returned by the child process
    detections = None


    ''' Starting the child process '''

    # construct a child process indepedent from our main process

    print("[INFO] starting process...")
    process = Process(target=classify, args=(net, inputQ, outputQ,))
    process.daemon = True
    process.start()


    ''' Predicting the detections'''

    print("[INFO] starting video stream...")

    # initialize the video stream
    vs = VideoStream(usePiCamera=True).start()

    # waiting for camera to settle
    time.sleep(2.0)

    # initialize the FPS counter
    fps = FPS().start()

    # looping over frames using video stream
    while True:

        # get the frame from the threaded video stream,
        frame = vs.read()

        # resize it, and
        frame = imutils.resize(frame, width=400)

        # get its dimensions
        (fH, fW) = frame.shape[:2]

        ''' working on queues '''

        # if the input queue is empty, give the current frame to classify
        if inputQ.empty():
            inputQ.put(frame)

        # if the output queue is not empty, grab the detections
        if not outputQ.empty():
            detections = outputQ.get()

        # check to see if our detectios are not None (and if so, we'll draw the detections on the frame)
        if detections is not None:

            # loop over the detections
            for i in np.arange(0, detections.shape[2]):

            # extract the confidence (i.e., probability) associated with the prediction
                conf = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence`
                # is greater than the minimum confidence
                if conf < args["confidence"]:
                    continue

                # otherwise, extract the index of the class label from the detections
                index = int(detections[0, 0, i, 1])
                dimensions = np.array([fW, fH, fW, fH])
                box = detections[0, 0, i, 3:7] * dimensions

                # then compute the (x, y)-coordinates of the bounding box for the object
                (startX, startY, endX, endY) = box.astype("int")

                ''' Draw the prediction on the frame '''

                # on x-axis 
                label = "{}: {:.2f}%".format(CLASSES[index], conf * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[index], 2)

                # on y-axis
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[index], 2)

            # display the output frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            
            # if the quit key (q) was pressed, break from the loop
            if key == ord("q"):
                break

            # checking if there is a person before camera
            if(CLASSES[index]=='person'):
                return 1
            
            # else return 0
            else:
                return 0
        
            # update the FPS counter
            fps.update()


    ''' Stopping the machine '''

    # Stop the timer and display FPS information 
    fps.stop()

    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()


