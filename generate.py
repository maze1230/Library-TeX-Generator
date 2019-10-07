from argparse import ArgumentParser
import toml
import os
import subprocess


def get_option():
    argparser = ArgumentParser(description='指定したテンプレートTeXファイルの"%%%INSERT HERE%%%"部分に別ファイルで指定したライブラリファイルを挿入する。')
    argparser.add_argument('-t', '--template', default='template.tex',
                           help='テンプレートとなるTeXファイル')
    argparser.add_argument('-l', '--library', default='library.toml',
                           help='使いたいライブラリのファイルをまとめたtomlファイル')
    argparser.add_argument('-o', '--output', default='library.tex',
                           help='出力するファイルの名前')
    argparser.add_argument('-p', '--pdf', help="コンパイルしてPDFファイルを作成する",
                           action="store_true")

    return argparser.parse_args()


category_style = '\\noindent \\large\n'
title_style = '\\noindent \\small\n'


def write_lib_file(fp, name, path):
    fp.write(title_style)
    name = name.replace('_', '\_')
    fp.write(name+'\n')
    fp.write('\\myMintedfile{'+path+'}\n')


if __name__ == '__main__':
    args = get_option()

    dict_toml = toml.load(open(args.library))

    with open(args.template, 'r') as rf, open(args.output, 'w') as wf:
        for l in rf.readlines():
            if not l.startswith('%%%INSERT HERE%%%'):
                wf.write(l)
                continue

            for libs in dict_toml['library']:
                wf.write(category_style)
                wf.write(libs['category']+'\\\\\n')

                if 'file' in libs:
                    for lib in libs['file']:
                        if not os.path.isfile(lib['path']):
                            print("Failed to find the file: {}\n    name: {}".format(lib['path'], lib['name']))
                            continue
                        path = os.path.abspath(lib['path'])
                        write_lib_file(wf, lib['name'], path)

                if 'dir' in libs:
                    for dir in libs['dir']:
                        if not os.path.isdir(dir['path']):
                            continue

                        for lib in os.listdir(dir['path']):
                            if not os.path.isfile(os.path.join(dir['path'], lib)):
                                continue
                            if not os.path.splitext(lib)[1] == '.cpp':
                                continue
                            path = os.path.abspath(os.path.join(dir['path'], lib))
                            write_lib_file(wf, dir['name']+lib, path)
    
    if args.pdf:
        filename = args.output.split('.')[0]
        subprocess.call(['platex', '-shell-escape', filename+'.tex'])
        subprocess.call(['dvipdfmx', filename+'.dvi'])
        subprocess.call(['rm', filename+'.dvi', filename+'.log', filename+'.aux'])
