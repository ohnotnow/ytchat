# ytchat

This is a Python script that uses the OpenAI API to generate a summary of a YouTube video transcript. It fetches the transcript of a given YouTube video, sends it to the OpenAI API, and prints out the generated summary.  You can then ask further questions about the transcript as needed without it having to refetch or resend the transcript.

## Prerequisites

- Python 3.11
- An OpenAI API key
- An OpenAI assistant ID (see https://platform.openai.com/docs/assistants/overview)

## Installation

1. Clone this repository:
```sh
git clone https://github.com/ohnotnow/ytchat.git
cd ytchat
```
2. Install the required Python packages:
```sh
pip install -r requirements.txt
```
## Usage
Run the script with a YouTube URL as an argument:
```sh
export YTCHAT_ASSISTANT_ID=asst_dUeK89O4......
python main.py 'https://www.youtube.com/watch?v=d10238d821q'
```
The script will fetch the transcript of the video, send it to the OpenAI API, and print out the generated summary.  You can then ask further questions about the content of the transcript.

## License
This project is licensed under the terms of the MIT license. See the License.md file for details.
