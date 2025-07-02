import cv2
import os

def capture_face_image(filename='face.jpg', save_dir='images'):
    """
    打开摄像头拍摄面部照片并保存到本地

    参数：
    - filename: 保存的文件名
    - save_dir: 保存目录（默认 images 文件夹）

    返回：
    - 图片的完整保存路径
    """
    # 创建保存目录（如果不存在）
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("无法打开摄像头")

    print("按空格键拍照，按 Q 退出")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法读取摄像头内容")
            break

        cv2.imshow('Camera - 按空格拍照', frame)

        key = cv2.waitKey(1)
        if key == ord(' '):  # 空格键
            cv2.imwrite(filepath, frame)
            print(f"已保存图像到 {filepath}")
            break
        elif key == ord('q') or key == ord('Q'):
            print("已取消拍照")
            break

    cap.release()
    cv2.destroyAllWindows()
    return filepath
