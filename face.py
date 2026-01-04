from deepface import DeepFace
import cv2


def emo_score(image_path):
  objs = DeepFace.analyze(
    img_path = image_path, 
    actions = ['emotion'], enforce_detection=False)
  
  img = cv2.imread(image_path)
  height, width, channels = img.shape
  size = objs[0]['region']['w'] *objs[0]['region']['h']/(height*width)
  emotion = objs[-1]['dominant_emotion']

  if emotion == 'neutral':
      return 0, size
  else:
     return objs[0]['emotion'][emotion]/100, size


    







