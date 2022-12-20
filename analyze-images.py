import pandas as pd 
import json

import logging
import glob
import os
from pathlib import Path
import time
from configparser import ConfigParser

from detectcvlabels import detect_cv_labels
from detectcvlabels import verify_directory
from generatemap import create_clustered_map


logging.getLogger().setLevel(logging.INFO)

# ML techniques
ML_CVLIB = 'cvlib'

# Config section
DEFAULT_CONFIG = 'DEFAULT'


def detect_objects(photo, technique, result_path):
    logging.info('--- Analyzing photo with %s to detect objects: %s', technique, photo)
    prediction = None
    if technique is ML_CVLIB:
        prediction = detect_cv_labels(photo, result_path)
    return prediction

def get_image_coordinates(prediction, photo,i): 
    
    if(i==1):
        prediction['lat'] = 36.858898
        prediction['lon'] = 10.196500
        prediction['direction'] = 1
        prediction['positioningError'] = 1
        
    if(i==2):
        prediction['lat'] = 34.730463
        prediction['lon'] = 10.742574
        prediction['direction'] = 1
        prediction['positioningError'] = 1
    if(i==3):
        prediction['lat'] = 36.721883
        prediction['lon'] = 9.191392
        prediction['direction'] = 1
        prediction['positioningError'] = 1

    return prediction


def produce_df(predictions, topic, device, technique):
    df = pd.read_json(json.dumps(predictions), lines = False)
    df['topic'] = topic
    df['device'] = device
    df['technique'] = technique

    return df


def get_filenames(directory):
    files = []
    os.chdir(directory)
    for file in glob.glob('*.*'):
        files.append(file)
    return files

def write_json(prediction, path, photo, technique):
    file_name = path + photo + '-' + technique + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(prediction, outfile, indent = 4, ensure_ascii = False)

def write_csv(df, result_path, topic, technique):
    df.to_csv(result_path + topic + '.csv', index=False)

def read_config():
    parser = ConfigParser()
    parser.read('config.ini')
    return parser


# MAIN
def main():
    technique = ML_CVLIB

    # Read configuration from config.ini
    config = read_config()
    local_path = config.get(DEFAULT_CONFIG, 'LocalPath')
    result_path = config.get(DEFAULT_CONFIG, 'ResultPath')
    query_date = config.get(DEFAULT_CONFIG, 'Date')
    topic = config.get(DEFAULT_CONFIG, 'Topic')
    device = config.get(DEFAULT_CONFIG, 'Device')

    local_path = str(Path(local_path).absolute().resolve()) + os.path.sep 
    result_path = str(Path(result_path).absolute().resolve()) + os.path.sep

    logging.info('--- Reading images from: %s', local_path)
    photos = get_filenames(local_path)
    verify_directory(result_path)
    
    predictions = []
    i=1
    for photo in photos:
        start = time.perf_counter()
        prediction = detect_objects(photo, technique, result_path)
        prediction = get_image_coordinates(prediction, local_path + photo,i)
        end = time.perf_counter()
        prediction['timeElapsed'] = round(end-start, 3)
        write_json(prediction, result_path, photo, technique)
        predictions.append(prediction)
        i=i+1

    logging.info('--- Writing analysis results to: %s', result_path)
    df = produce_df(predictions, topic, device, technique)
    write_csv(df, result_path, topic, technique)
    create_clustered_map(local_path, df, result_path, topic)
    logging.info('--- Analysis completed')

if __name__ == "__main__":
    main()
