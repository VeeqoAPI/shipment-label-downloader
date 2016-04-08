# Shipment Label Downloader

Sample application which consumes [Veeqo API][] in order to download labels for
the shipped today orders.

## Requirements

Python 2.7

## Installation

Clone repository:

    git clone git@github.com:veeqoapi/shipment-label-downloader.git

Switch to the directory:

    cd shipment-label-downloader

Add config file:

    cp config.ini-sample config.ini

Use your favorite editor to update `config.ini` file with your API Key.

## Usage

    python get_labels.py

Labels will be downloaded into the `./labels` directory

[Veeqo API]: http://developers.veeqo.com/
