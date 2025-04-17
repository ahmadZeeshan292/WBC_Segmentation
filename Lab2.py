def CCA1(image, shape, v_set):
    mapping = {}
    label = 0
    new_matrix = np.zeros(shape)

    for i in range(1, shape[0]-1):
        for j in range(1, shape[1] - 1):

            if image[i][j] not in v_set:
                continue

            if image[i - 1][j] not in v_set and image[i][j - 1] not in v_set and image[i - 1][j - 1] not in v_set \
                    and image[i - 1][j + 1] not in v_set:
                label += 1
                mapping[label] = {int(label)}
                new_matrix[i][j] = int(label)
                continue

            collision_flag = False
            four_c_condition = image[i - 1][j] in v_set and image[i][j - 1] in v_set
            d_c_condition = image[i - 1][j - 1] in v_set and image[i - 1][j + 1] in v_set
            d_4_c_1 = image[i - 1][j - 1] in v_set and image[i - 1][j] in v_set
            d_4_c_2 = image[i - 1][j - 1] in v_set and image[i][j - 1] in v_set
            d_4_c_3 = image[i - 1][j + 1] in v_set and image[i - 1][j] in v_set
            d_4_c_4 = image[i - 1][j + 1] in v_set and image[i][j - 1] in v_set

            value1 = 0
            value2 = 0
            if new_matrix[i][j - 1] != new_matrix[i - 1][j] and four_c_condition:
                value1 = new_matrix[i][j - 1]
                value2 = new_matrix[i - 1][j]
                collision_flag = True
            elif new_matrix[i - 1][j - 1] != new_matrix[i - 1][j + 1] and d_c_condition:
                value1 = new_matrix[i - 1][j - 1]
                value2 = new_matrix[i - 1][j + 1]
                collision_flag = True
            elif new_matrix[i - 1][j - 1] != new_matrix[i - 1][j] and d_4_c_1:
                value1 = new_matrix[i - 1][j - 1]
                value2 = new_matrix[i - 1][j]
                collision_flag = True
            elif new_matrix[i - 1][j - 1] != new_matrix[i][j - 1] and d_4_c_2:
                value1 = new_matrix[i - 1][j - 1]
                value2 = new_matrix[i][j - 1]
                collision_flag = True
            elif new_matrix[i - 1][j + 1] != new_matrix[i - 1][j] and d_4_c_3:
                value1 = new_matrix[i - 1][j + 1]
                value2 = new_matrix[i - 1][j]
                collision_flag = True
            elif new_matrix[i - 1][j + 1] != new_matrix[i][j - 1] and d_4_c_4:
                value1 = new_matrix[i - 1][j + 1]
                value2 = new_matrix[i][j - 1]
                collision_flag = True

            min_val = int(min(value1, value2))
            max_val = int(max(value1, value2))
            if collision_flag and min_val != 0:
                a = int(next(iter(mapping[min_val])))
                while True:
                    if a in mapping[a]:
                        new_matrix[i][j] = a
                        mapping[a].update(mapping[max_val])
                        mapping[max_val] = {a}
                        break
                    else:
                        a = int(next(iter(mapping[a])))

            if collision_flag:
                continue

            if image[i - 1][j] in v_set or image[i][j - 1] in v_set:
                if new_matrix[i - 1][j] == new_matrix[i][j - 1]:
                    new_matrix[i][j] = int(new_matrix[i][j - 1])
                elif image[i - 1][j] in v_set and image[i][j - 1] not in v_set:
                    new_matrix[i][j] = int(new_matrix[i - 1][j])
                elif image[i - 1][j] not in v_set and image[i][j - 1] in v_set:
                    new_matrix[i][j] = int(new_matrix[i][j - 1])

            elif image[i - 1][j - 1] in v_set or image[i - 1][j + 1] in v_set:
                if new_matrix[i - 1][j - 1] == new_matrix[i - 1][j + 1]:
                    new_matrix[i][j] = int(new_matrix[i - 1][j - 1])
                elif image[i - 1][j - 1] in v_set and image[i - 1][j + 1] not in v_set:
                    new_matrix[i][j] = int(new_matrix[i - 1][j - 1])
                elif image[i - 1][j - 1] not in v_set and image[i - 1][j + 1] in v_set:
                    new_matrix[i][j] = int(new_matrix[i - 1][j + 1])

    print(new_matrix)

    for sets in mapping.values():
        if len(sets) > 1:
            value = next(iter(sets))
            sets.discard(value)
            for i in range(1, shape[0]):
                for j in range(1, shape[1]):
                    if new_matrix[i][j] in sets:
                        new_matrix[i][j] = value

    return new_matrix, mapping
