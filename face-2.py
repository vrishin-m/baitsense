import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

from deepface import DeepFace
objs = DeepFace.analyze(
  img_path = r"C:\Users\mahad\Pictures\Screenshots\Screenshot 2025-11-30 210303.png", 
  actions = ['emotion'])

size = objs[0]['region']['w'] *objs[0]['region']['h']
emotion = objs[-1]['dominant_emotion']
if emotion == 'neutral':
    emo_score =0
else:
    emo_score =1


