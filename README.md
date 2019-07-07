# Library TeX Generator

競プロ用ライブラリからPDFにするためのTeXファイルを作る

## Requirements

- LaTeX環境
  - -shell-escapeオプション付きでのコンパイル

- Python3
  - pip install toml

## How to use

### template.tex
頑張って読んで好きな設定にしてください.  
34行目付近の```\lhead```のところでヘッダの左側にチーム名を載せることができる.  
「%%%INSERT HERE%%%」と書かれている行にライブラリのファイルが挿入される.

### library.toml

toml形式でどのファイルからPDFを作りたいか指定する  

####  書式
```toml
[[library]]
category = "Math"

	[[library.file]]
	name = "行列"
	path = "lib/Math/Matrix/Matrix.cpp"

[[library]]
category = "Data Structure"

	[[library.dir]]
	name = "SegmentTree/"
	path = "lib/Tree/SegmentTree"

	[[library.file]]
	name = "SparseTable"
	path = "lib/DataStructure/SparseTable.cpp"
```

みたいな感じ  
```[[library]]```でcategoryを書いて、その下にそのカテゴリのファイルを```[[library.file]]```で並べる.  
```[[library.file]]```の情報は```name```と```path```.  
```[[library.dir]]```をすると```path```で指定したディレクトリの直下にあるcppファイルを使い、```name```とファイル名をそのまま連結したものがタイトルみたいになる。区切り文字は自分でつけないとそのままつながってしまうので気をつけて。
パスは実行する場所からの相対パスか絶対パスを指定すること.

## Run

```sh
python generate.py --template "ベースになるTeXファイル" --library "上のように記述したTOMLファイル" --output "結果として出力するTeXファイル"
```

できたTeXファイルのコンパイルは頑張ってください

## Example

https://github.com/maze1230/Library-TeX-Generator/blob/master/sample/lib.pdf
