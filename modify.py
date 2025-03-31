import os

vasp_files = [f for f in os.listdir() if f.endswith(".vasp")]

for input_file in vasp_files:
    output_file = f"POSCAR_{input_file}"

    with open(input_file, "r") as f:
        lines = f.readlines()

    lines[0] = "SnBC\n" #modify with your choice

    lines[5] = "C B Sn\n" #modify with your choice

    lines[6] = lines[6].strip() + "   8\n"

    extra_lines = [
        "  0.250000000         0.000000000         0.500000000           \n"
        "  0.750000000         0.000000000         0.500000000           \n"
        "  0.500000000         0.250000000         0.000000000           \n"
        "  0.500000000         0.750000000         0.000000000           \n"
        "  0.000000000         0.500000000         0.250000000           \n"
        "  0.000000000         0.500000000         0.750000000           \n"
        "  0.000000000         0.000000000         0.000000000           \n"
        "  0.500000000         0.500000000         0.500000000           \n"
    ]

    with open(output_file, "w") as f:
        f.writelines(lines + extra_lines)

    print(f"file {input_file} is reserved as {output_file}")
