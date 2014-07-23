Export values:

$ ssh -L 8083:10.23.42.5:8083 -L 8086:10.23.42.5:8086 pimp
$ defluxio-exporter -config=/home/md/go/src/github.com/gonium/defluxio/defluxio-exporter.conf -meter=foofrequenz -file="datasets/20140723-export" -start=1405525188 -end=1406126881



Group dataframes:

https://stackoverflow.com/questions/15297053/how-can-i-divide-single-values-of-a-dataframe-by-monthly-averages
http://pandas.pydata.org/pandas-docs/stable/cookbook.html#cookbook-resample

Book:
http://shop.oreilly.com/product/0636920023784.do
