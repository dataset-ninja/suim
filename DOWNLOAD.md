Dataset **SUIM** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/R/5/VH/t88rcCi1nmmtabykb6Xi0FJTA3IqoWa4nMvbXXoQOUQrGkGjO5SL9ipT6SXSpbljUuboauu8qycQsr1y2b1sVHyt19d3IFbPSRZ2CohRZLcexPAUTSGcSr42bDBt.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='SUIM', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

