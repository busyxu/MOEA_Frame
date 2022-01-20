import openpyxl
import xlrd
import xlwt


class Flight:

    def __init__(self, Num, start_t, DS, end_t, AS, Comp):
        self.Num = Num
        self.start_t = start_t
        self.DS = DS
        self.end_t = end_t
        self.AS = AS
        self.Comp = Comp

    def __str__(self):
        return 'Num={}\nstart_t{}\nDS={}\nend_t={}\nAS={}\nComp={}\n'\
            .format(self.Num, self.start_t, self.DS, self.end_t, self.AS, self.Comp)

    __repr__ = __str__


class Person:

    def __init__(self, No, Captain, FirstOffice, Deadhead, Base, DutyCost, ParingCost):
        self.No = No
        self.Captain = Captain
        self.FirstOffice = FirstOffice
        self.Deadhead = Deadhead
        self.Base = Base
        self.DutyCost = DutyCost
        self.ParingCost = ParingCost

    def __str__(self):
        return 'No={}\nCaptain={}\nFirstOffice={}\nDeadHead={}\nBase={}\nDutyCost={}\nParingCost={}\n'\
            .format(self.No, self.Captain, self.FirstOffice, self.Deadhead, self.Base, self.DutyCost, self.ParingCost)

    __repr__ = __str__


class OpData:

    def __init__(self):

        # 打开Excel表格
        # In_data = xlrd.open_workbook(r"DataSource.xlsx")
        self.In_data1 = xlrd.open_workbook(r"Flight1.xlsx")
        self.In_data2 = xlrd.open_workbook(r"Crew.xls")

        # 获取目标EXCEL文件sheet名
        # print(In_data.sheet_names())  # 通过索引顺序获取
        self.table1 = self.In_data1.sheets()[0]
        self.table2 = self.In_data2.sheets()[0]

        # print(table)
        # 通过索引顺序获取
        # table = data.sheet_by_index(0)
        # 通过名称获取
        # table = data.sheet_by_name(u'sheet1')
        # 获取总行数
        self.nrows1 = self.table1.nrows
        self.nrows2 = self.table2.nrows
        # print(nrows)
        # 获取总列数
        self.ncols1 = self.table1.ncols
        self.ncols2 = self.table2.ncols
        # print(ncols)

    def get_Flight(self):
        FlightList = []

        for row in range(self.nrows1)[1:]:
            temp = self.table1.row_values(row)
            temp_f = Flight(temp[0], temp[1]+temp[2], temp[3], temp[4]+temp[5], temp[6], temp[7])
            FlightList.append(temp_f)

        return FlightList

    CrewList = []

    @staticmethod
    def value(val):
        if val == 'Y':
            return 1
        return 0

    def get_Crew(self):
        CrewList = []
        for row in range(self.nrows2)[1:]:
            temp = self.table2.row_values(row)
            temp_f = Person(temp[0], self.value(temp[1]), self.value(temp[2]), self.value(temp[3]), temp[4], temp[5], temp[6])
            CrewList.append(temp_f)
        return CrewList

# P = OpData()
# a = P.get_Flight()
# b = P.get_Crew()
# print(a)
# print(b)