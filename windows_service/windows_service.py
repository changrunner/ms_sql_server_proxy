import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
from subprocess import Popen, PIPE, STDOUT, DEVNULL
from zeppos_logging.app_logger import AppLogger
from zeppos_logging.app_logger_json_conifg_name import AppLoggerJsonConfigName
from zeppos_application.app_config import AppConfig
import os
import psutil


class WindowsService(win32serviceutil.ServiceFramework):
    # *************** Only Change This ########################
    # *** These values CAN NOT be gotten from config as the win32serviceutil.ServiceFramework expects them.
    _svc_name_ = "ms_sql_server_proxy_service"  # Change: Name
    _svc_display_name_ = "ms sql server proxy service"  # Change: Description
    # *************** Only Change This ########################

    # Below this is Generated code -- Do not change here.
    @staticmethod
    def get_service_name():
        return WindowsService._svc_name_

    def __init__(self, args):
        AppLogger.logger.info("******* STARTING Windows Service Process")
        AppLogger.logger.debug("Entering __init__")
        try:
            _, self.application_name, self.app_to_start_cmd, self.debug_mode = \
                WindowsService.get_configuration_values()
            AppLogger.logger.debug(f"Args: {args}")
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)
        except Exception as error:
            AppLogger.logger.error(f'Error in __init__: {error}')

        AppLogger.logger.info("Exiting __init__")

    @staticmethod
    def get_configuration_values():
        config_dict = WindowsService._get_config_dict()
        AppLogger.logger.debug(f"service_name: {config_dict['SERVICE_NAME']}")
        AppLogger.logger.debug(f"application_name: {config_dict['APPLICATION_NAME']}")
        AppLogger.logger.debug(f"app_to_start_cmd: {config_dict['APP_TO_START_CMD']}")
        AppLogger.logger.debug(f"debug_mode: {config_dict['DEBUG_MODE']}")
        return config_dict['SERVICE_NAME'], config_dict['APPLICATION_NAME'], \
               config_dict['APP_TO_START_CMD'], config_dict['DEBUG_MODE']

    @staticmethod
    def _get_config_dict():
        return AppConfig.get_json_config_dict(
            current_module_filename=WindowsService._get_configuration_directory(),
            config_file_name=WindowsService._get_configuration_file_name()
        )

    @staticmethod
    def _get_configuration_directory():
        return os.path.join(
            os.path.expanduser('~'), '.config'
        )

    @staticmethod
    def _get_configuration_file_name():
        return f"config_{WindowsService.get_service_name()}.json"

    @staticmethod
    def get_configuration_full_file_name():
        return os.path.join(WindowsService._get_configuration_directory(),
                            WindowsService._get_configuration_file_name())

    def SvcStop(self):
        AppLogger.logger.debug('Entering SvcStop')

        try:
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

            WindowsService.stop_the_process(self.application_name)
        except Exception as error_object:
            AppLogger.logger.error(f'Error in SvcStop: {error_object}')

        AppLogger.logger.debug('Exiting SvcStop')

    def SvcDoRun(self):
        AppLogger.logger.debug('Entering SvcDoRun')

        try:
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
            WindowsService.start_the_process(self.debug_mode, self.app_to_start_cmd, self.application_name)
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)

            rc = None
            while rc != win32event.WAIT_OBJECT_0:
                AppLogger.logger.debug(f"is_running: {WindowsService.is_running(self.application_name)}")
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)

        except Exception as error_object:
            AppLogger.logger.error(f'Error in SvcStop: {error_object}')

        AppLogger.logger.debug('Exit SvcDoRun')

    @staticmethod
    def start_the_process(debug_mode, app_to_start_cmd, application_name):
        AppLogger.logger.debug('Enter start_the_process')
        try:
            AppLogger.logger.debug(f'Starting: [{app_to_start_cmd}]')
            if debug_mode:
                os.makedirs(r"c:\temp", exist_ok=True)
                with open(f"c:\\temp\\{application_name}_log.txt", 'w') as fl:
                    WindowsService.run_process(app_to_start_cmd, fl)
            else:
                WindowsService.run_process(app_to_start_cmd, STDOUT)
            AppLogger.logger.info(f'App started| {application_name} | [{app_to_start_cmd}]')
        except Exception as error_object:
            AppLogger.logger.error(f'Error starting process: [{error_object}]')
        AppLogger.logger.debug('Exit start_the_process')

    @staticmethod
    def run_process(app_to_start_cmd, stdout):
        Popen([app_to_start_cmd], stdout=stdout, stderr=STDOUT, stdin=DEVNULL, shell=False)

    @staticmethod
    def stop_the_process(application_name):
        AppLogger.logger.debug('Enter stop_the_process')
        WindowsService.kill_app(application_name)
        AppLogger.logger.debug('Exit stop_the_process')

    @staticmethod
    def get_pid_full_file_name(application_name):
        current_user_directory = os.path.expanduser("~")
        pid_file_directory = os.path.join(current_user_directory, ".pidfile")
        pid_file_name = f'{application_name}.pid'
        pid_full_file_name = os.path.join(pid_file_directory, pid_file_name)
        AppLogger.logger.debug(f'pid_full_file_name | {pid_full_file_name}')
        return pid_full_file_name

    @staticmethod
    def kill_app(application_name):
        AppLogger.logger.debug("Entering kill_app")
        proc_object = WindowsService.get_proc_object(application_name)
        if proc_object:
            AppLogger.logger.debug(f"Application | {application_name} | Killing")
            proc_object.kill()
            AppLogger.logger.info(f"Application | {application_name} | Killed")
        else:
            AppLogger.logger.info(f"Application | {application_name} | Service not running. Nothing to Kill.")
        AppLogger.logger.debug("Exiting kill_app")

    @staticmethod
    def get_proc_object(application_name):
        AppLogger.logger.debug("Entering get_proc_object")
        pid_full_file_name = WindowsService.get_pid_full_file_name(application_name)
        if os.path.exists(pid_full_file_name):
            AppLogger.logger.debug("pid_full_file_name exits")
            try:
                with open(pid_full_file_name, 'r') as fl:
                    pid_str = fl.readline()  # separate lines for easier infoging thru logs
                    pid = int(pid_str)
                    AppLogger.logger.debug(f"pid | {pid}")

                proc_object = None
                for proc in psutil.process_iter():
                    if proc.pid == pid:
                        proc_object = proc

                if proc_object:
                    AppLogger.logger.debug(
                        f"Application | {application_name} | Proc found with status: {proc_object.status()}")
                    if proc.status().upper() == "RUNNING":
                        AppLogger.logger.debug("Exiting get_proc_object")
                        return proc_object

            except Exception as error_object:
                AppLogger.logger.error(f"Application | {application_name} | get_proc_object error: {error_object}")
        else:
            AppLogger.logger.debug(f"pid_file_not found | {os.path.basename(pid_full_file_name)}")
        AppLogger.logger.debug("Exiting get_proc_object")
        return None

    @staticmethod
    def is_running(application_name):
        return WindowsService.get_proc_object(application_name) is not None


