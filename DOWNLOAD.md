Dataset **SUIM** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/b/F/7n/YqBQDPAnqgdqLqFnlUG6C8t8vLG0kr6vHgYC5C1KZ2Ia4SNmxAdeFIraNlWrKRfdDOWFaZiK6FMkjKqnyhchHiQhHT9hjh6BItKnjVGdufxo5tVikvym7VPdb1s8.tar)

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

