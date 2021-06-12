import argparse
import make_project

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name',type=str, help='.vtpを抜いたプロジェクトファイル名を入力する')
    parser.add_argument('--database', action='store_true')
    parser.add_argument('--copy', action='store_true')
    parser.add_argument('--distance', type=float, default=1.0)
    args = parser.parse_args()

    make_project.edit_vista(args)

if __name__ == "__main__":
    main()