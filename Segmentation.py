from Lab2 import CCA1
import os
import cv2
import numpy as np
import copy
import csv


def binary_change(image, value):
    shape = np.shape(image)
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if image[i][j] != 0:
                image[i][j] = value

    return image


def add(image, image1):

    shape = np.shape(image)
    overall_image = np.zeros(shape)
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            s = image[i][j] + image1[i][j]
            if s > 255:
                overall_image[i][j] = 255
            else:
                overall_image[i][j] = s

    return overall_image


def loss(actual, estimated):
    shape = np.shape(actual)
    accuracy = 0
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if actual[i][j] == estimated[i+1][j+1]:
                accuracy += 1

    accuracy /= (shape[0]*shape[1])
    return accuracy


def freq_count(new_image):
    image_mapping = {}
    shape = np.shape(new_image)

    for i in range(1, shape[0]):
        for j in range(1, shape[1]):
            if new_image[i][j] in image_mapping:
                image_mapping[int(new_image[i][j])] += 1
            else:
                image_mapping[int(new_image[i][j])] = 1

    return image_mapping


def fill_gaps(image, freq_mapping):
    new_image = copy.deepcopy(image)
    freq_mapping.pop(0)
    max_value = max(freq_mapping.values())

    for keys in freq_mapping:
        if freq_mapping[keys] == max_value:
            continue
        new_image[new_image == keys] = 0

    return new_image


def fill_gaps_nucleus(image, freq_mapping):

    new_image = copy.deepcopy(image)
    freq_mapping.pop(0)

    if len(freq_mapping.values()) == 0:
        return image

    max_value = max(freq_mapping.values())
    max_label = 0

    for keys in freq_mapping:
        if freq_mapping[keys] == max_value:
            max_label = keys

    for keys in freq_mapping:
        if keys == max_label or freq_mapping[keys] > 300:
            continue
        new_image[new_image == keys] = 0

    return new_image


def fill_WBC_gaps(WBC_image, cytoplasm_image, WHB_freq_count, value):

    WHB_freq_count.pop(0)
    max_island = max(WHB_freq_count.values())

    new_image = copy.deepcopy(cytoplasm_image)

    for keys in WHB_freq_count:
        if WHB_freq_count[keys] == max_island:
            continue
        else:
            new_image[WBC_image == keys] = value

    return new_image


def split_chunk_mean(original_image, chunk_size):
    arr = []
    shape = np.shape(original_image)
    new_image = np.zeros(shape)

    for i in range(0, shape[0]-chunk_size[0]+1, chunk_size[0]):
        for j in range(0, shape[1]-chunk_size[1]+1, chunk_size[1]):
            chunk = original_image[i:i+chunk_size[0], j:j+chunk_size[1]]
            chunk_mean = np.mean(chunk)
            arr.append(int(chunk_mean))

            new_image[i:i+chunk_size[0], j:j+chunk_size[1]] = chunk_mean

    return arr, new_image


def dice_coefficient(actual_image, estimated_image):

    shape = np.shape(actual_image)

    nucleus_region_accuracy = 0
    nucleus_region_count = 0
    cytoplasm_region_accuracy = 0
    cytoplasm_region_count = 0
    WBC_region_accuracy = 0
    WBC_region_count = 0

    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if actual_image[i][j] == 0:
                WBC_region_count += 1
                if actual_image[i][j] == estimated_image[i+1][j+1]:
                    WBC_region_accuracy += 1
            elif actual_image[i][j] == 128:
                cytoplasm_region_count += 1
                if actual_image[i][j] == estimated_image[i+1][j+1]:
                    cytoplasm_region_accuracy += 1
            elif actual_image[i][j] == 255:
                nucleus_region_count += 1
                if actual_image[i][j] == estimated_image[i+1][j+1]:
                    nucleus_region_accuracy += 1

    return nucleus_region_accuracy/nucleus_region_count, cytoplasm_region_accuracy/cytoplasm_region_count, WBC_region_accuracy/WBC_region_count


