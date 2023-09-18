from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import time
def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image

def plot_face_blendshapes_bar_graph(face_blendshapes):
  
  # Extract the face blendshapes category names and scores.
  face_blendshapes_names = [face_blendshapes_category.category_name for face_blendshapes_category in face_blendshapes]
  face_blendshapes_scores = [face_blendshapes_category.score for face_blendshapes_category in face_blendshapes]
  # The blendshapes are ordered in decreasing score value.
  face_blendshapes_ranks = range(len(face_blendshapes_names))

  fig, ax = plt.subplots(figsize=(12, 12))
  bar = ax.barh(face_blendshapes_ranks, face_blendshapes_scores, label=[str(x) for x in face_blendshapes_ranks])
  ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
  ax.invert_yaxis()

  # Label each bar with values
  for score, patch in zip(face_blendshapes_scores, bar.patches):
    plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

  ax.set_xlabel('Score')
  ax.set_title("Face Blendshapes")
  plt.tight_layout()
  plt.show()


import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode



options = FaceLandmarkerOptions(
  base_options = BaseOptions(model_asset_path="modelos/face_landmarker.task"),
  running_mode = VisionRunningMode.VIDEO,
  output_face_blendshapes=True,
  num_faces=1
)

cap = cv2.VideoCapture("sources/video3.mp4")
fps = cv2.CAP_PROP_FPS
timeNow = 0
with FaceLandmarker.create_from_options(options) as landmarker:

  while(1):
    ret, imagen = cap.read()

    if not ret:
      break
    else:
      
      imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
      imagen = cv2.resize(imagen, (0,0), fx=0.4, fy=0.4)
      cv2.imshow("imagen1", imagen)

      if (cv2.waitKey(1) == 27):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imagen)
        timeNow
        face_landmarker_result = landmarker.detect_for_video(mp_image, timeNow)
        timeNow += 1000//fps
      
        annotated_image = draw_landmarks_on_image(imagen, face_landmarker_result)
      
        
        cv2.imshow("imagen2", annotated_image)
        break
      
      #plot_face_blendshapes_bar_graph(face_landmarker_result.face_blendshapes[0])




cap.release()
cv2.destroyAllWindows()


for element in face_landmarker_result.face_blendshapes[0]:
  print(element.index, element.category_name, element.score)

caracteristicas = face_landmarker_result.face_blendshapes[0]

nombreCaracteristicas = [caracteristica.category_name for caracteristica in caracteristicas]
calificacionCaracteristicas = [calificacion.score for calificacion in caracteristicas] 

rangos = range(len(nombreCaracteristicas))

fig, ax = plt.subplots(figsize=(12,12))
bar = ax.barh(rangos, calificacionCaracteristicas, label = [str(x) for x in rangos])
ax.set_yticks(rangos, nombreCaracteristicas)
ax.invert_yaxis()

#etiquetar cada barra
for score, patch in zip(calificacionCaracteristicas, bar.patches):
  plt.text(patch.get_x() +  patch.get_width(), patch.get_y(), f"{score: .4f}", va = "top")

ax.set_label("Calificacion")
ax.set_title("Caracteristicas Rostro")
plt.tight_layout()
plt.show()
