#!/usr/bin/env python3
import pandas as pd
import os
import sys
import numpy as np
from functools import reduce
import fplib
from ase.io import read as ase_read

def get_ixyz(lat, cutoff):
    lat = np.ascontiguousarray(lat)
    lat2 = np.dot(lat, np.transpose(lat))
    vec = np.linalg.eigvals(lat2)
    ixyz = int(np.sqrt(1.0/max(vec))*cutoff) + 1
    ixyz = np.int32(ixyz)
    return ixyz

def count_atoms_within_cutoff(lat, rxyz, cutoff):
    natoms = len(rxyz)
    count = 0

    ixyzf = get_ixyz(lat, cutoff)
    ixyz = int(ixyzf) + 1

    for iat in range(natoms):
        xi, yi, zi = rxyz[iat]

        for jat in range(natoms):
            if jat == iat:
                continue  # Skip the same atom

            for ix in range(-ixyz, ixyz + 1):
                for iy in range(-ixyz, ixyz + 1):
                    for iz in range(-ixyz, ixyz + 1):

                        xj = rxyz[jat][0] + ix * lat[0][0] + iy * lat[1][0] + iz * lat[2][0]
                        yj = rxyz[jat][1] + ix * lat[0][1] + iy * lat[1][1] + iz * lat[2][1]
                        zj = rxyz[jat][2] + ix * lat[0][2] + iy * lat[1][2] + iz * lat[2][2]

                        d2 = (xj - xi) ** 2 + (yj - yi) ** 2 + (zj - zi) ** 2

                        if d2 < cutoff ** 2:
                            count += 1
                            break  # Only need to count one image per jat

    return count
def recommend_cutoff_and_nx(lat, rxyz, initial_cutoff=6.0, max_cutoff=10.0, step=0.5):
    """
    Recommend a suitable `cutoff` and `nx` value based on lattice and atomic positions.

    Parameters:
    lat: numpy.ndarray
        Lattice matrix.
    rxyz: numpy.ndarray
        Positions of atoms in the unit cell.
    initial_cutoff: float
        Starting value for the cutoff radius.
    max_cutoff: float
        Maximum cutoff radius to try.
    step: float
        Step size to increase the cutoff.

    Returns:
    tuple:
        Recommended cutoff and nx.
    """
    cutoff = initial_cutoff
    best_cutoff = initial_cutoff
    best_nx = 0

    lat = np.array(lat, dtype = np.float64)
    rxyz = np.array(rxyz, dtype = np.float64)

    while cutoff <= max_cutoff:
        cutoff = np.float64(cutoff)
        max_atoms_in_sphere = count_atoms_within_cutoff(lat, rxyz, cutoff)
        if max_atoms_in_sphere > best_nx:
            best_nx = max_atoms_in_sphere
            best_cutoff = cutoff

        cutoff += step

    return best_cutoff, best_nx
def read_types(cell_file):
    buff = []
    with open(cell_file) as f:
        for line in f:
            buff.append(line.split())
    try:
        typt = np.array(buff[5], int)
    except:
        del(buff[5])
        typt = np.array(buff[5], int)
    types = []
    for i in range(len(typt)):
        types += [i+1]*typt[i]
    types = np.array(types, int)
    return types

if __name__ == "__main__":
    current_dir = './'
    x = 0
    glitchy_files = []
    for filename in os.listdir(current_dir):
        f = os.path.join(current_dir, filename)
        if os.path.isfile(f) and os.path.splitext(f)[-1].lower() == '.vasp':
            atoms = ase_read(f)
            lat = atoms.cell[:]
            rxyz = atoms.get_positions()
            chem_nums = list(atoms.numbers)
            znucl_list = reduce(lambda re, x: re+[x] if x not in re else re, chem_nums, [])
            typ = len(znucl_list)
            znucl = np.array(znucl_list, int)
            types = read_types(f)
            cell = (lat, rxyz, types, znucl)

            natx = 256
       #     best_cutoff,best_nx = recommend_cutoff_and_nx(lat,rxyz)
            cutoff = 4.0
            nx = natx
       #     print("cutoff=",cutoff)
       #     print("nx= ",nx)
       #    cutoff = np.float64(int(np.sqrt(8.0)) * 3)  # Shorter cutoff for GOM
            is_glitchy = False  # 标记文件是否有问题
            
            atom_count = count_atoms_within_cutoff(lat, rxyz, cutoff)
            if atom_count > natx:
                is_glitchy = True  # 触发异常，标记文件有问题
                print("cutoff too large\n") 
                x+=1
                print("atom_count:",atom_count)
            if len(rxyz) != len(types) or len(set(types)) != len(znucl):
                is_glitchy = True  # 类型匹配有问题，标记文件有问题
            if is_glitchy:
                print(f"{filename} is glitchy !")
                glitchy_files.append(filename.replace('.vasp', ''))
            else:
                fp = fplib.get_lfp(cell, cutoff=cutoff, natx=natx, log=False)  # Long Fingerprint
    print("x=",x)        
    print("Total glitchy files:", len(glitchy_files))
  
    csv_path = "fulllist.csv"
    output_csv_path = "id_prop.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, header= None)
        df_filtered = df[~df[0].isin(glitchy_files)]  # 删除有问题的行
        df_filtered.to_csv(output_csv_path, index=False)
        print(f"Filtered data saved to {output_csv_path}")
    else:
        print(f"CSV file {csv_path} not found!")
