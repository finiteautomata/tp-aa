# -*- coding: utf-8 -*-
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import os
import sys
import argparse
import json
import random


# q es el porcentaje que va a tomar para test
def split_file(path, q):
    base, ext = os.path.splitext(path)

    full_data = json.load(open(path))
    test_data = random.sample(full_data, int(q * len(full_data) / 100.0))
    dev_data = [mail for mail in full_data if mail not in test_data]

    with open(base + '_dev.json', 'w+') as outfile:
        json.dump(dev_data, outfile)

    with open(base + '_test.json', 'w+') as outfile:
        json.dump(test_data, outfile)


if __name__ == '__main__':
    # q es el porcentaje que queremo
    parser = argparse.ArgumentParser()

    parser.add_argument("--porcentaje", help="Porcentaje de datos a convertir en test (entre 0.0 y 99.9). Por defecto, 10", default=10, type=float)
    parser.add_argument("--base_dir", help="Directorio donde encontrar ham.json y spam.json (por defecto, data/)", default="data/")
    parser.add_argument("--seed", help="Seed random", default=100023045129, type=int)

    args = parser.parse_args()

    random.seed(args.seed)

    split_file(os.path.join(args.base_dir, "ham.json"), args.porcentaje)
    split_file(os.path.join(args.base_dir, "spam.json"), args.porcentaje)
