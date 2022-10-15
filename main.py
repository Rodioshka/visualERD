import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def get_data() -> dict:
    with open(r'data/entity', 'r', encoding='utf-8') as file:
        qs = file.read().splitlines()
    data = {(item[0], item[2]): item[1] for item in [i.split(',') for i in qs]}
    return data


def main():
    data = get_data()
    print(data)


if __name__ == '__main__':
    main()
