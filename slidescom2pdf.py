from pathlib import Path
import time
import img2pdf

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

SLIDE_SIZE = (1280, 960)
TMP_DIR = 'tmp'


def get_slides_ss(deck_link):
    ss_dir = TMP_DIR
    driver = webdriver.Chrome(service=Service('chromedriver.exe'))
    driver.set_window_size(*SLIDE_SIZE)

    driver.get(deck_link)
    time.sleep(5)

    ss_idx = 0
    while True:
        time.sleep(2)
        ss_fname = '{:04d}.png'.format(ss_idx)
        driver.save_screenshot(str(Path(ss_dir) / ss_fname))
        right_arrow = driver.find_element(by=By.CLASS_NAME, value='navigate-down')
        down_arrow = driver.find_element(by=By.CLASS_NAME, value='navigate-right')
        if right_arrow.is_enabled():
            right_arrow.click()
            print('Wrote: {}'.format(ss_fname))
            ss_idx += 1
            continue
        elif down_arrow.is_enabled():
            down_arrow.click()
            print('Wrote: {}'.format(ss_fname))
            ss_idx += 1
            continue
        else:
            break
    return ss_idx


def make_tmp_dir(ss_dir):
    if Path(ss_dir).exists():
        for old_file in Path(ss_dir).glob('*'):
            if old_file.is_file():
                old_file.unlink()
    else:
        Path(ss_dir).mkdir()


def main():
    deck_link = 'https://slides.com/afonasev/fintech-2022-python-2/fullscreen'
    output_name = 'output.pdf'

    make_tmp_dir(TMP_DIR)
    get_slides_ss(deck_link)

    filenames = list(map(lambda x: str(x), Path(TMP_DIR).glob('*.png')))
    pdf = img2pdf.convert(filenames)
    with open(output_name, 'wb') as f:
        f.write(pdf)


if __name__ == '__main__':
    main()
