# import cStringIO
# import datetime
# import hashlib
# import logging
# import cloudstorage as gcs
# from sr.util import deferred
# import sr.config as settings
# from sr.util import blobstore as blobutil
# from sr.app.integrations import MaximsSftpDelivery, open_sftp
#
# MDD_EXTENSION_NAME = "mdd"
# TXT_EXTENSION_NAME = "txt"
# GCS_BUCKET = "sr-maxim-feed"
# CSV_CONTENT_TYPE = "text/csv"
# MDD_CONTENT_TYPE = "text/mdd"
# TXT_CONTENT_TYPE = "text/txt"
# TEMPLATE_ACTIVITY = "Yet_To_Be_Determined"
# MAXIM_SFTP_PUSH_PATH = "\\%s\\PointSoft\\FBpos\MDSync\\" % (
#     settings.MAXIMS_SFTP_FILE_IP
# )
# MAXIM_SFTP_PULL_PATH = "\\%s\\PointSoft\\FBpos\MDSync\\" % (
#     settings.MAXIMS_SFTP_FILE_IP
# )
#
# MAXIM_KEYS = {
#     "version": "VER",
#     "operation": "OP",
#     "device_id": "deviceID",
#     "remark": "remark",
#     "table_number": "tableNum",
#     "data_key": "dataKey",
#     "device_key": "deviceKey",
#     "ds": "ds",
#     "item_suspend_info": "itemSuspendInfo",
#     "auto_link": "autoLink",
#     "pax": "pax",
# }
#
# MAXIM_FUNCTION_CODES = {
#     "MDRegister": {"VER": "1.0", "OP": 1},
#     "MDLinkTable": {"VER": "1.0", "OP": 2},
#     "MDOpenTable": {"VER": "1.0", "OP": 6},
#     "MDLoadTable": {"VER": "1.0", "OP": 3},
#     "MDSaveTable": {"VER": "1.0", "OP": 4},
#     "GetSuspendItems": {"VER": "1.0", "OP": 8},
# }
#
# ds = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")[:-3]
# function_register = "MDRegister"
# function_link_table = "MDLinkTable"
# function_table_status = "TableStatus"
# function_open_table = "MDOpenTable"
# function_load_table = "MDLoadTable"
# function_save_table = "MDSaveTable"
# function_get_suspend_items = "GetSuspendItems"
#
#
# def _create_mdd_string(**kwargs):
#     """
#     Generate the mdd string from kwargs
#     :param kwargs: Dynamic list of variables to be converted to string
#     :return: encoded string
#     """
#     build_string = u""
#     for key, value in kwargs.items():
#         build_string += u"%s=%s\n" % (MAXIM_KEYS[key], value)
#     build_string += u"<<<"
#     encoded_string = build_string.encode("utf8")
#
#     return encoded_string
#
#
# def process_table_status(list_table_info):
#     """
#     Process Table Status and upload for Maxim Table Status function
#
#     :param list_table_info: List of Table information
#     :return:
#     """
#
#     pass
#
#
# def process_actual_for_registration(reference_code, table_id):
#     """
#     Process all the actual (Reservation Info)
#
#     :param actuals:
#     :return:
#     """
#     f = cStringIO.StringIO()
#     d = _create_registration_data(reference_code, table_id)
#     f.write(d)
#
#     file_name = "%s\%s-%s.%s" % (
#         MAXIM_SFTP_PUSH_PATH,
#         function_register,
#         ds,
#         MDD_EXTENSION_NAME,
#     )
#     _upload_sftp(f, file_name)
#
#
# def _create_registration_data(reference_code, table_id):
#     """
#     To create registration information for MDRegister Function
#
#     :param reference_code: reference code for actual
#     :param table_id: table id for actual
#     :return: string to be put in a file for upload
#     """
#
#     device_id = reference_code
#     data_key = _create_mdd_gen_key(function_register, device_id, ds)
#     encoded_string = _create_mdd_string(
#         version=MAXIM_FUNCTION_CODES["MDRegister"]["VER"],
#         operation=MAXIM_FUNCTION_CODES["MDRegister"]["OP"],
#         device_id=device_id,
#         remark=device_id,
#         table_number=table_id,
#         data_key=data_key,
#         ds=ds,
#     )
#     return encoded_string
#
#
# def _upload_sftp(sftp_file, file_name):
#     """
#
#     :param sftp_file: File data to be uploaded
#     :param file_name: File name to be used for storage
#     """
#     return MaximsSftpDelivery.deliver_file(sftp_file, file_name)
#
#
# def import_maxims_feed(venue_group_id):
#     pass
#
#
# def _get_available_filenames_from_sftp():
#     pass
#
#
# def _download_maxim_file(process_type, filename, content_type):
#     pass
#
#
# def _process_maxim_downloaded_file(filename, file_blobkey):
#     pass
#
#
# def _delete_maxim_downloaded_file(filename):
#     pass
#
#
# def _incoming_file_path(filename):
#     return "%s%s" % (MAXIM_SFTP_PULL_PATH, filename)
#
#
# def _create_mdd_gen_key(
#     data_key_type, device_id, ds, device_key=None, table_num=None, table_key=None
# ):
#     """
#     Generation of gen key based on the parameters passd
#     :param data_key_type: Type of function the key is generated for
#     :param device_id: Device Id (unique number).
#     :param ds: Timestamp in string format
#     :param device_key: Device Key to be used for function calls
#     :param table_num: Table number being booked
#     :param table_key: Table key that is generated for table
#     :return: DataKey
#     """
#     switcher = {
#         "MDRegister": hashlib.md5(
#             "Maxims%s%sm_r3UtNUTSArC46ByPo_%s"
#             % (MAXIM_FUNCTION_CODES["MDRegister"]["OP"], device_id, ds)
#         ).hexdigest(),
#         "MDLinkTable": hashlib.md5(
#             "Maxims%s%s3uZN5NA0VuNT%s"
#             % (MAXIM_FUNCTION_CODES["MDLinkTable"]["OP"], device_id, ds)
#         ).hexdigest(),
#         "MDOpenTable": hashlib.md5(
#             "Maxims%s%s3uZN5NA0VuNT%s"
#             % (MAXIM_FUNCTION_CODES["MDOpenTable"]["OP"], device_id, ds)
#         ).hexdigest(),
#         "MDLoadTable": hashlib.md5(
#             "Maxims%s%shTqLKgzovq9NrTmIXfoR%s%s%s%s"
#             % (
#                 MAXIM_FUNCTION_CODES["MDLoadTable"]["OP"],
#                 device_id,
#                 device_key,
#                 table_num,
#                 table_key,
#                 ds,
#             )
#         ).hexdigest(),
#         "MDSaveTable": hashlib.md5(
#             "Maxims%s%sNlPdTJJKY2lKZUxShvcA%s%s%s%s"
#             % (
#                 MAXIM_FUNCTION_CODES["MDSaveTable"]["OP"],
#                 device_id,
#                 device_key,
#                 table_num,
#                 table_key,
#                 ds,
#             )
#         ).hexdigest(),
#         "GetSuspendItems": hashlib.md5(
#             "Maxims%s%s3uZN5NA0VuNT%s"
#             % (MAXIM_FUNCTION_CODES["GetSuspendItems"]["OP"], device_id, ds)
#         ).hexdigest(),
#     }
#     return switcher.get(data_key_type, "Invalid MDD Function Key type")
