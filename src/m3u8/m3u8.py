import concurrent.futures
import logging
import os
import subprocess
import threading
import time
from urllib.parse import urljoin

import requests

logging.basicConfig(level=logging.INFO)

download_mutex = threading.Lock()
successful_downloads = set()
start_time = 0


def download_m3u8(url):
    """
    下载url对应的m3u8视频
    :param url: m3u8 url
    :return: response（m3u8）
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch M3U8 playlist. Status code: {response.status_code}")


# Function to parse the M3U8 playlist and extract segment URLs
def parse_m3u8(m3u8_content, m3u8_url):
    """
    解析m3u8文件，得到.ts文件的请求url
    :param m3u8_content:
    :param m3u8_url:
    :return:
    """
    lines = m3u8_content.split('\n')
    # .ts文件的请求url
    segment_urls = [urljoin(m3u8_url, line.strip()) for line in lines if line and not line.startswith("#")]
    return segment_urls


def download_segment(segment_url, output_dir, index):
    """
    下载各个.ts文件
    :param segment_url:
    :param output_dir:
    :param index:
    :return:
    """
    max_retries = 10  # 最大请求次数
    retries = 0

    # 检测其他线程是否已经成功下载这个.ts文件，若是则返回
    with download_mutex:
        if index in successful_downloads:
            return

    while retries < max_retries:
        try:
            response = requests.get(segment_url, stream=True)
            if retries >= 1:
                print(f"Re-Request for segment: {index}")
            if response.status_code == 200:
                # 保存.ts文件到本地
                segment_filename = os.path.join(output_dir, f"segment_{index:04d}.ts")
                with open(segment_filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                    print(f"Downloading segment_{index:04d}.ts")

                # 标记已经下载成功
                with download_mutex:
                    successful_downloads.add(index)

                return
            else:
                print(f"Failed to download segment_{index:04d}.ts. Retrying...")
        except Exception as e:
            print(f"An error occurred while downloading segment_{index:04d}.ts: {str(e)}")

        retries += 1
        time.sleep(1)

    print(f"Failed to download segment_{index:04d}.ts after {max_retries} retries.")


def download_segments(segment_urls, output_dir):
    """
    下载所有的.ts文件
    :param segment_urls: ts url
    :param output_dir: 下载路径
    :return: none
    """
    os.makedirs(output_dir, exist_ok=True)
    total_segments = len(segment_urls)
    downloaded_segments = 0
    total_bytes = 0
    before_bytes = 0
    before_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_segment, url, output_dir, i): url for i, url in enumerate(segment_urls)}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                future.result()
                downloaded_segments += 1
                segment_size = os.path.getsize(os.path.join(output_dir, f"segment_{downloaded_segments - 1:04d}.ts"))
                total_bytes += segment_size

                # 计算进度以及下载速度
                progress = downloaded_segments / total_segments * 100

                downloaded_bytes = total_bytes - before_bytes
                downloaded_time = time.time() - before_time
                download_speed = 0
                if downloaded_time != 0:
                    download_speed = downloaded_bytes / downloaded_time
                show_speed = download_speed / 1024  # Current speed in KB/s

                print(
                    f"Downloaded {downloaded_segments}/{total_segments} segments - {progress:.2f}% complete ({show_speed:.2f} KB/s)",
                )

            except Exception as e:
                print(f"Downloading of {url} generated an exception: {str(e)}")


def merge_segments(output_dir, output_filename):
    """
    合并所有的.ts文件成一个m3u8视频
    :param output_dir:
    :param output_filename:
    :return:
    """
    ts_files = [os.path.join(output_dir, filename) for filename in os.listdir(output_dir) if filename.endswith(".ts")]
    try:
        cmd = [r'D:\study\pycharm\project\hust2021-software-engineering\src\m3u8\ffmpeg', '-i',
               'concat:' + '|'.join(ts_files), '-c', 'copy', output_filename]
        subprocess.run(cmd, check=True)
        print(f'Successfully merged {len(ts_files)} .ts files into {output_filename}')
    except subprocess.CalledProcessError as e:
        print(f'Error merging files: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
    clean_up(ts_files)
    print("All .ts files have been cleaned up!")
    print(f"Video saved as {output_filename}")


def clean_up(ts_files):
    try:
        for ts_file in ts_files:
            os.remove(ts_file)
    except Exception as e:
        print(f'An error occurred while cleaning up files: {e}')


def interface_ui(m3u8_url, output_dir, filename):
    """
    提供给UI界面的接口
    :param output_dir: 保存路径
    :param m3u8_url: m3u8_url
    :param filename: 保存文件名
    :return: none
    """
    m3u8_url = m3u8_url.replace("al-vod", "videotx-platform")
    output_filename = os.path.join(output_dir, filename)

    try:
        m3u8_content = requests.get(m3u8_url).text
        segment_urls = [urljoin(m3u8_url, line.strip()) for line in m3u8_content.split('\n') if
                        line and not line.startswith("#")]
        download_segments(segment_urls, output_dir)
        merge_segments(output_dir, output_filename)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
