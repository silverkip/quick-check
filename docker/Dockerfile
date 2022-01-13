ARG TF_SERVING_VERSION=1.15.0-rc2
ARG TF_SERVING_BUILD_IMAGE=tensorflow/serving:${TF_SERVING_VERSION}-devel

FROM ${TF_SERVING_BUILD_IMAGE} as build_image
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install TensorFlow model server
COPY --from=build_image /usr/local/bin/tensorflow_model_server /usr/bin/tensorflow_model_server

ENV BASE_PATH=/models
RUN mkdir -p ${BASE_PATH}

ENV MODEL_NAME=quick_check

COPY models/quick_check models/quick_check
# Create script
RUN echo '#!/bin/bash \n\n\
tensorflow_model_server  --rest_api_port=$PORT \
--model_name=${MODEL_NAME} --model_base_path=${BASE_PATH}/${MODEL_NAME} \
"$@"' > /usr/bin/tf_serving_entrypoint.sh \
&& chmod +x /usr/bin/tf_serving_entrypoint.sh

CMD ["/usr/bin/tf_serving_entrypoint.sh"]