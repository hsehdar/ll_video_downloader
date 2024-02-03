# ll_video_downloader
Follow below steps to setup environment and download videos. Ensure you use appropriate path of your system in each command below.
* Clone this repository (read steps from Github).
* Setup the environment using **Command Prompt** or **bash**.
   * Windows: `python -m pip install %UserProfile%\ll_video_downloads`
   * Linux: `python -m pip install ${HOME}/ll_video_downloads`
* Set Chrome path to the environment variable.
   * Windows: `set PATH="%PATH%;C:\Program Files\google\chrome"`
   * Linux: `PATH=$PATH:/opt/google/chrome; export PATH`
* Activate Python environment.
   * Windows: `%UserProfile%\ll_video_downloads\bin\activate.ps1`
   * Linux: `source ${HOME}/ll_video_downloads/bin/activate`
* Change directory to *ll_video_downloads* using `cd` command.
* Install Python dependencies `pip install -r requirements.txt`.
* Edit _setup.py_ and _download_videos.py_ to update `chrome_data_dir` for storing Chrome related files and `download_videos.py` for storing downloaded videos. Ensure you use PATH style as per Python requirements.
* Log in to LinkedIn `python setup.py`
* Edit _download_videos.py_ to update `linkedin_learning_url`.
* Download videos `python download_videos.py`