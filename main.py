#!/usr/bin/env python3
import logging
import sys
from k8s import K8S
from prettytable import PrettyTable


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s \t%(message)s')

    namespace = 'kube-system'
    k8s = K8S()
    ascii_table = PrettyTable(align='l')

    # Вывод таблицы с данными подов
    for pod in k8s.get_pods(namespace=namespace):
        ascii_table.add_row([
            pod.namespace, pod.name, pod.image, pod.ip, pod.created_at,
            pod.cpu_request, pod.cpu_limit, pod.memory_request, pod.memory_limit
        ])
    ascii_table.field_names = [
        'Namespace', 'Name', 'Image', 'IP', 'Created At', 'CPU Request', 'CPU Limit', 'Memory Request', 'Memory Limit'
    ]
    logging.info('Pods information:\n' + str(ascii_table) + '\n')
    ascii_table.clear()

    # Вывод таблицы с используемыми в namespace образами
    for image in k8s.get_images(namespace=namespace):
        ascii_table.add_row([image])
    ascii_table.field_names = ['Image']
    logging.info('Images information:\n' + str(ascii_table) + '\n')
    ascii_table.clear()

    return 0


if __name__ == '__main__':
    sys.exit(main())
