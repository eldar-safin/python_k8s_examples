#!/usr/bin/env python3
import logging
from k8s import K8S


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s \t%(message)s')

    k8s = K8S()
    namespace = ''

    for pod in k8s.get_pods(namespace=namespace):
        logging.info(pod.to_json())

    for image in k8s.get_images(namespace=namespace):
        logging.info(image)


if __name__ == '__main__':
    main()
