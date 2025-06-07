import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import glob
from time import time


def get_data():
    data = []
    imgs = []
    for file in glob.glob('<PATHTOIMAGES>/img_*.jpg'):
        img = cv2.imread(file)
        img_244 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_224 = cv2.resize(img_244, (224, 224))[np.newaxis, :, :, :]

        img_224 = (np.float32(img_224) - 0.0) / 255.0
        data.append(img_224)
        imgs.append(img)

    return data, imgs


def main():
    model_path = '<PATHTOMODEL>/hand_landmark_lite.tflite'
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    print('INPUT\n', input_details)
    print('OUTPUT\n', output_details)

    data, imgs = get_data()  # get and preprocess data
    input_data = data[1]  # take one of the images
    org_image = imgs[1]  # save original
    print(input_data.shape)

    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Execute the inference
    t1 = time()
    interpreter.invoke()
    t2 = time()

    output_data1 = interpreter.get_tensor(output_details[0]['index'])[0]
    # print(output_data1)
    output_data2 = interpreter.get_tensor(output_details[1]['index'])
    # print(output_data2)
    output_data3 = interpreter.get_tensor(output_details[2]['index'])
    # print(output_data3)
    output_data4 = interpreter.get_tensor(output_details[3]['index'])
    # print(output_data4)

    pred = np.array(output_data1)
    pred = np.reshape(pred, (-1, 3))
    landmarks = []
    for i, lmk in enumerate(pred):
        # print(lmk)
        lmx = int(lmk[0] / 224.0 * 500)
        lmy = int(lmk[1] / 224.0 * 500)
        landmarks.append([lmx, lmy])
        if i == 8:  # make the tip of the idex finger more visible for reference
            cv2.circle(org_image, (lmx, lmy), 4, (255, 0, 0), -1)
        else:
            cv2.circle(org_image, (lmx, lmy), 2, (0, 0, 255), -1)

    print(landmarks)
    cv2.imshow('tflite model', org_image)
    cv2.waitKey(0)
    print('Inference time:', t2 - t1, 's')


if __name__ == "__main__":
    main()
