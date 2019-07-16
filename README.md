Install [dashing](https://github.com/technosophos/dashing): 
`brew edit dashing`, then add a head entry for it at the top of the file with
the other metadata to be able to install the latest version:

```ruby
    head "https://github.com/technosophos/dashing.git"
```

Then `brew install dashing --HEAD`.

You'll then need to create a case sensitive volume to work from, as TensorFlow
has files that only differ by case. You can follow [this guide](https://coderwall.com/p/mgi8ja/case-sensitive-git-in-mac-os-x-like-a-pro) for example.

Then, inside the case sensitive volume, clone this repository, cd into it, and set up a new virtualenv.

Finally, follow these steps:

```bash
$ pip install pygments misaka
$ git clone --depth 1 --branch r1.14 https://github.com/tensorflow/docs tf-docs
$ python gen.py tf-docs/site/en/api_docs/python out_dir
$ pygmentize -S default -f html > out_dir/style.css
$ cp dashing.json icon*.png out_dir
$ cd out_dir
$ dashing build
```

This should generate a `TensorFlow.docset` folder inside `out_dir`.
