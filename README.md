<h1 align="center">KTU Result Downloader</h1>
<div align="center">
  <p>A python script to download ktu exam result as pdf.
Written as part of learning python.</p>
</div>
<br/>

## 🚧 Requirements

* Python
* Git

## 🤔 Why ?

When ktu publishes result usually their servers are overloaded to the point its almost impossible to view result for several hours. 

This script will try to download the result and it will keep trying until it's been downloaded. so no need to refresh the pages !

## 🛠 Common setup

1. Clone the repo.

```bash
git clone https://github.com/Anoop1507/ktu_results_downloader
```

2. Enter into the folder and install the script.

```bash
cd ktu_results_downloader
sudo pip install -r requirements.txt
```

## 💻 Run

To run the program in your computer type the following command in the terminal.

python3 ktu_results_downloader.py -s[semester no.] -u[username] -p[password] -t[timeout in seconds(default 7)] -o[dir]

### Example

```bash
python3 ktu_results_downloader.py -s 3 -u MYUSERNAME -p PASSWORD -t 10 
```

## 😎 Author

[Anoop](https://github.com/Anoop1507)
