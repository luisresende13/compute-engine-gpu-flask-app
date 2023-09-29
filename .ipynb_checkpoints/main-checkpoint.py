# Copyright 2019 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, jsonify
import tensorflow as tf

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return "Server is running!"

@app.route('/gpu', methods=['GET'])
def gpu():
    if tf.config.experimental.list_physical_devices('GPU'):
        return jsonify({'message': 'GPU is available', 'gpu': True})
    else:
        return jsonify({'message': 'GPU is not available', 'gpu': False})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
