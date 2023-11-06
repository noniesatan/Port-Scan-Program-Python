# import win32evtlogutil
#
#
# def report_EV(mylist, eventtype):
#     IP_EVT_APP_NAME = " CheckIPPort - IP-Port Scan Application"
#     IP_EVT_ID = 7040
#     IP_EVT_CATEG = 9876
#     IP_EVT_TYPE = win32evtlog.EVENTLOG_WARNING_TYPE  # WARNING=2
#     IP_EVT_ERR = win32evtlog.EVENTLOG_ERROR_TYPE  # ERROR=1
#     IP_EVT_STRS = mylist
#     IP_EVT_DATA = b"Scan IP Address Event Data"
#     win32evtlogutil.ReportEvent(IP_EVT_APP_NAME, \
#                                 IP_EVT_ID, \
#                                 eventCategory=IP_EVT_CATEG, \
#                                 eventType=eventtype, \
#                                 strings=IP_EVT_STRS, \
#                                 data=IP_EVT_DATA)
#
#
# report_EV(ip_list,2)
# ip_list = {'192.168.1.1'.'192.168.1.3'}