## JSON Line Utility

Python 2.7+

`process_files(file_dir, out_file_path)` transforms all `.pdf` and `.htm` files in a `file_dir` to text and then consolidates them in a compressed jsonl, specified by `out_file_path`.

Call from python:

``` python
import jsonio
jsonio.process_files('test_data', 'output/docs.jsonl.gz')
jsonio.process_files('test_data', 'output/docs.jsonl.gz')
```

or from command line:

``` bash
python jsonio.py 'train_data' 'output/train.jsonl.gz'
python jsonio.py 'test_data' 'output/test.jsonl.gz'
```

Class `Jsonliter` used for iterating over jsonl file.

``` python
import jsonio
docs = jsonio.Jsonliter('output/docs.jsonl.gz', 'output/docs.jsonl.gz')

train_x, train_y = docs.train_iter()
model.fit(x, y)
```
