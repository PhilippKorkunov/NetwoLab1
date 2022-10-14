import pexpect
import argparse


class AdditionalClass:
    # Установка EthTool.
    @staticmethod
    def install(settings: pexpect.spawn):
        if 'install' not in settings.before.decode('utf-8').split():
            settings.sendline("apt install -y ethtool")
            i = settings.expect_exact(["# ", pexpect.TIMEOUT])
            while True:
                if i != 1:
                    return settings
        return settings

    # Создание парсера аргументов
    @staticmethod
    def create_argument_parser():
        parser = argparse.ArgumentParser(description="Network settings")
        parser.add_argument("-m", "--model", action="store_true")
        parser.add_argument("-l", "--link", action="store_true")
        parser.add_argument("-a", "--adapter", action="store_true")
        return parser

    @staticmethod
    def spawn():
        settings = pexpect.spawn("su -")
        settings.expect_exact("#")
        return settings

    @staticmethod
    def send_line(settings: pexpect.spawn, send_lines: list):
        for line in send_lines:
            settings.sendline(line)
        settings.expect_exact("#")
        return settings

    @staticmethod
    def check_input():
        while True:
            input_str = input("Перейти к настройке интерфейсов? [Y/n]: ")
            if input_str == "n":
                return False
            if input_str == "Y":
                return True
            print("Введите либо y - да, либо n -нет")

    @staticmethod
    def interface_print(interfaces: list):
        output = "Какой сетевой интерфейс вы хотите настроить?:\n\n"
        for i in range(len(interfaces)):
            if 'lo' not in interfaces[i]:
                output += f"{i + 1}. {interfaces[i][:-1]}"
            else:
                output += f"\n{i + 1}. {interfaces[i][1:-1]}"

        print(output)
        while True:
            try:
                interface_index = int(input("Укажите номер: "))
                interface = interfaces[interface_index - 1][:-1]
                return interface
            except:
                print("Введите корректный номер\n\n")

    @staticmethod
    def auto_set(settings: pexpect.spawn, interface):
        settings = AdditionalClass.send_line(settings, [f"nmcli connection add con-name \"dhcp\" type "
                                                        f"ethernet ifname {interface}"])
        AdditionalClass.send_line(settings, [f"nmcli conn up \"dhcp\""])

    @staticmethod
    def configurate_set(settings: pexpect.spawn, interface):
        ip_address = input("Введите ip c маской сети в формате XXX.XXX.XXX.XXX/YY \\:\n")
        gateway = input("Введите адрес шлюза в формате XXX.XXX.XXX.XXX/YY: \n")
        dns = input("Введите адрес dns-сервера XXX:XXX:XXX:XXX \n")
        settings = AdditionalClass.send_line(settings, [f"nmcli connection add con-name \"static\" ifname {interface} "
                                                        f"autoconnect no type ethernet ip4 {ip_address} gw4 {gateway}"])
        settings = AdditionalClass.send_line(settings, [f"nmcli conn modify \"static\" ipv4.dns {dns}"])
        settings = AdditionalClass.send_line(settings, [f"nmcli conn up \"static\""])
