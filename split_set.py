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
    print("Separando el {}% de {}...".format(q, path))
    base, ext = os.path.splitext(path)

    full_data = json.load(open(path))

    print("{} mails.".format(len(full_data)))

    test_data = random.sample(full_data, int(q * len(full_data) / 100.0))
    dev_data = [mail for mail in full_data if mail not in test_data]

    dev_out_path = base + '_dev.json'
    test_out_path = base + '_test.json'

    with open(dev_out_path, 'w+') as outfile:
        json.dump(dev_data, outfile)
        print("{} mails guardados en {}".format(len(dev_data), outfile.name))

    with open(test_out_path, 'w+') as outfile:
        json.dump(test_data, outfile)
        print("{} mails guardados en {}".format(len(test_data), outfile.name))

    print("===" * 10 + '\n')

if __name__ == '__main__':
    # q es el porcentaje que queremo
    parser = argparse.ArgumentParser()

    parser.add_argument("--porcentaje", help="Porcentaje de datos a convertir en test (entre 0.0 y 99.9). Por defecto, 10", default=10, type=float)
    parser.add_argument("--base_dir", help="Directorio donde encontrar ham.json y spam.json (por defecto, data/)", default="data/")
    parser.add_argument("--seed", help="Seed random", default=100023045129, type=int)

    args = parser.parse_args()

    random.seed(args.seed)

    print("Partiendo conjunto de datos.")
    print("Porcentaje tomado de cada conjunto = {}%".format(args.porcentaje))
    print("Seed = {}%\n\n\n".format(args.seed))

    split_file(os.path.join(args.base_dir, "ham.json"), args.porcentaje)
    split_file(os.path.join(args.base_dir, "spam.json"), args.porcentaje)
