from __future__ import print_function
import os
import sys
import codecs  # sub for python 3 style open
import lxml
from lxml.html.clean import Cleaner
import gzip
import json


def _diriter(root_dir, extension):
    ''' grab files from root/sub dirs having extension
    '''
    return ((f, os.path.join(root, f))
            for root, dirs, files in os.walk(root_dir)
            for f in files if f.endswith(extension))


def pdf_to_txt(root_dir):
    ''' convert all pdfs in root/sub to txt
        write txt version of files in same dir as pdf version
    '''
    for pdf_file, pdf_path in _diriter(root_dir, '.pdf'):
        os.system(('pdftotext "%s" -q') % pdf_path)


def htm_to_txt(root_dir):
    ''' convert all htms in root/sub to txt
        writing to txt file b/c i'm lazy and want to treat the same as pdf_to_txt
    '''
    cleaner = Cleaner(allow_tags=[''], remove_unknown_tags=False)
    cleaner.javascript, cleaner.style = True, True

    for htm_file, htm_path in _diriter(root_dir, '.htm'):
        txt_file = '{}.txt'.format(os.path.splitext(htm_path)[0])
        with open(txt_file, 'w') as txt:
            txt.write(
                lxml.html.tostring(cleaner.clean_html(lxml.html.parse(htm_path)))
            )


def txt_to_jsonl(root_dir, out_file_path):
    ''' collect txtfiles in root/sub dir and write them to jsonl
    '''
    with gzip.GzipFile(out_file_path, 'wb') as jsonl:
        for txt_file, txt_path in _diriter(root_dir, '.txt'):
            with codecs.open(txt_path, 'r', encoding='utf-8', errors='ignore') as txt:
                json.dump({'name': txt_file, 'content': txt.read()}, jsonl)
                jsonl.write('\n')


def _txt_del(root_dir):
    ''' remove text files after process files is complete
    '''
    for txt_file, txt_path in _diriter(root_dir, '.txt'):
        os.remove(txt_path)


def _process_files(file_dir, out_file_path):
    ''' transform pdf, htm files to txt, load txt to jsonl file
    '''
    print('pdf to text ...')
    pdf_to_txt(file_dir)
    print('htm to text ...')
    htm_to_txt(file_dir)
    print('text to jsonl ...')
    txt_to_jsonl(file_dir, out_file_path)
    print('complete.')


if __name__ == '__main__':
    ''' transform all pdf and htm files in input directory to jsonl file

        arg 1: FILE_DIR - the dir contaning pdf and/or htm files
        arg 2: OUTPUT_FILE_PATH - the path of the output jsonl file

    '''

    FILE_DIR = 'test_data'
    OUTPUT_FILE_PATH = 'output/docs.jsonl.gz'

    if len(sys.argv) > 1:
        FILE_DIR, OUTPUT_FILE_PATH = str(sys.argv[1]), str(sys.argv[2])

    if not (os.path.exists(FILE_DIR) and os.path.exists(os.path.dirname(OUTPUT_FILE_PATH))):
        print('%s or %s does not exist. check yourself.') % (FILE_DIR, OUTPUT_FILE_PATH)
        sys.exit(2)

    try:
        _process_files(FILE_DIR, OUTPUT_FILE_PATH)
    except Exception as ex:
        logging.exception('Awesome Job on your code fail!.')
    finally:
        _txt_del(FILE_DIR)
