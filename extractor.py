# coding: utf-8

from pixivpy3 import *
import argparse
import time


def search_specific_tagged_works(aapi, pixiv_id, tag="R-18", work_type="illust"):

    specific_tagged_works_information_list = []
    json_result = aapi.user_illusts(pixiv_id, type=work_type)

    # get all works' information
    while True:
        for i in range(0, len(json_result.illusts)):
            information = _get_specific_tagged_works_information(json_result.illusts[i], tag)
            if information is not None:
                specific_tagged_works_information_list.append(information)

        next_qs = aapi.parse_qs(json_result.next_url)
        if next_qs is None:
            break

        json_result = aapi.user_illusts(**next_qs)

    return specific_tagged_works_information_list


def _get_specific_tagged_works_information(illusts_information, tag):
    if {"name": tag} in illusts_information.tags:
        return illusts_information
    else:
        return None


def download_works(aapi, works_information, download_dir):

    for work in works_information:
        aapi.download(work.image_urls.large, download_dir)
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="pixiv user id")
    parser.add_argument("password", help="pixiv password")
    parser.add_argument("artist_profile_page_url", help="url for artist's pixiv profile page")
    args = parser.parse_args()

    # app-api
    aapi = AppPixivAPI()
    aapi.login(args.user_id, args.password)

    artist_pixiv_id = int(args.artist_profile_page_url.replace("https://www.pixiv.net/member.php?id=", ""))

    # get specific tagged works(illusts and mangas) information
    specific_tagged_works_information_list = []
    illust_information_list = search_specific_tagged_works(aapi, artist_pixiv_id, work_type="illust")
    manga_information_list = search_specific_tagged_works(aapi, artist_pixiv_id, work_type="manga")

    specific_tagged_works_information_list.extend(illust_information_list)
    specific_tagged_works_information_list.extend(manga_information_list)

    download_works(aapi, specific_tagged_works_information_list, "./")


if __name__ == '__main__':
    main()