def set_debug_level():
    try:
        _, _, _, debug_mode = WindowsService.get_configuration_values()
        if debug_mode:
            AppLogger.set_debug_level()
            AppLogger.logger.debug(f"{WindowsService.get_service_name()} | logger level | DEBUG")
    except Exception as error:
        AppLogger.logger.error(f'Error getting debug config settings | {error}')


if __name__ == '__main__':
    # The log_group and stream should not be changed.
    # The ip_client in the log string on the cloudwatch stream will allow distinction amongst logs
    AppLogger.configure_and_get_logger(
        "windows_service",
        AppLoggerJsonConfigName.default_with_watchtower_format_1(),
        watchtower_log_group="windows_service",
        watchtower_stream_name=WindowsService.get_service_name()
    )

    try:
        AppLogger.logger.info(f"{WindowsService.get_service_name()} | Entering Main")
        AppLogger.logger.info(f"{WindowsService.get_service_name()} | log_group_name | {AppLogger.get_log_group()}")
        AppLogger.logger.info(f"{WindowsService.get_service_name()} | stream_name | {AppLogger.get_stream_name()}")

        set_debug_level()

        if len(sys.argv) == 1:  # no command line parameters where passed. Start|Stop the windows server
            AppLogger.logger.info(f"{WindowsService.get_service_name()} | service initialize")
            servicemanager.Initialize()
            AppLogger.logger.info(f"{WindowsService.get_service_name()} | prepare to host")
            servicemanager.PrepareToHostSingle(WindowsService)
            AppLogger.logger.info(f"{WindowsService.get_service_name()} | start service dispatch")
            servicemanager.StartServiceCtrlDispatcher()
        else:  # install, remove commands route to here.
            AppLogger.logger.info(f"{WindowsService.get_service_name()} | handle command line")
            win32serviceutil.HandleCommandLine(WindowsService)
    except Exception as error:
        AppLogger.logger.error(f'{WindowsService.get_service_name()} | Error Main | {error}')

    AppLogger.logger.info(f"{WindowsService.get_service_name()} | Exiting Main")
