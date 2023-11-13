from detection import parking_info
from ultralytics import YOLO


# импортировать конкретно эту модель
model = YOLO('segmentation.pt')

answer = parking_info(model, 1)

print(answer)

# answer = {
#     'status': 'exported', 
#     'data': {
#         0: 'occupied', 
#         1: 'occupied', 
#         2: 'occupied', 
#         3: 'occupied', 
#         4: 'occupied', 
#         5: 'occupied', 
#         6: 'occupied', 
#         7: 'occupied', 
#         8: 'occupied', 
#         9: 'occupied'
#         }
#     }