import cv2

img1 = cv2.imread("../datasets/ps_i4_provenance/assets/A081__resize_640.jpg", 0)
img2 = cv2.imread("../datasets/ps_i4_provenance/assets/A081__crop_10pct.jpg", 0)

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING)

matches = bf.knnMatch(des1, des2, k=2)

# Apply Lowe's ratio test
good_matches = []

for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

print("Good ORB matches:", len(good_matches))