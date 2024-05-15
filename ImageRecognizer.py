import cv2 as cv
from sentence_transformers import util
from PIL import Image
import numpy as np
import torch
import open_clip


class ImageRecognizer:
    def __init__(self, imagesCount, subImagesCount):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        zipModel = open_clip.create_model_and_transforms('ViT-B-16-plus-240',
                                                                            pretrained="laion400m_e32")
        self.model = zipModel[0]
        self.preprocess = zipModel[1]
        self.imagesCount = imagesCount
        self.subImagesCount = subImagesCount

    def imageEncoder(self, img):
        img1 = Image.fromarray(img).convert('RGB')
        img1 = self.preprocess(img1).unsqueeze(0).to(self.device)
        img1 = self.model.encode_image(img1)
        return img1

    def generateScore(self, image1, image2):
        test_img = cv.imread(image1, cv.IMREAD_UNCHANGED)
        data_img = cv.imread(image2, cv.IMREAD_UNCHANGED)
        img1 = self.imageEncoder(test_img)
        img2 = self.imageEncoder(data_img)
        cos_scores = util.pytorch_cos_sim(img1, img2)
        score = round(float(cos_scores[0][0]) * 100, 2)
        return score

    def checkingResult(self, image1FileName):
        scores = np.zeros((6, 12))
        for i in range(1, 7):
            for j in range(1, 13):
                image2FileName = f'Images/{i}/{i}_1_{j}.jpg'
                score = round(self.generateScore(image1FileName, image2FileName), 2)
                scores[i - 1, j - 1] = score
        index = np.unravel_index(np.argmax(scores, axis=None), scores.shape)
        return index
