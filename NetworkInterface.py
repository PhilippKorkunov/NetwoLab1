from AdditionalClass import AdditionalClass


class NetworkInterfaceSettings:
    def __init__(self):
        settings = AdditionalClass.spawn()
        settings = AdditionalClass.send_line(settings, ["dpkg --get-selections | grep ethtool"])
        settings = AdditionalClass.install(settings)
        settings = AdditionalClass.send_line(settings, ["ifconfig -a | sed 's/[ \t].*//;/^$/d'"])
        interfaces = settings.before.decode("utf-8").split('\r')[2:-1]
        self.interface = AdditionalClass.interface_print(interfaces)

    def set(self):
        settings = AdditionalClass.spawn()
        args_parser = AdditionalClass.create_argument_parser()
        args = args_parser.parse_args()

        if args.model:  # Обработка ключа -m\--model
            settings = AdditionalClass.send_line(settings, ["lshw -class network -short"])
            print(settings.before.decode('utf-8'))
            if not AdditionalClass.check_input():
                return "Finished successfully!"

        if args.link:  # Обработка ключа -l\--link
            settings = AdditionalClass.send_line(settings, [f"ip -br -c link show {self.interface}"])
            print("\n".join(settings.before.decode('utf-8').split("\r\n")[1:-1]))
            if not AdditionalClass.check_input():
                return "Finished successfully!"

        if args.adapter:  # Обработка ключа -a\\-adapter
            print(self.interface)
            if "enp" not in self.interface and "eth" not in self.interface:
                return "Доступ данной функции есть только у Ethernet интерфейса"
            settings = AdditionalClass.send_line(settings, [f"ethtool {self.interface}"])
            info = settings.before.decode('utf-8').split("\r\n")
            for i in info:
                if 'Speed' in i or 'Duplex' in i:
                    print(i, "\n")
            if not AdditionalClass.check_input():
                return "Finished successfully"

        if "eth" in self.interface or "enp" in self.interface:
            while True:
                method = int(input("Выбор настройки проводного сетевого интерфейса:\n"
                                   "1. Автонастройка\n2. Настройка вручную\n> "))
                if method == 1:
                    AdditionalClass.auto_set(settings, self.interface)  # Автоматическая настройка
                    return "Автоматическая настройка завершена"
                elif method == 2:
                    AdditionalClass.configurate_set(settings, self.interface)
                    return "Ручная настройка завершена"
                else:
                    print("Укажите '1' для автонастройки или '2' для настройки самостоятельно")
