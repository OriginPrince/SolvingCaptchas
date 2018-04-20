# _*_ encoding:utf-8 _*_
# author:ElegyPrincess
import xlrd
data = xlrd.open_workbook('商品资料4.17.xlsx')
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
for i in range(nrows):
      print(table.row_values(i))