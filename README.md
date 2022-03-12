# Picture Sort

A Python script to finally sort this pictures from my 2006 holidays.

See your pictures one by one, and choose right/left for keep/discard, print/hide forever... Kind of like Tinder, but with your own pictures.

## Install

```sh
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Run

```sh
python picture-sort.py /path/to/my/pictures
```

Available options

```txt
  -h, --help            show this help message and exit
  --left LEFTDIR, -l LEFTDIR
                        Custom name of the directory for <Arrow-Left> (or <Space>) key (eg. "bad", "throw"...). Defaults to "left"
  --right RIGHTDIR, -r RIGHTDIR
                        Custom name of the directory for <Arrow-Right> (or <Enter>) key (eg. "good", "keep"...). Defaults to "right"
```
