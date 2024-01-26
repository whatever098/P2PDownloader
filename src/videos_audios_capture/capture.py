import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def capture(url, path):
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return False

    page_content = response.text
    soup = BeautifulSoup(page_content, 'html.parser')

    # 获取所有<a>标签的href属性
    all_links = [link['href'] for link in soup.find_all('a', href=True)]

    # 根据链接的扩展名筛选视频链接
    video_links = [link for link in all_links if link.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))]

    # 根据链接的扩展名筛选音频链接
    audio_links = [link for link in all_links if link.lower().endswith(('.mp3', '.wav', '.ogg'))]

    # 下载视频和音频
    for video_link in video_links:
        try:
            # 将视频链接转换为绝对链接
            video_url = urljoin(url, video_link)
            video_response = requests.get(video_url, headers=headers)
            # 获取链接的文件名作为保存文件名
            filename = os.path.basename(video_url)
            with open(os.path.join(path, filename), 'wb') as f:
                f.write(video_response.content)
        except Exception:
            print("Some error occurred, maybe you should try again!")

    for audio_link in audio_links:
        try:
            # 将音频链接转换为绝对链接
            audio_url = urljoin(url, audio_link)
            audio_response = requests.get(audio_url, headers=headers)
            # 获取链接的文件名作为保存文件名
            filename = os.path.basename(audio_url)
            with open(os.path.join(path, filename), 'wb') as f:
                f.write(audio_response.content)
        except Exception:
            print("Some error occurred, maybe you should try again!")

    return True
