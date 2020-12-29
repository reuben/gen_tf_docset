Install [dashing 0.4.0](https://github.com/technosophos/dashing).

You'll then need to create a case sensitive volume to work from, as TensorFlow
has files that only differ by case. You can follow [this guide](https://coderwall.com/p/mgi8ja/case-sensitive-git-in-mac-os-x-like-a-pro) for example.

Then, inside the case sensitive volume:

```bash
$ git clone https://github.com/reuben/gen_tf_docset
$ cd gen_tf_docset
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -U setuptools wheel pip pygments misaka git+https://github.com/tensorflow/docs
$ git clone --depth 1 --branch r2.4 https://github.com/tensorflow/tensorflow
$ pushd tensorflow/tensorflow/tools/docs
$ python generate2.py --code_url_prefix "https://github.com/tensorflow/tensorflow/blob/v2.4.0/tensorflow/" --output_dir=../../../../tf_generated_docs
$ popd
$ python gen.py tf_generated_docs out_dir
$ cp dashing.json icon*.png style.css out_dir
$ pygmentize -S default -f html >> out_dir/style.css
$ sed -E 's/href="([^"]+)\.md"/href="\1.html"/g' out_dir/tf.html > out_dir/index.html
$ rm out_dir/tf.html
$ find out_dir/tf -type f -exec sed -i '' -E 's/href="([^"]+)\.md"/href="\1.html"/g' {} \;
$ # With GNU sed, use sed -iE (macOS sed requires the empty string to avoid saving backups)
$ cd out_dir
$ dashing build
```

This should generate a `TensorFlow 2.docset` folder inside `out_dir`.
