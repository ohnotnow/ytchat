import os
import time
import argparse
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from yaspin import yaspin

@yaspin(text="Waiting on GPT")
def get_assistant_response(client, thread, run):
    answer = ""
    while not answer:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            answer = messages.data[0].content[0].text.value
        else:
            time.sleep(1)
    return answer

@yaspin(text="Creating GPT run")
def create_run(client, thread, assistant_id, file_id, prompt):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
        file_ids=[file_id]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    return run

@yaspin(text="Getting video transcript")
def get_text_from_youtube(url: str, fallback_audio=False) -> str:
    video_id = url.split('watch?v=')[-1]
    text = ""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        text = " ".join([i['text'] for i in transcript.fetch()])
    except:
        print(f"Could not get transcript for {url}")
        exit(1)

    return text

def main():
    parser = argparse.ArgumentParser(description='Process some URL.')
    parser.add_argument('url', type=str, help='The YouTube URL to process')
    args = parser.parse_args()

    url = args.url

    summary = '';

    text = get_text_from_youtube(url)
    with open('transcript.txt', 'w') as f:
        f.write(text)
    client = OpenAI()
    file = client.files.create(
        file=open("transcript.txt", "rb"),
        purpose="assistants"
    )
    thread = client.beta.threads.create()
    assistant_id = os.getenv('YTCHAT_ASSISTANT_ID')
    run = create_run(client, thread, assistant_id, file.id, "Can you summarise the following video transcript for me?")
    summary = get_assistant_response(client, thread, run)
    print(f"\n\n## Summary\n\n{summary}\n\n")
    while True:
        question = input("Ask a further question?\n")
        if question:
            run = create_run(client, thread, assistant_id, file.id, question)
            answer = get_assistant_response(client, thread, run)
            print(f"\n\n## GPT\n\n{answer}\n\n")
        else:
            print("Goodbye!")
            exit(0)

if __name__ == '__main__':
    main()
