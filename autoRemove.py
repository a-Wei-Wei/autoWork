import os
import re
import logging
import time
import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

fp = logging.FileHandler("runtime.log", encoding='utf-8')
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO, datefmt=DATE_FORMAT, handlers=[fp])


def execute_fun():
    patter = re.compile(r'launch([\s\S]*).ica')
    current_files = os.listdir(".")

    for single_file in current_files:
        if patter.match(single_file) is not None:
            if os.path.exists("./" + single_file):
                os.remove("./" + single_file)
            else:
                # print("not found %s" % single_file)
                logging.info("not found %s" % single_file)
    # print("all had clear............")
    logging.info("all had clear............")


def schedule_job():
    count = 0
    patter = re.compile(r'launch([\s\S]*).ica')
    current_files = os.listdir(".")
    logging.info("当前目录为： " + str(os.getcwd()))
    for single_file in current_files:
        if patter.match(single_file) is not None:
            count += 1
    if count >= 10:
        # print("launch.ica 数量达到上限， 调用删除。。。")
        logging.info("launch.ica 数量达到上限， 调用删除。。。")
        execute_fun()
    else:
        # print("当前launch.ica 数量为 %s 未达到上限" % count)
        logging.info("扫描当前目录下 launch.ica 数量为 %s ，未达到上限" % count)


def create_block_scheduler():
    scheduler = BlockingScheduler()
    # 定义时间 days， 意思就是 在三天之后就开始运行
    trigger = IntervalTrigger(hours=10)
    scheduler.add_job(schedule_job, trigger)
    scheduler.start()


def create_background_scheduler():
    scheduler = BackgroundScheduler()
    trigger = IntervalTrigger(hours=10)
    scheduler.add_job(schedule_job, trigger)
    scheduler.start()


if __name__ == '__main__':
    # execute_fun()
    # os.system("pause")
    # block scheduler 运行在主线程上，如果主线程有其他任务，就会被阻塞
    logging.info("运行中，每10个小时将进行清理launch.ica。")
    create_block_scheduler()
    # create_background_scheduler() 这是需要依赖主线程运行，意思就是 不主塞主线程，后台运行，但是主线程结束，这个定时任务也结束
    # while True:
    #     time.sleep(10)
    #     print("main thread..........")
