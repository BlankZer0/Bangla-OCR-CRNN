import os
import cv2
import json

WIDTH = 300
HEIGHT = 150
DIM = (WIDTH, HEIGHT)

dataset_path = r"BanglaWriting"
extracted_path = r"BanglaWriting Extracted"

try:
    # Create  Directory  MyDirectory 
    os.mkdir(extracted_path)
except FileExistsError:
    ##print if directory already exists
    print("Directory already exists.")

for sub_dir in os.listdir(dataset_path):

    dataset_sub_dir = os.path.join(dataset_path, sub_dir)

    try:
        # Create  Directory  MyDirectory 
        os.mkdir(os.path.join(extracted_path, sub_dir))
    except FileExistsError:
        ##print if directory already exists
        print("Directory already exists.")

    word_counter = 0

    for filename in os.listdir(dataset_sub_dir):
        
        if filename.endswith(".json"):

            json_file = open(os.path.join(dataset_sub_dir, filename), encoding='utf-8')
            page = json.load(json_file)

            # take the image file name from the json file
            # image_path = page["imagePath"]

            # if not image_path[0].isdigit():
            #     image_path = image_path.rsplit("\\", 1)[1]

            image_path = filename.replace(".json", ".jpg")

            image = cv2.imread(os.path.join(dataset_sub_dir, image_path))

            image_path = image_path.replace(".jpg", "")

            # faulty_pages = ["256_14_1/", "25_22_0/"]
            # if image_path in faulty_pages:
            #     continue

            print("Extracting from " + image_path + " | words in page: " + str(len(page["shapes"])))

            for i in range(len(page["shapes"])):

                word_counter += 1

                label = page["shapes"][i]["label"] # label of the word
                # pixel coordinates of the bounding box
                xmin, ymin = page["shapes"][i]["points"][0]
                xmax, ymax = page["shapes"][i]["points"][1]

                word = image[int(ymin):int(ymax), int(xmin):int(xmax)]

                # cv2.imshow("example", word)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
                if word.shape[0] == 0 or word.shape[1] == 0:
                    continue
                
                word_resized = cv2.resize(word, DIM)
                cv2.imwrite(os.path.join(extracted_path, sub_dir, str(word_counter) + "_" + label + ".jpg"), word_resized)


