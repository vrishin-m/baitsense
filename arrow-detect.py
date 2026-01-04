from ultralytics import YOLO
if __name__ == '__main__':
    model = YOLO('yolo11n.pt') 
    results = model.train(
        data=r"arrows\dataset.yaml", 
        epochs=20, 
        imgsz=160, 
        batch=16, 
        name='arrow-detector')
    