from mtcnn import MTCNN
import cv2
import matplotlib.pyplot as plt

# Đọc ảnh đầu vào
image_path = "c:/code/GrProj/Demo/data/image.jpg"
img = cv2.imread(image_path)
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Tạo bộ phát hiện MTCNN
detector = MTCNN()

# Phát hiện khuôn mặt
faces = detector.detect_faces(rgb_img)

# Vẽ hình chữ nhật quanh khuôn mặt
for face in faces:
    x, y, w, h = face['box']
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Hiển thị ảnh
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Hide axes
plt.show()
