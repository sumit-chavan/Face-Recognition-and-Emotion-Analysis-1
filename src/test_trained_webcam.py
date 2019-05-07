import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import cv2
#from webapp import db,Actor

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}



def predict(X_img, knn_clf=None, model_path=None, distance_threshold=0.6):
    # if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
    #     raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    # X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]




def faceRec(vid_path):
    video_capture = cv2.VideoCapture(0)
    length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_no=0
    print(vid_path)
    print("Number of total frames are: {}".format(length))
    while frame_no < 20:
        ret, frame = video_capture.read()
        if not ret:
            break
        rgb_frame = frame[:, :, ::-1]
        predictions=predict(rgb_frame,model_path="face_reco_models/trained_knn_model.clf")
        for name, (top, right, bottom, left) in predictions:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_no+=1
        print("Writing frame {} / {}".format(frame_no, length))
        # print(predictions)
        # print(predictions[0][0])
        
        if predictions:
            print(predictions[0][1][0])
            print(predictions[0][1][1])
            print(predictions[0][1][2])
            print(predictions[0][1][3])
            # actor=Actor(actorname=predictions[0][0],frameno=frame_no,image_file="default.jpg",x=predictions[0][1][0],y=predictions[0][1][1],z=predictions[0][1][2],w=predictions[0][1][3])
            # db.session.add(actor)
            # db.session.commit()

    # print(Actor.query.all())
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
# destination="/home/yash/Desktop/face_recognition-master/examples/short_hamilton_clip.mp4"
destination="videoplayback.mp4"
faceRec(destination)
