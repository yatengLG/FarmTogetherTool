from core import FarmTogetherCore
from ui_mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.input_validator()

    def input_validator(self):
        # 限制输入大小
        self.ui.Level.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^(250|2[0-4][0-9]|[1-9]?[0-9]?[0-9])')))
        # self.ui.Experience.setValidator()

        money_validator = QtGui.QRegExpValidator(QtCore.QRegExp('^([1-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9])'))
        self.ui.Coins.setValidator(money_validator)
        self.ui.Bills.setValidator(money_validator)
        self.ui.Medals.setValidator(money_validator)
        self.ui.Tickets.setValidator(money_validator)

        resource_validator = QtGui.QRegExpValidator(QtCore.QRegExp('^([1-9]?[0-9]?[0-9]?[0-9]?[0-9])'))
        self.ui.Resource_1_amount.setValidator(resource_validator)
        self.ui.Resource_2_amount.setValidator(resource_validator)
        self.ui.Resource_3_amount.setValidator(resource_validator)
        self.ui.Resource_4_amount.setValidator(resource_validator)
        self.ui.Resource_5_amount.setValidator(resource_validator)
        self.ui.Resource_6_amount.setValidator(resource_validator)
        self.ui.Resource_7_amount.setValidator(resource_validator)
        self.ui.Resource_8_amount.setValidator(resource_validator)
        self.ui.Resource_9_amount.setValidator(resource_validator)
        self.ui.Resource_10_amount.setValidator(resource_validator)
        self.ui.Resource_11_amount.setValidator(resource_validator)
        self.ui.Resource_12_amount.setValidator(resource_validator)
        self.ui.Resource_13_amount.setValidator(resource_validator)
        self.ui.Resource_14_amount.setValidator(resource_validator)
        self.ui.Resource_15_amount.setValidator(resource_validator)
        self.ui.Resource_16_amount.setValidator(resource_validator)

        self.ui.Resource_1_max.setValidator(resource_validator)
        self.ui.Resource_2_max.setValidator(resource_validator)
        self.ui.Resource_3_max.setValidator(resource_validator)
        self.ui.Resource_4_max.setValidator(resource_validator)
        self.ui.Resource_5_max.setValidator(resource_validator)
        self.ui.Resource_6_max.setValidator(resource_validator)
        self.ui.Resource_7_max.setValidator(resource_validator)
        self.ui.Resource_8_max.setValidator(resource_validator)
        self.ui.Resource_9_max.setValidator(resource_validator)
        self.ui.Resource_10_max.setValidator(resource_validator)
        self.ui.Resource_11_max.setValidator(resource_validator)
        self.ui.Resource_12_max.setValidator(resource_validator)
        self.ui.Resource_13_max.setValidator(resource_validator)
        self.ui.Resource_14_max.setValidator(resource_validator)
        self.ui.Resource_15_max.setValidator(resource_validator)
        self.ui.Resource_16_max.setValidator(resource_validator)


