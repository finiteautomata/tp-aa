# -*- coding: utf-8 -*-
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import os
import sys
import argparse
import json
import random


def save_data(data, path):
    """Salva datos a un path."""
    with open(path, 'w+') as outfile:
        json.dump(data, outfile)
        print("{} mails guardados en {}".format(len(data), outfile.name))


# q es el porcentaje que va a tomar para test
def split_file(path, q):
    print("Separando el {}% de {}...".format(q, path))
    base, ext = os.path.splitext(path)

    full_data = json.load(open(path))

    print("{} mails.".format(len(full_data)))

    test_data = random.sample(full_data, int(q * len(full_data) / 100.0))
    dev_data = [mail for mail in full_data if mail not in test_data]
    small_dev_data = random.sample(dev_data, len(dev_data) / 10)

    save_data(test_data, base + '_test.json')
    save_data(dev_data, base + '_dev.json')
    save_data(small_dev_data, base + '_small_dev.json')


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
