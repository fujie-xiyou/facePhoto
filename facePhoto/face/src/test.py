import face_recognition

model_path = '~/Downloads/20180402-114759'  # 模型文件路径
image_path = '/Users/fujie/Downloads/IMG_20190505_185934.jpg'
image_path2 = '/Users/fujie/Downloads/雷军/images3.jpeg'


def face_recognition_image(image_path):
    # 加载数据库的数据
    # 初始化mtcnn人脸检测
    face_detect = face_recognition.FaceDetection()
    facenet_embedding = face_recognition.FacenetEmbedding(model_path)

    image1 = face_detect.detect_face(image_path)
    image2 = face_detect.detect_face(image_path2)
    emb1 = facenet_embedding.get_embedding(image1[0], image1[1])
    emb2 = facenet_embedding.get_embedding(image2[0], image2[1])
    dist = face_recognition.get_dist(emb1, emb2)
    print("dist = {}".format(dist))


if __name__ == '__main__':
    face_recognition_image(image_path)