class Tools:
    def __init__(self):
        self.core = None
        self.mainwindow = MainWindow()

    def run(self):
        self.mainwindow.show()

    def open_farm_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self.mainwindow)
        if file:
            self.core = FarmTogetherCore(file)
            self.load_values_to_window()
        return True

    def save_farm_file(self):
        if self.core is None or self.core.data is None:
            return True
        file, _ = QtWidgets.QFileDialog.getSaveFileName(self.mainwindow)
        if file:
            try:
                self.core.save(file)
            except Exception as e:
                print(e)
        return True

    def load_values_to_window(self):
        key_value_dict = {}
        if self.core is not None:
            level = self.core.get_farm_level()
            key_value_dict.update(level)
            moneys = self.core.get_money()
            key_value_dict.update(moneys)
            resources = self.core.get_resource()
            key_value_dict.update(resources)

        for key, value in key_value_dict.items():
            if key == 'Level':
                self.mainwindow.ui.Level.setText('{}'.format(value))
            if key == 'Coins':
                self.mainwindow.ui.Coins.setText('{}'.format(value))
            if key == 'Bills':
                self.mainwindow.ui.Bills.setText('{}'.format(value))
            if key == 'Medals':
                self.mainwindow.ui.Medals.setText('{}'.format(value))
            if key == 'Tickets':
                self.mainwindow.ui.Tickets.setText('{}'.format(value))
            if key.startswith('Resource'):
                eval('self.mainwindow.ui.{}_amount'.format(key)).setText('{}'.format(value.get('Amount', 0)))
                eval('self.mainwindow.ui.{}_max'.format(key)).setText('{}'.format(value.get('Max', 0)))
        return True

    def updata_value_to_core_data(self):
        try:
            key_value_dict = {}
            key_value_dict['Level'] = int(self.mainwindow.ui.Level.text())
            key_value_dict['Coins'] = int(self.mainwindow.ui.Coins.text())
            key_value_dict['Bills'] = int(self.mainwindow.ui.Bills.text())
            key_value_dict['Medals'] = int(self.mainwindow.ui.Medals.text())
            key_value_dict['Tickets'] = int(self.mainwindow.ui.Tickets.text())
            key_value_dict['Resource_1'] = {'Amount': int(self.mainwindow.ui.Resource_1_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_1_max.text())}
            key_value_dict['Resource_2'] = {'Amount': int(self.mainwindow.ui.Resource_2_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_2_max.text())}
            key_value_dict['Resource_3'] = {'Amount': int(self.mainwindow.ui.Resource_3_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_3_max.text())}
            key_value_dict['Resource_4'] = {'Amount': int(self.mainwindow.ui.Resource_4_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_4_max.text())}
            key_value_dict['Resource_5'] = {'Amount': int(self.mainwindow.ui.Resource_5_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_5_max.text())}
            key_value_dict['Resource_6'] = {'Amount': int(self.mainwindow.ui.Resource_6_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_6_max.text())}
            key_value_dict['Resource_7'] = {'Amount': int(self.mainwindow.ui.Resource_7_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_7_max.text())}
            key_value_dict['Resource_8'] = {'Amount': int(self.mainwindow.ui.Resource_8_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_8_max.text())}
            key_value_dict['Resource_9'] = {'Amount': int(self.mainwindow.ui.Resource_9_amount.text()),
                                            'Max': int(self.mainwindow.ui.Resource_9_max.text())}
            key_value_dict['Resource_10'] = {'Amount': int(self.mainwindow.ui.Resource_10_amount.text()),
                                             'Max': int(self.mainwindow.ui.Resource_10_max.text())}
            key_value_dict['Resource_11'] = {'Amount': int(self.mainwindow.ui.Resource_11_amount.text()),
                                             'Max': int(self.mainwindow.ui.Resource_11_max.text())}
            key_value_dict['Resource_12'] = {'Amount': int(self.mainwindow.ui.Resource_12_amount.text()),
                                             'Max': int(self.mainwindow.ui.Resource_12_max.text())}
            key_value_dict['Resource_13'] = {'Amount': int(self.mainwindow.ui.Resource_13_amount.text()),
                                             'Max': int(self.mainwindow.ui.Resource_13_max.text())}
            key_value_dict['Resource_14'] = {'Amount': int(self.mainwindow.ui.Resource_14_amount.text()),
                                             'Max': int(self.mainwindow.ui.Resource_14_max.text())}
            key_value_dict['Resource_15'] = {'Amount': int(self.mainwindow.ui.Resource_15_amount.text()),
                                             'Max': int(self.mainwindow.ui.Resource_15_max.text())}
            key_value_dict['Resource_16'] = {'Amount': int(self.mainwindow.ui.Resource_16_amount.text()),
                                             'Max': int(self.mainwindow.ui.Resource_16_max.text())}

            self.core.set_money(key_value_dict)
            self.core.set_farm_level(key_value_dict)
            self.core.set_resource_amount({k: v['Amount'] for (k, v) in key_value_dict.items() if isinstance(v, dict)})
            self.core.set_resource_max({k: v['Max'] for (k, v) in key_value_dict.items() if isinstance(v, dict)})
            self.load_values_to_window()
        except Exception as e:
            print(e)
        return True

    def init_connect(self):
        self.mainwindow.ui.open_button.clicked.connect(self.open_farm_file)
        self.mainwindow.ui.updata_button.clicked.connect(self.updata_value_to_core_data)
        self.mainwindow.ui.save_button.clicked.connect(self.save_farm_file)
        self.mainwindow.ui.Openfile_action.triggered.connect(self.open_farm_file)
        self.mainwindow.ui.Updata_action.triggered.connect(self.updata_value_to_core_data)
        self.mainwindow.ui.Savefile_action.triggered.connect(self.save_farm_file)
        self.mainwindow.ui.Close_action.triggered.connect(self.mainwindow.close)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    tool = Tools()
    tool.init_connect()
    tool.run()
    sys.exit(app.exec_())
