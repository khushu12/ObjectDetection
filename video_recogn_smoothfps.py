import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image



# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

# if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
#   raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')
# This is needed to display the images.
# %matplotlib inline
from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
	file_name = os.path.basename(file.name)
	if 'frozen_inference_graph.pb' in file_name:
		tar_file.extract(file, os.getcwd())

detection_graph = tf.Graph()
with detection_graph.as_default():
	od_graph_def = tf.GraphDef()
	with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
import cv2
cap=cv2.VideoCapture(0)


# # Size, in inches, of the output images.
# IMAGE_SIZE = (25, 25)
 
with detection_graph.as_default():
	with tf.Session(graph=detection_graph) as sess:
		while True:
			ret, image_np=cap.read()
			image_np_expanded = np.expand_dims(image_np, axis=0)
			# output_dict = run_inference_for_single_image(image_np, detection_graph)
			image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
			boxes = tf.get_default_graph().get_tensor_by_name('detection_boxes:0')
			scores= tf.get_default_graph().get_tensor_by_name('detection_scores:0')
			classes= tf.get_default_graph().get_tensor_by_name('detection_classes:0')
			num_detections= tf.get_default_graph().get_tensor_by_name('num_detections:0')
			(boxes,scores,classes,num_detections)=sess.run(
				[boxes,scores,classes,num_detections],
				feed_dict={image_tensor:image_np_expanded})
			vis_util.visualize_boxes_and_labels_on_image_array(
				image_np,
				np.squeeze(boxes),
				np.squeeze(classes).astype(np.int32),
				np.squeeze(scores),
				# output_dict['detection_boxes'],
				# output_dict['detection_classes'],
				# output_dict['detection_scores'],
				category_index,
				# instance_masks=output_dict.get('detection_masks'),
				use_normalized_coordinates=True,
				line_thickness=8)

			cv2.imshow('object_detection', cv2.resize(image_np,(800,800)))
			if cv2.waitKey(25) & 0xFF== ord('q'):
				cv2.destroyAllWindows()
				break

#   ops = tf.get_default_graph().get_operations()
#   all_tensor_names = {output.name for op in ops for output in op.outputs}
#   tensor_dict = {}
#   for key in [
#       'num_detections', 'detection_boxes', 'detection_scores',
#       'detection_classes', 'detection_masks'
#   ]:
#     tensor_name = key + ':0'
#     if tensor_name in all_tensor_names:
#       tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
#           tensor_name)
#   if 'detection_masks' in tensor_dict:
    
#     detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
#     real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
#     detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
#     detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
#     detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
#         detection_masks, detection_boxes, image.shape[0], image.shape[1])
#     detection_masks_reframed = tf.cast(
#         tf.greater(detection_masks_reframed, 0.5), tf.uint8)
#     tensor_dict['detection_masks'] = tf.expand_dims(
#         detection_masks_reframed, 0)

#   output_dict = sess.run(tensor_dict,
#                          feed_dict={image_tensor: np.expand_dims(image, 0)})

#   output_dict['num_detections'] = int(output_dict['num_detections'][0])
#   output_dict['detection_classes'] = output_dict[
#       'detection_classes'][0].astype(np.uint8)
#   output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
#   output_dict['detection_scores'] = output_dict['detection_scores'][0]
#   if 'detection_masks' in output_dict:
#     output_dict['detection_masks'] = output_dict['detection_masks'][0]
#   return output_dict



# # for image_path in TEST_IMAGE_PATHS:
# # 	newimage=image_path.split('/')
# # 	print (image_path)
# # 	image = Image.open(image_path)
# # 	print (image)
# # 	# the array based representation of the image will be used later in order to prepare the
# # 	# result image with boxes and labels on it.
# # 	image_np = load_image_into_numpy_array(image)
# 	# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
# 	image_np_expanded = np.expand_dims(image_np, axis=0)
# 	# Actual detection.
# 	output_dict = run_inference_for_single_image(image_np, detection_graph)
# 	# Visualization of the results of a detection.

	# plt.figure(figsize=IMAGE_SIZE)
	# print (image_np)
	# plt.imshow(image_np)
	# plt.savefig(newimage[1],bbox_inches='tight')


