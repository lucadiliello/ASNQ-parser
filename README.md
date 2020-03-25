# ASNQ-parser
Parse the `ANSQ` dataset to generate samples in a given format.

## Usage
Place the train and dev files of `ANSQ` in the data folder. Generate splits with
```bash
python main.py -i data/<input file> -o <output folder> -s 50 50
```
To divide the `<input file>` in two splits of size `50%` and `50%` and place results in <output folder>.

### Other parameters
- `-f`: overwrite output folder if it exists
- `--delimiter`: use given delimiter on input file rows, otherwise it will be automatically inferred
- `--shuffle`: shuffle dataset before splitting
- `--seed`: use this seed when shuffling
- `--as-true`: which labels should be considered as true, others will be considered as false

Enjoy