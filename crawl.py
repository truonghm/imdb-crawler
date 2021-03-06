from src.crawler.movie import BulkMovieCrawler, MovieCrawler, MovieListCrawler
from src.crawler.rating import BulkRatingCrawler, RatingCrawler
from src.crawler.filmo import (
    BulkFilmoCrawler,
    StarFilmoCrawler,
    WriterFilmoCrawler,
    DirectorFilmoCrawler,
)
from src.crawler.cpi import crawl_cpi
from src.config import Setting
from src.transform.db_input import transform_actors, transform_writers, transform_directors, transform_stars

# from src.crawler import write_to_cache
import json
import time
import sys
import pandas as pd
import getopt
import logging
from pathlib import Path


# Create logging folder
Path("logs").mkdir(exist_ok=True)
Path("caches").mkdir(exist_ok=True)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler("logs/crawler_log.log")
# formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


def get_args():
    page = 'all'
    stop_at = None

    opts, args = getopt.getopt(sys.argv[1:], shortopts="p:sa", longopts=["page=", "stop_at="])

    if len(opts) > 0:
        for opt, arg in opts:
            if opt in ["-p","--page"]:
                page = arg
            elif opt in ["-sa","--stop_at"]:
                if arg.isnumeric():
                    stop_at = int(arg)

    return page, stop_at

def crawl_movies(stop_at: int = None):
    crawler = BulkMovieCrawler(load_from_cache=True, stop_at=stop_at)
    res = crawler.bulk_craw(
        MovieCrawler, write_to_cache=True, file_name=Setting.MOVIE_CACHE
    )

    directors_df = transform_directors(res)
    actors_df = transform_actors(res)
    writers_df = transform_writers(res)
    stars_df = transform_stars(res)

    directors_df.to_csv(Setting.DIRECTORS_CACHE, index=False)
    print(Setting.DIRECTORS_CACHE)
    actors_df.to_csv(Setting.ACTORS_CACHE, index=False)
    print(Setting.ACTORS_CACHE)
    writers_df.to_csv(Setting.WRITERS_CACHE, index=False)
    print(Setting.WRITERS_CACHE)
    stars_df.to_csv(Setting.STARS_CACHE, index=False)
    print(Setting.STARS_CACHE)


def crawl_ratings(stop_at: int = None):
    crawler = BulkRatingCrawler(load_from_cache=True, stop_at=stop_at)
    res = crawler.bulk_craw(
        RatingCrawler,
        write_to_cache=True,
        file_name=[Setting.RATING_DIST_CACHE, Setting.RATING_DEMO_CACHE],
    )


def crawl_movie_list():
    crawler = MovieListCrawler("/chart/top")
    res = crawler.crawl(write_to_cache=True, file_name=Setting.MOVIE_LIST_CACHE)


def crawl_actor_filmo(stop_at: int = None):
    crawler = BulkFilmoCrawler(job_type="actor", load_from_cache=True, stop_at=stop_at)
    res = crawler.bulk_craw(
        StarFilmoCrawler, write_to_cache=True, file_name=Setting.STAR_FILMO_CACHE
    )


def crawl_director_filmo(stop_at: int = None):
    crawler = BulkFilmoCrawler(
        job_type="director", load_from_cache=True, stop_at=stop_at
    )
    res = crawler.bulk_craw(
        DirectorFilmoCrawler,
        write_to_cache=True,
        file_name=Setting.DIRECTOR_FILMO_CACHE,
    )


def crawl_writer_filmo(stop_at: int = None):
    crawler = BulkFilmoCrawler(job_type="writer", load_from_cache=True, stop_at=stop_at)
    res = crawler.bulk_craw(
        WriterFilmoCrawler, write_to_cache=True, file_name=Setting.WRITER_FILMO_CACHE
    )


if __name__ == "__main__":

    start = time.time()

    # try:
    #     arg = sys.argv[1]

    #     if arg == "movie":
    #         crawl_movies()

    #     elif arg == "rating":
    #         crawl_ratings()

    #     elif arg == "movie_list":
    #         crawl_movie_list()

    #     elif arg == "actor_filmo":
    #         crawl_actor_filmo()

    #     elif arg == "director_filmo":
    #         crawl_director_filmo()

    #     elif arg == "writer_filmo":
    #         crawl_writer_filmo()

    #     elif arg == "filmo":
    #         crawl_actor_filmo()
    #         crawl_director_filmo()
    #         crawl_writer_filmo()
        
    #     elif arg == "cpi":
    #         crawl_cpi()

    #     elif arg == "all":
    #         print("Start crawling movies")
    #         crawl_movies()
    #         print("Start crawling ratings")
    #         crawl_ratings()
    #         print("Start crawling actor filmography")
    #         crawl_actor_filmo()
    #         print("Start crawling director filmography")
    #         crawl_director_filmo()
    #         print("Start crawling writer filmography")
    #         crawl_writer_filmo()
    #         print("Start crawling CPI data")
    #         crawl_cpi()
    #     else:
    #         raise ValueError("Invalid input")

    # except IndexError:
    #     print("Start crawling movies")
    #     crawl_movies()
    #     print("Start crawling ratings")
    #     crawl_ratings()
    #     print("Start crawling actor filmography")
    #     crawl_actor_filmo()
    #     print("Start crawling director filmography")
    #     crawl_director_filmo()
    #     print("Start crawling writer filmography")
    #     crawl_writer_filmo()
    #     print("Start crawling CPI data")
    #     crawl_cpi()

    page, stop_at = get_args()
    try:
        if page == "movie":
            crawl_movies(stop_at=stop_at)

        elif page == "rating":
            crawl_ratings(stop_at=stop_at)

        elif page == "movie_list":
            crawl_movie_list(stop_at=stop_at)

        elif page == "actor_filmo":
            crawl_actor_filmo(stop_at=stop_at)

        elif page == "director_filmo":
            crawl_director_filmo(stop_at=stop_at)

        elif page == "writer_filmo":
            crawl_writer_filmo(stop_at=stop_at)

        elif page == "filmo":
            crawl_actor_filmo(stop_at=stop_at)
            crawl_director_filmo(stop_at=stop_at)
            crawl_writer_filmo(stop_at=stop_at)
        
        elif page == "cpi":
            crawl_cpi()

        elif page == "all":
            print("Start crawling movies")
            crawl_movies(stop_at=stop_at)
            print("Start crawling ratings")
            crawl_ratings(stop_at=stop_at)
            print("Start crawling actor filmography")
            crawl_actor_filmo(stop_at=stop_at)
            print("Start crawling director filmography")
            crawl_director_filmo(stop_at=stop_at)
            print("Start crawling writer filmography")
            crawl_writer_filmo(stop_at=stop_at)
            print("Start crawling CPI data")
            crawl_cpi()
        else:
            raise ValueError("Invalid input")

    finally:
        print("Runtime: ", time.time() - start, "seconds")
        print("Done")
