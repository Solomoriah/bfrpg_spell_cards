#!/usr/local/bin/python

"""
Convert svg files to pdf. Optionally, multiple pdf files may be merged into a single file.
Requires inkscape to be installed and in the path.

Usage: svg2pdf.py [--outdir=<dir>] [--dpi=<dpi>] [--strict] <svg>...
       svg2pdf.py [--outdir=<dir>] [--dpi=<dpi>] [--strict] [--merge --file=<file>] <svg>...

Options:
  --outdir <dir>, -o <dir>  Output directory for pdf files (will be created if it doesn't exist). [default: .]
  --file <file>  Name of pdf file for merged output.
  --merge, -m  Merge all generated pdf files into <file>.
  --strict  Stop if conversion errors are encountered. The default is to convert as many input files as possible.
  --dpi <dpi>  Resolution to use when rasterising filter effects. [default: 96]
"""

import os
import PyPDF2
import re
import subprocess
import sys
from docopt import docopt

opts = docopt(__doc__)

## Convert svg files to pdf with inkscape
os.makedirs(opts["--outdir"], exist_ok=True)
pdf_files = []
for filename in opts["<svg>"]:
    out_name = os.path.basename(filename)
    out_name = opts["--outdir"] + '/' + re.sub("\\.svg$", ".pdf", out_name)
    command = "inkscape --without-gui --export-pdf=" + out_name + " --file=" + filename + " --export-dpi=" + opts["--dpi"]
    try:
        completed = subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("stdout:", str(e.stdout))
        print("stderr:", str(e.stderr))
        if opts["--strict"]: raise
    pdf_files.append(out_name)

## merge all pdfs
if opts["--merge"]:
    os.makedirs(os.path.dirname(opts["--file"]), exist_ok=True)
    merger = PyPDF2.PdfFileMerger()
    for filename in pdf_files:
        merger.append(filename)
    merger.write(opts["--file"])


    
