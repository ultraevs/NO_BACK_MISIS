from ultralytics import YOLO
from detecton import detect
import random

print('1')
mo = YOLO('segmentation.pt')
print('2')
print(detect(mo, random(1, 2)))