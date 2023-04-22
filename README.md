# Google Image Downloader

This is a simple python script to download images from Google Images. It uses the Google Custom Search API to search for images and download them. It is a command line tool and can be used to download images for a particular search query.

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

### API Key
You need to get a SerpAPI API key from [here](https://serpapi.com/manage-api-key). You can get 100 free searches per day. You can also get a free trial for 100 searches per day. You can also get a paid plan if you need more searches per day.

After getting the API key, set an environment variable `SERPAPI_KEY` with the API key.
```bash
export SERPAPI_KEY="your-api-key"
```
### Command Line Arguments

```
Usage: main.py [OPTIONS]

Options:
  -s, --search TEXT     Search term  [required]
  -n, --number INTEGER  Number of images to download
  --help                Show this message and exit.
```