# Benchmark on Deep Learning Frameworks and GPUs

Performance of popular deep learning frameworks and GPUs are compared, including the effect of adjusting the floating point precision (the new Volta architecture allows performance boost by utilizing half/mixed-precision calculations.)

The measure metric is latency of running general algoritems via diffrent precisions and framework.

The Result will be csv file with the following fields:
* Timestamp
* Framework
* Algoritem
* BenchStage - eval or train
* Precision
* Result in mileseconds

For running the benchmark press the command with your customize params:
``` bash
   python3 benchmarkGPU-warpper.py -h
   usage: benchmarkGPU-warpper.py [-h] [--log_path LOG_PATH]
                               [--repo_path REPO_PATH]
                               [--result_path RESULT_PATH]
                               [--repo_url REPO_URL]

   Benchmark GPUs Capabilities

   optional arguments:
     -h, --help            show this help message and exit
     --log_path LOG_PATH, -L LOG_PATH
                           a path for logs outputs
     --repo_path REPO_PATH, -R REPO_PATH
                           path for repo clone
     --result_path RESULT_PATH, -O RESULT_PATH
                           Result path
     --repo_url REPO_URL, -U REPO_URL
                           url of the git(helps for private networks)

```

## About

### Deep Learning Frameworks
* PyTorch 0.3.0

* Caffe2 0.8.1

* TensorFlow 1.4.0 (note: this is TensorFlow 1.4.0 compiled against CUDA 9 and CuDNN 7)
  
* TensorFlow 1.5.0

* MXNet 1.0.0 (anyone interested?)

* CNTK (anyone interested?)


### GPUs

|Model     |Architecture|Memory    |CUDA Cores|Tensor Cores|F32 TFLOPS|F16 TFLOPS|Retail|Cloud  |
|----------|------------|----------|----------|------------|----------|----------|------|-----|
|Tesla V100|Volta       |16GB HBM2 |5120      |640         |15.7      |125       |      |$3.06/hr (p3.2xlarge)|


### CUDA / CuDNN
* CUDA 9.0.176
* CuDNN 7.0.0.5
* NVIDIA driver 387.34.
Except where noted.


### Networks
* VGG16
* Resnet152
* Densenet161
* Any others you might be interested in?

# Contributors

* Yusaku Sako
* Bartosz Ludwiczuk (thank you for supplying the V100 numbers)
* Oryan Omer
