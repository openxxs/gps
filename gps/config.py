#! /usr/bin/env python
#coding=utf-8


class CONFIG(object):
	"""
	一些配置信息的保存，保存到这里比较方便
	"""
	GAMITTABLEPATH = '/home/usr/GAMIT/tables/'
	SOFTWAREPATH = '/home/liu/gps/gps/'
	RINEXPATH = '/home/usr/GPS/trunk/data/rinex/'
	#需要修改编辑的table目录下的配置文件，如果需要添加用%%隔开
	fileList = 'sestbl.%%sittbl.%%station.info%%process.defaults%%sites.defaults%%eq_rename%%globk_comb.cmd%%globk_vel.cmd'
	#需要跟踪下载更新状态的文件，如果需要添加请用%%隔开
	downloadList = 'rcvant.dat%%antmod.dat%%pmu.bull_a%%ut1.usno%%pole.usno%%leap.sec'
	#需要检查文件的站点，即****2020.11o的前四位，用%%隔开
	checklist = 'fjfq%%fjct%%fjdt%%fjgs'

	refStation = 'bjfs guam irkt kit3 lhaz pimo pol2 shao twtf tnml tskb urum wuhn'