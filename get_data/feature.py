import cv2
import numpy as np
from BiT import bio_taxo # Bitdesc
import mahotas.features as ft
def fct_haralick(data):
    stats = ft.haralick(data).mean(0).tolist()
    return stats

def fct_BiT(data):
    return bio_taxo(data)

def Har_Bit(data):
    return fct_haralick(data) + fct_BiT(data)

def process_image(image):
    rgb = cv2.imread(image)
    r, g, b = cv2.split(rgb)
    # Convert into gray
    rgb_gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    r_gray = r
    g_gray = g
    b_gray = b
    # Extract features
    rgb_feat = np.array(Har_Bit(rgb_gray))
    r_feat = np.array(Har_Bit(r_gray))
    g_feat = np.array(Har_Bit(g_gray))
    b_feat = np.array(Har_Bit(b_gray))
    # Concatenate features 
    combined_features = np.hstack((rgb_feat, r_feat, g_feat, b_feat,))
    return combined_features