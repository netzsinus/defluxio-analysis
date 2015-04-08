This is a collection of python programs to analyze the netzsin.us
datasets. Currently, no public export of frequency data is implemented,
but the repository contains some snapshots of the collected data.

Please install the [Anaconda Python Distribution](http://continuum.io/downloads)
since it contains all dependencies for this repository.

Export values :

$ ssh -L 8083:10.23.42.5:8083 -L 8086:10.23.42.5:8086 <HOST>
$ defluxio-exporter -config=/home/md/go/src/github.com/gonium/defluxio/defluxio-exporter.conf -meter=foofrequenz -file="datasets/20140723-export" -start=1405525188 -end=1406126881

