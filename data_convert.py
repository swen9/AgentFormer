def transform_split_and_save_data(input_file, train_output_file, test_output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()


    lines_tuples = [(float(line.split()[0]), line) for line in lines]
    # rank by frame number
    sorted_lines_tuples = sorted(lines_tuples, key=lambda x: x[0])

    # only keep even frame lines
    even_frame_lines = [line for frame, line in sorted_lines_tuples if frame % 2 == 0]

    transformed_lines = []
    for line in even_frame_lines:
        parts = line.strip().split()
        # frame number divided by 2
        parts[0] = str(float(parts[0]) / 2)
        # (x, y, z) -> (x - 584800, y - 4452400, z)
        parts[3] = str(float(parts[3]) - 584800) 
        parts[4] = str(float(parts[4]) - 4452400) 
        # delete the last column, adjust the order of the columns, fill other columns with -1, and replace the third column with "Car"
        new_line = [
            parts[0],  # frame number
            parts[1],  # ID
            "Car",
        ] + ["-1.0"] * 10 + [parts[3]] + ["-1.0"] + [parts[4]] + ["-1.0"]
        transformed_lines.append(" ".join(new_line))

    # split point
    split_point = int(len(transformed_lines) -10000)
    train_lines = transformed_lines[:split_point]
    test_lines = transformed_lines[split_point:]

    # write training data
    with open(train_output_file, 'w') as f:
        for line in train_lines:
            f.write(line + "\n")

    # write test data
    with open(test_output_file, 'w') as f:
        for line in test_lines:
            f.write(line + "\n")

transform_split_and_save_data('objects_3d_traj.txt', 'objects_3d_traj_train.txt', 'objects_3d_traj_val.txt')
