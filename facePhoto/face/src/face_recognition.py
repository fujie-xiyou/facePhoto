import tensorflow as tf
import facenet
import cv2
import numpy as np
from scipy import misc

from align import detect_face


def get_dist(emb1, emb2):
    return np.sqrt(np.sum(np.square(np.subtract(emb1[0, :], emb2[0, :]))))


class FacenetEmbedding:
    def __init__(self, model_path):
        self.sess = tf.InteractiveSession()
        self.sess.run(tf.global_variables_initializer())
        self.image_size = 160
        self.margin = 44
        # Load the model
        facenet.load_model(model_path)
        # Get input and output tensors
        self.images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        self.tf_embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        self.phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

    def get_embedding(self, img, bounding_boxes):
        det = np.squeeze(bounding_boxes[0, 0:4])
        img_size = np.asarray(img.shape)[0:2]
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0] - self.margin / 2, 0)
        bb[1] = np.maximum(det[1] - self.margin / 2, 0)
        bb[2] = np.minimum(det[2] + self.margin / 2, img_size[1])
        bb[3] = np.minimum(det[3] + self.margin / 2, img_size[0])
        cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
        aligned = misc.imresize(cropped, (self.image_size, self.image_size), interp='bilinear')
        prewhitened = facenet.prewhiten(aligned)
        images = np.stack([prewhitened])
        feed_dict = {self.images_placeholder: images, self.phase_train_placeholder: False}

        emb = self.sess.run(self.tf_embeddings, feed_dict=feed_dict)
        return emb

    def free(self):
        self.sess.close()


class FaceDetection:
    def __init__(self):
        self.minsize = 20  # minimum size of face
        self.threshold = [0.6, 0.7, 0.7]  # three steps's threshold
        self.factor = 0.709  # scale factor
        print('Creating networks and loading parameters')
        with tf.Graph().as_default():
            # gpu_memory_fraction = 1.0
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                self.pnet, self.rnet, self.onet = detect_face.create_mtcnn(sess, None)

    def detect_face(self, image_path):
        image = misc.imread(image_path, mode='RGB')

        bboxes, landmarks = detect_face.detect_face(image, self.minsize, self.pnet, self.rnet, self.onet,
                                                    self.threshold, self.factor)
        return image, bboxes, landmarks

    def get_square_bboxes(self, bboxes, landmarks, fixed="height"):
        '''
        获得等宽或者等高的bboxes
        :param bboxes:
        :param landmarks:
        :param fixed: width or height
        :return:
        '''
        new_bboxes = []
        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            w = x2 - x1
            h = y2 - y1
            center_x, center_y = (int((x1 + x2) / 2), int((y1 + y2) / 2))
            if fixed == "height":
                dd = h / 2
            elif fixed == 'width':
                dd = w / 2
            x11 = int(center_x - dd)
            y11 = int(center_y - dd)
            x22 = int(center_x + dd)
            y22 = int(center_y + dd)
            new_bbox = (x11, y11, x22, y22)
            new_bboxes.append(new_bbox)
        return new_bboxes, landmarks
