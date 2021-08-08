import argparse
from integrated import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name',type=str, help='.vtpを抜いたプロジェクトファイル名を入力する')
    parser.add_argument('--database', action='store_true')
    parser.add_argument('--copy', action='store_true')
    args = parser.parse_args()


    # RPA
    edit_vista(args)
    #preview

if __name__ == "__main__":
    main()\