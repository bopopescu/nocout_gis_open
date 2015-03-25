import os
from downloader.models import Downloader
from nocout.settings import MEDIA_ROOT
from celery.task import task
from django.contrib.auth.models import User
from django.http import HttpRequest
from datetime import datetime
import xlwt
import simplejson

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@task
def get_datatable_response(payload):
    """
        Generating excel for datatable
        Parameters:
            - payload (dict) - payload data for e.g.
                                {
                                    'username': u'priyesh',
                                    'rows': u'LivePerformanceListing',
                                    'app': u'performance',
                                    'object_id': 3L,
                                    'headers': u'Live_Performance',
                                    'rows_data': {
                                        'data_tab': 'P2P',
                                        'page_type': 'customer',
                                        'download_excel': 'yes'
                                    },
                                    'fulltime': '2015-03-23-17-07-35',
                                    'headers_data': {
                                        'data_tab': 'P2P',
                                        'page_type': 'customer',
                                        'download_excel': 'yes'
                                    }
                                }

        URL:
           - "/downloader/datatable/?app=performance&headers=Live_Performance&rows=LivePerformanceListing&
               headers_data={'page_type': 'customer', 'data_tab': 'P2P', 'download_excel': 'yes' }&
               rows_data={'page_type': 'customer', 'data_tab': 'P2P', 'download_excel': 'yes' }"

    """

    # get downloader object
    d_obj = None
    try:
        d_obj = Downloader.objects.get(id=payload['object_id'])
    except Exception as e:
        pass

    if all([key in payload for key in ["app", "rows", "headers"]]):
        # current user object
        user = User.objects.get(username=payload['username'])

        # import headers class
        exec "from {}.views import {}".format(payload['app'], payload['headers']) in globals(), locals()

        # import rows data class
        exec "from {}.views import {}".format(payload['app'], payload['rows']) in globals(), locals()

        # ********************************** CREATE HEADERS REQUEST (START) **********************************

        # create http request for getting rows data (for accessing list view classes)
        headers_req = HttpRequest()

        # binding data to headers request
        if payload:
            headers_req.GET = payload['headers_data']

        # create request attribute for http request
        headers_req.REQUEST = payload['headers_data']

        # bind current user with http request
        headers_req.user = user

        # *********************************** CREATE HEADERS REQUEST (END) ***********************************

        # ************************************ CREATE ROWS REQUEST (START) ***********************************

        # create http request for getting rows data (for accessing list view classes)
        rows_req = HttpRequest()

        # binding data to rows request
        if payload:
            rows_req.GET = payload['rows_data']

        # create request attribute for http request
        rows_req.REQUEST = payload['rows_data']
        rows_req.REQUEST['iDisplayStart'] = 0

        # bind current user with http request
        rows_req.user = user

        # ************************************ CREATE ROWS REQUEST (END) ************************************

        # create view class object (for headers data)
        headers_req_obj = eval("{}()".format(payload['headers']))
        headers_req_obj.request = headers_req
        headers_req_obj.object_list = []
        headers_req_obj.kwargs = payload['headers_data']

        # get headers
        headers_data = headers_req_obj.get_context_data()

        # fetch headers
        headers_list = ""
        file_headers_list = ""
        try:
            headers_list = list()
            file_headers_list = list()
            datatable_headers = simplejson.loads(headers_data['datatable_headers'])
            for headers_dict in datatable_headers:
                if 'sClass' in headers_dict:
                    if headers_dict['sClass'] != 'hide':
                        headers_list.append(headers_dict['mData'])
                        file_headers_list.append(headers_dict['sTitle'])
        except Exception as e:
            logger.error(e.message)

        # create view class object (for rows data)
        rows_req_obj = eval("{}()".format(payload['rows']))
        rows_req_obj.request = rows_req
        rows_req_obj.kwargs = payload['rows']

        # get datatable data
        query_set_length = len(rows_req_obj.get_initial_queryset())

        rows_req.REQUEST['iDisplayLength'] = query_set_length
        rows_req_obj.max_display_length = query_set_length
        result = rows_req_obj.get_context_data()

        # error rows list
        rows_list = []

        # headers for excel sheet
        if result['aaData']:
            headers = headers_list
            if headers:
                # create list of lists containing excel rows data (except header)
                for val in result['aaData']:
                    temp_list = list()
                    for key in headers:
                        try:
                            temp_list.append(val[key])
                        except Exception as e:
                            temp_list.append("")
                            logger.info(e.message)
                    rows_list.append(temp_list)

                # excel workbook
                wb = xlwt.Workbook()

                # excel worksheet
                ws = wb.add_sheet('Sheet 1')

                # xlwt style object for styling header row
                style = xlwt.easyxf('pattern: pattern solid, fore_colour tan;')

                # writing header row to excel sheet
                try:
                    for i, col in enumerate(file_headers_list):
                        ws.write(0, i, col.decode('utf-8', 'ignore').strip(), style)
                except Exception as e:
                    pass

                # writing rows (except header) in excel sheet
                try:
                    for i, l in enumerate(rows_list):
                        i += 1
                        for j, col in enumerate(l):
                            ws.write(i, j, col)
                except Exception as e:
                    pass

                # if directory for bulk upload excel sheets didn't exist than create one
                if not os.path.exists(MEDIA_ROOT + 'download_excels'):
                    os.makedirs(MEDIA_ROOT + 'download_excels')

                # saving bulk upload errors excel sheet
                try:
                    # file path
                    file_path = 'download_excels/{}_{}_{}.xls'.format(payload['app'], payload['username'], payload['fulltime'])

                    # saving workbook
                    wb.save(MEDIA_ROOT + file_path)
                    # update downloader object (on success)
                    d_obj.file_path = file_path
                    d_obj.file_type = 'MS-Excel'
                    d_obj.status = 1
                    d_obj.description += "\nSuccessfully downloaded on {}.".format(payload['fulltime'])
                    d_obj.request_completion_on = datetime.now()
                    d_obj.save()
                except Exception as e:
                    # update downloader object
                    d_obj.status = 2
                    d_obj.request_completion_on = datetime.now()
                    d_obj.save()
                    logger.info(e.message)
        else:
            # update downloader object (on success)
            d_obj.description += "\nData table has no data."
            d_obj.request_completion_on = datetime.now()
            d_obj.save()
    else:
        # update downloader object (on success)
        d_obj.description += "\nWrong parameters."
        d_obj.request_completion_on = datetime.now()
        d_obj.save()