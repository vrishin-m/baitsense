from ultralytics import YOLO
if __name__ == '__main__':
    model = YOLO('yolo11n.pt') 
    results = model.train(
        data=r"arrows\dataset.yaml", 
        epochs=40, 
        imgsz=640, 
        batch=16, 
        name='udhay')
    