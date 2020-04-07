# google-images-downloader

A command-line Python application which can download Google images based on a key phrase, with optional parameters to prune the images returned.

Team Name: CAS Dream Team

Team Members: Joshua Guinness (@guinnesj), Sam Crawford (@crawfs1), Nicholas Mari (@marin)

This project is a reimplementation of: https://github.com/hardikvasa/google-images-download

## User Guide

### Installation

Running the following commands will download the repository into the directory you run the terminal from, and will install all dependencies and libraries required to run the program.
```bash
git clone https://gitlab.cas.mcmaster.ca/guinnesj/google-images-downloader
cd google-images-downloader/src
make install
```

### Usage
To use, run the command `python Main.py -k <keyword>`, where `python` is the command for running Python on your system, and `<keyword>` is the keyword to use for searching Google for the images to download. This is the minimum input required to run the program; all valid parameters are given below, and a full list of options can be accessed by just running `python Main.py` without the keyword argument.

#### Input Parameters

Parameter |Abbr. |Description |Example
---|---|---|---
keyword* |k| The keyword to search Google Images with |"software"
limit** |l| The maximum number of images to download |10
safesearch |ss| Whether or not to enable SafeSearch |N/A
filetype |ft| The file type of images to download |"gif"
directory |d| The directory to save images to |a path to a directory
colour |c| The colour of images to download |"teal"
license |li| The license of images to download |"labeled-for-reuse"
imagetype |t| The type of images to download |"clipart"
imageage |a| The age of images to download| "past-year"
aspectratio |ar| The aspect ratio of images to download |"square"
imagesize |is| The size of images to download |">2MP"
serverhost |s| The host of the server to download images to |"moore.mcmaster.ca"
serverusername |u| The username to log in to the given server |the user’s MacID
serverpassword |p| The password to log in to the given server |the user’s Moore password
region |rg| The geographical location of images to download |"Canada"
whitelist |wl| The website to download images from| "mcmaster.ca"
blacklist |bl| The website to exclude image download from |"mcmaster.ca"
fromfile |ff| The file to parse input arguments from |a path to a file

\*`keyword` is a required parameter to run the program.
\*\*The default value of `limit` is 10.

### Advanced Usage
When in the `src/` folder, you can test the program by running `make test` and generate doxygen documentation by running `make docs`.
