from argparse import ArgumentParser
import toml


def get_option():
    argparser = ArgumentParser(description='指定したテンプレートTeXファイルの"%%%INSERT HERE%%%"部分に別ファイルで指定したライブラリファイルを挿入する。')
    argparser.add_argument('-t', '--template', default='template.tex',
                           help='テンプレートとなるTeXファイル')
    argparser.add_argument('-f', '--file', default='library.toml',
                           help='使いたいライブラリのファイルをまとめたtomlファイル')
    argparser.add_argument('-o', '--output', default='library.tex',
                           help='出力するファイルの名前')

    return argparser.parse_args()


if __name__ == '__main__':
    args = get_option()

    dict_toml = toml.load(open(args.file))
    category_style = '\\noindent \\large\n'
    title_style = '\\noindent \\small\n'

    with open(args.template, 'r') as rf, open(args.output, 'w') as wf:
        for l in rf.readlines():
            if not l.startswith('%%%INSERT HERE%%%'):
                wf.write(l)
                continue

            for libs in dict_toml['library']:
                wf.write(category_style)
                wf.write(libs['category']+'\\\\\n')

                for lib in libs['file']:
                    wf.write(title_style)
                    wf.write(lib['name']+'\n')
                    wf.write('\\myMintedfile{'+lib['file']+'}\n')
