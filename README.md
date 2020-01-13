Install [dashing 0.4.0](https://github.com/technosophos/dashing).

You'll then need to create a case sensitive volume to work from, as TensorFlow
has files that only differ by case. You can follow [this guide](https://coderwall.com/p/mgi8ja/case-sensitive-git-in-mac-os-x-like-a-pro) for example.

Then, inside the case sensitive volume:

```bash
$ git clone https://github.com/reuben/gen_tf_docset
$ cd gen_tf_docset
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -U setuptools wheel pip pygments misaka
$ git clone --depth 1 --branch r1.15 https://github.com/tensorflow/docs tf-docs
$ python gen.py tf-docs/site/en/api_docs/python out_dir
$ pygmentize -S default -f html > out_dir/style.css
$ cp dashing.json icon*.png out_dir
$ cd out_dir
$ dashing build
```

This should generate a `TensorFlow.docset` folder inside `out_dir`.
