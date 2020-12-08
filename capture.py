import cv2
import numpy as np
from keras.models import load_model

model = load_model('CNNmodel.h5')


def prediction(pred):
    return chr(pred + 65)


def keras_predict(model1, image):
    data = np.asarray(image, dtype="int32")
    pred_probab = model1.predict(data)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class


def keras_process_image(img):
    img = cv2.resize(img, (1, 28, 28), interpolation=cv2.INTER_AREA)

    return img


def crop_image(image, x, y, width, height):
    return image[y:y + height, x:x + width]


def main():
    while True:

        webcam = cv2.VideoCapture(0)
        rval, frame = webcam.read()
        frame = cv2.flip(frame, 1)

        im2 = crop_image(frame, 0, 300, 300, 300)
        image_grayscale = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (15, 15), 0)
        im3 = cv2.resize(image_grayscale_blurred, (28, 28), interpolation=cv2.INTER_AREA)

        im4 = np.resize(im3, (28, 28, 1))
        im5 = np.expand_dims(im4, axis=0)

        pred_probab, pred_class = keras_predict(model, im5)

        curr = prediction(pred_class)

        cv2.putText(frame, curr, (10, 300), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.rectangle(frame, (0, 300), (300, 600), (255, 255, 00), 3)
        cv2.imshow("frame", frame)
        
        cv2.imshow("Image3", image_grayscale_blurred)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()

# cam_capture.release()
cv2.destroyAllWindows()