if __name__ == "__main__":

    total_loss = []

    nucleus_region_loss = []
    cytoplasm_region_loss = []
    WBC_region_loss = []

    path = "C:\\Users\\Ahmad Zeeshan\\OneDrive\\Desktop\\semestor\\6th semestor\\DIP\\Assignment\\test-20250207T090048Z-001\\test\\images"
    path1 = "C:\\Users\\Ahmad Zeeshan\\OneDrive\\Desktop\\semestor\\6th semestor\\DIP\\Assignment\\test-20250207T090048Z-001\\test\\masks"

    path_ = "C:\\Users\\Ahmad Zeeshan\\OneDrive\\Desktop\\semestor\\6th semestor\\DIP\\Assignment\\train-20250207T090047Z-001\\train\\images"
    path1_ = "C:\\Users\\Ahmad Zeeshan\\OneDrive\\Desktop\\semestor\\6th semestor\\DIP\\Assignment\\train-20250207T090047Z-001\\train\\masks"

    path_file = "C:\\Users\\Ahmad Zeeshan\\OneDrive\\Desktop\\semestor\\6th semestor\\DIP\\Assignment\\Results.csv"

    with open(path_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Mask', 'Nucleus_Loss', 'Cytoplasm_Loss', 'WBC_Loss', 'Overall_Accuracy'])

    for images, masks in zip(os.listdir(path_),  os.listdir(path1_)):

        image = cv2.imread(os.path.join(path_, images), 0)
        mask = cv2.imread(os.path.join(path1_, masks), 0)

        padded_image = np.pad(image, ((1, 1), (1, 1)), mode='constant', constant_values=0)

        mean = np.mean(image)
        means, arr = split_chunk_mean(image, (15, 15))

        arr = arr.astype(np.uint8)

        nmv = []
        cmv = []
        for value in means:
            if value >= min(means) and value <= min(means)+55:
                nmv.append(value)
            elif value >= min(means)+60 and value <= 200:
                cmv.append(value)

        nucleus_mean_value = np.mean(nmv)
        cytoplasm_mean_value = np.mean(cmv)

        if cytoplasm_mean_value == np.inf:
            cytoplasm_mean_value = mean*1.05

        mean = np.mean(image)
        v_set = set(range(1, int(nucleus_mean_value * 1.1125)))
        v_set1 = set(range(1, int(np.mean(means) * 1.025)))

        nucleus_region, mapping = CCA1(padded_image, np.shape(padded_image), v_set)
        cytoplasm_region, mapping1 = CCA1(padded_image, np.shape(padded_image), v_set1)

        freq_count_1 = freq_count(cytoplasm_region)
        cytoplasm_region = fill_gaps(cytoplasm_region, freq_count_1)

        new_matrix1_gap_cytoplasm = copy.deepcopy(cytoplasm_region)

        gap_matrix_shape = np.shape(new_matrix1_gap_cytoplasm)

        new_matrix1_gap_cytoplasm[0] = 1
        new_matrix1_gap_cytoplasm[:, 0] = 1
        new_matrix1_gap_cytoplasm[gap_matrix_shape[0] - 1] = 1
        new_matrix1_gap_cytoplasm[:, gap_matrix_shape[1] - 1] = 1

        WBC_holes_cytoplasm, WBC_cytoplasm_mapping = CCA1(new_matrix1_gap_cytoplasm, gap_matrix_shape, {0})

        freq_count_WBC_cytoplasm_gaps = freq_count(WBC_holes_cytoplasm)
        freq_count_nucleus = freq_count(nucleus_region)

        cytoplasm_region = binary_change(cytoplasm_region, 128)
        cytoplasm_region = fill_WBC_gaps(WBC_holes_cytoplasm, cytoplasm_region, freq_count_WBC_cytoplasm_gaps, 128)
        nucleus_region = binary_change(nucleus_region, 255)

        overall_image = add(cytoplasm_region, nucleus_region)
        overall_image = overall_image.astype(np.uint8)

        Loss = loss(mask, overall_image)
        N_L, C_L, WBC_L = dice_coefficient(mask, overall_image)

        with open(path_file, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([masks, N_L, C_L, WBC_L, Loss])

        nucleus_region_loss.append(N_L)
        cytoplasm_region_loss.append(C_L)
        WBC_region_loss.append(WBC_L)

        total_loss.append(Loss)

    print(total_loss)
    print(np.mean(total_loss))
    print(np.mean(nucleus_region_loss))
    print(np.mean(cytoplasm_region_loss))
    print(np.mean(WBC_region_loss))


        # blue is nucleus
        # red is white blood cells
        # shades of blue and red WBP


# 200, 195, 149, 129, 98








